from ..models import *
from .process_data import *

words_to_delete = ["UNIDAD 3", "UNIDAD 4", "UNIDAD 5","DSCTO ASMETSALUD PARA SANITAS"]  # List of words to trigger column deletion

def extract_data_patronales_temporales(csv_file_path,year,month):
    # data = read_data_from_csv(csv_file_path)
    delete_columns_by_words(csv_file_path, words_to_delete)
