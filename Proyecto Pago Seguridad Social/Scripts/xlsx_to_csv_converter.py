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

def convert_all_files_to_csv( xlsx_directory, csv_directory):
    # Verify if the month directory exist
    create_folder_if_not_exists(csv_directory)

    # Get the list of files in the folder
    files_list = os.listdir(xlsx_directory)

    # Iterate over each file in the folder
    for file in files_list:
        # Check if it's a valid file 
        if file.endswith('.xlsx'): 
            # Full path of the file
            file_path = os.path.join(xlsx_directory, file)
            
            # Read the file into a DataFrame 
            data = pd.read_excel(file_path)

            # Generate the new file name
            file_name, file_extension = os.path.splitext(file)
            new_file_name = file_name + "_converted.csv"

            # Full path of the new file
            new_file_path = os.path.join(csv_directory, new_file_name)

            # # Convert and save as CSV
            data.to_csv(new_file_path, index=False)

            # # Print success message for each converted file
            print(f'The file {file} has been successfully converted to CSV as {new_file_name}.')


# Call Functions
convert_all_files_to_csv(xlsx_directory, csv_directory)