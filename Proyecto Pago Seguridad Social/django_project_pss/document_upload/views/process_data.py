import os
import pandas as pd 
import csv

from ..models import Patronal, Gasto, Entidad, Motivo

def converter_xlsx_to_csv( folder_path_xlsx, folder_path_csv):
    try:
        # Cargar el archivo XLSX usando pandas
        dataframe = pd.read_excel(folder_path_xlsx)

        # Guardar el dataframe como archivo CSV
        dataframe.to_csv(folder_path_csv, index=False)
        # print("Archivo convertido exitosamente a CSV.")
    except Exception as e:
        print("Error al convertir el archivo:", e)


def process_entidad_row(row):
    # Assuming the values are in the following order:
    # NIT, idTipoGasto (foreign keys), concepto, razonEntidad, rubro, tipoCuentaPagar, codigo

    # Get the Gasto instance that matches the value of idTipoGasto in the xlsx file
    try:
        gasto_instance = Gasto.objects.get(tipo=row[1])
    except Gasto.DoesNotExist:
        print(f"Error: No Gasto instance found with type '{row[1]}'")
        return
    except IndexError:
        print("Error: Column 'idTipoGasto' not found in the file")
        return

    # Create an Entidad instance and save it to the database
    entidad = Entidad(
        NIT=row[0],
        idTipoGasto=gasto_instance,
        concepto=row[2],
        razonEntidad=row[3],
        rubro=row[4],
        tipoCuentaPagar=row[5],
        codigo=row[6]
    )
    entidad.save()

def clean_empty_rows_csv( path_file ):
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
