import os
import csv

from constants import csv_directory

def clean_empty_row_csv_files(csv_directory):
    # Get the list of files in the folder
    files_list = os.listdir(csv_directory)
    
    files_list = os.listdir(csv_directory)

    for filename in files_list:
        if filename.endswith('.csv'):
            file_path = os.path.join(csv_directory, filename)
            temp_file_path = os.path.join(csv_directory, f"{filename}.tmp")

            # Open the input CSV file and the temporary output file
            with open(file_path, 'r', newline='') as input_file, \
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
            os.replace(temp_file_path, file_path)

# Call Functions
clean_empty_row_csv_files(csv_directory)