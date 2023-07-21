import os
import pandas as pd
import csv

# Global Variables
month = "Junio"
# Get the path of the directory where the convert_to_csv.py script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path to the xlsx "files" directory by joining it with the script directory
xlsx_directory = os.path.abspath(os.path.join(script_directory, "..", "Files", "xlsx", month))
csv_directory = os.path.abspath(os.path.join(script_directory, "..", "Files", "csv", month))

def create_folder_if_not_exists(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        try:
            # Create the folder if it doesn't exist
            os.makedirs(folder_path)
            print(f"Folder '{folder_path}' created successfully.")
        except OSError as e:
            print(f"Error: Failed to create folder '{folder_path}'. Reason: {e}")
    else:
        print(f"Folder '{folder_path}' already exists.")

create_folder_if_not_exists(csv_directory)