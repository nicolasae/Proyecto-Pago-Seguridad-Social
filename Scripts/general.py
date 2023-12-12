import csv

def read_data_from_csv( csv_file_path ):
    data = []

    # Open CSV file in reading mode 
    with open(csv_file_path, newline='', encoding='utf-8') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        
        #Read data's file and save in data list
        for fila in lector_csv:
            data.append(fila)
    
    return data