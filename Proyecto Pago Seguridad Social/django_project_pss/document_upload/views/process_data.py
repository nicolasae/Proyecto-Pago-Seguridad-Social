import os
import pandas as pd 
import csv
import shutil

from datetime import datetime

from ..models import *

def converter_xlsx_to_csv( folder_path_xlsx, folder_path_csv):
    try:
        # Cargar el archivo XLSX usando pandas
        dataframe = pd.read_excel(folder_path_xlsx)

        # Guardar el dataframe como archivo CSV
        dataframe.to_csv(folder_path_csv, index=False)
        print("Archivo convertido exitosamente a CSV.")
    except Exception as e:
        print("Error al convertir el archivo:", e)

def clean_empty_rows_csv( path_file ):
    print(path_file)
    #Get path without filename
    dir_without_name = os.path.dirname(path_file)
    temp_file_path = os.path.join(dir_without_name, "temporal.tmp")

    # Open the input CSV file and the temporary output file
    with open(path_file, 'r', encoding='utf-8', newline='') as input_file, \
        open(temp_file_path, 'w', newline='') as output_file:
                        
        # Create a CSV reader and writer objects
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        # Loop through the rows in the input CSV
        for row in csv_reader:
            # Check if the row has any data (non-empty cells)
            if any(field.strip() for field in row):
                # Write the row to the temporary output file
                csv_writer.writerow(row)

    # Replace the original CSV file with the cleaned one
    os.replace(temp_file_path, path_file)

def read_data_from_csv( csv_file_path ):
    data = []
    # Open CSV file in reading mode 
    with open(csv_file_path, 'r', newline='') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        
        #Read data's file and save in data list
        for fila in lector_csv:
            data.append(fila)
    
    return data

def find_index_of_row_by_partial_word(data, search_word):
    for index, row in enumerate(data):
        if search_word in row[0]:
            return index
    return None

def split_data_by_index_range(data, min_index, max_index):
    return data[min_index:max_index + 1]

def search_word_in_csv(csv_file_path, search_word):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for index_row, row in enumerate(reader):
            for index_col, value in enumerate(row):
                if value == search_word:
                    return index_col
    return None

def delete_column_by_index(file_path, index_to_delete):
    # Read the entire content of the original CSV file
    with open(file_path, 'r', newline='') as csvfile:
        rows = list(csv.reader(csvfile))

    # Validate if the provided index is valid
    num_columns = len(rows[0])
    if index_to_delete < 0 or index_to_delete >= num_columns:
        raise ValueError("Invalid index for the column to delete.")

    # Remove the desired column from each row
    for row in rows:
        del row[index_to_delete]

    # Overwrite the original file with the updated content
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)

def delete_columns_by_words(file_path, words_to_delete):
    # Get the indices of columns to delete based on the words found
    columns_to_delete = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Get the header row
        for word in words_to_delete:
            index_col = search_word_in_csv(file_path, word)
            if index_col is not None and index_col not in columns_to_delete:
                columns_to_delete.append(index_col)

    # Delete the corresponding columns from the CSV file
    for index_col in sorted(columns_to_delete, reverse=True):
        delete_column_by_index(file_path, index_col)

def delete_rows_by_words(file_path, words_to_delete):
    # Create a temporary file to write the updated content
    temp_file_path = file_path + '.temp'
    with open(temp_file_path, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                should_delete = False
                for word in words_to_delete:
                    if any(word in cell for cell in row):
                        should_delete = True
                        break
                if not should_delete:
                    writer.writerow(row)

    # Replace the original file with the updated content from the temporary file
    shutil.move(temp_file_path, file_path)

def keep_rows_with_six_columns(file_path):
    # Create a temporary file to write the updated content
    temp_file_path = file_path + '.temp'
    with open(temp_file_path, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if sum(1 for cell in row if cell.strip()) == 6:
                    writer.writerow(row)

    # Replace the original file with the updated content from the temporary file
    shutil.move(temp_file_path, file_path)

def keep_rows_by_fragments(file_path, fragments_to_keep):
    # Create a temporary file to write the updated content
    temp_file_path = file_path + '.temp'
    with open(temp_file_path, 'w', newline='') as temp_file:
        writer = csv.writer(temp_file)
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                should_keep = any(any(fragment in cell for fragment in fragments_to_keep) for cell in row)
                if should_keep:
                    writer.writerow(row)

    # Replace the original file with the updated content from the temporary file
    shutil.move(temp_file_path, file_path)