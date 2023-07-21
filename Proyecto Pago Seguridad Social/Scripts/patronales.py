import os
import pandas as pd
import csv

from constants import csv_directory

file_name = "PATRONALES PLANTA PERMANENTE - JUN_converted.csv"
words_to_delete = ["UNIDAD 3", "UNIDAD 4", "UNIDAD 5","DSCTO ASMETSALUD PARA SANITAS"]  # List of words to trigger column deletion

# Path to the CSV file
csv_file_path = os.path.join(csv_directory,file_name)

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