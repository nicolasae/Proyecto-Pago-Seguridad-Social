import os

# Global Variables
month = "Junio"
# Get the path of the directory where the convert_to_csv.py script is located
script_directory = os.path.dirname(os.path.abspath(__file__))
# Get the absolute path to the xlsx "files" directory by joining it with the script directory
xlsx_directory = os.path.abspath(os.path.join(script_directory, "..", "Files", "xlsx", month))
csv_directory = os.path.abspath(os.path.join(script_directory, "..", "Files", "csv", month))
