import os
import pandas as pd
import csv

from constants import csv_directory

file_name = "PATRONALES PLANTA PERMANENTE - JUN_converted.csv"
words_to_delete = ["UNIDAD 3", "UNIDAD 4", "UNIDAD 5","DSCTO ASMETSALUD PARA SANITAS"]  # List of words to trigger column deletion

# Path to the CSV file
csv_file_path = os.path.join(csv_directory,file_name)

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
words_to_delete = ["UNIDAD 3", "UNIDAD 4", "UNIDAD 5","DSCTO ASMETSALUD PARA SANITAS"]  # List of words to trigger column deletion

delete_columns_by_words(csv_file_path, words_to_delete)