from ..models import *
from .process_data import *

words_to_delete_columns = ["UNIDAD 3", "UNIDAD 4", "UNIDAD 5","DSCTO ASMETSALUD PARA SANITAS"]  # List of words to trigger column deletion
words_to_delete_rows = ["TOTAL","SOLICITUD DE CDP","GASTOS DE ADMINISTRACION Y OPERACION"]

def extract_data_patronales_temporales(csv_file_path,year,month):
    delete_columns_by_words(csv_file_path, words_to_delete_columns)
    delete_rows_by_words(csv_file_path, words_to_delete_rows)

    data = read_data_from_csv(csv_file_path)

    first_search_word_gasto = 'CONTRIBUCIONES EFECTIVAS'
    second_search_word_gasto = 'APORTES SOBRE NOMINA'
    ID_PATRONAL_CONSTANTE = 1

    min_index = find_index_of_row_by_partial_word(data, first_search_word_gasto)
    max_index = find_index_of_row_by_partial_word(data, second_search_word_gasto) - 1

    contribuciones_data = split_data_by_index_range(data, min_index, max_index)
    aportes_data = split_data_by_index_range(data, max_index + 1, len(data) -1 )

    print(contribuciones_data)    
    # print(aportes_data)    

    
   