from django.contrib import messages

from ..models import *
from .process_data import *

def clean_data_patronales(csv_file_path):
    words_to_delete_columns = ["UNIDAD 3", "UNIDAD 4", "UNIDAD 5","DSCTO ASMETSALUD PARA SANITAS"]  
    words_to_delete_rows = ["TOTAL","SOLICITUD DE CDP","GASTOS DE ADMINISTRACION Y OPERACION","Unnamed","Aporte Patronales"]
    
    delete_columns_by_words(csv_file_path, words_to_delete_columns)
    delete_rows_by_words(csv_file_path, words_to_delete_rows)
    keep_rows_with_six_columns(csv_file_path)

def extract_data_patronales(request,csv_file_path,year,month,type):
    clean_data_patronales(csv_file_path)
   
    data = read_data_from_csv(csv_file_path)
    save_data_patronales(request,data,type, year, month)

def save_data_patronales(request,data,type,year=None,month=None):
    TIPO_PATRONAL_CONSTANTE = Patronal.objects.get(tipo=type) 

    for item in data:
        if (item[0] == '0'):
            NIT = '860011153'
        else:
            NIT = item[0]
        
        if item[2] == '': 
            item[2] = 0
        if item[3] == '':  
            item[3] = 0
        if item[4] == '':  
            item[4] = 0

        total_unidades = int(item[2]) + int(item[3]) + int(item[4])
        periodo = year + '/' + month
        
        entidad_instance = Entidad.objects.filter(NIT=NIT).first()

        if entidad_instance:
            try:
                valores_patron_instance = valoresPatron.objects.get(
                    NIT=entidad_instance,
                    tipoPatronal=TIPO_PATRONAL_CONSTANTE,
                    fecha=periodo,
                )

                #If it does  exists, update values
                valores_patron_instance.unidad2 += int(item[2])
                valores_patron_instance.unidad8 += int(item[3])
                valores_patron_instance.unidad9 += int(item[4])
                valores_patron_instance.total += total_unidades
                valores_patron_instance.save()

            except valoresPatron.DoesNotExist:
                # If it does not exist, create a new record
                valores_patron_instance = valoresPatron(
                    NIT=entidad_instance,
                    tipoPatronal=TIPO_PATRONAL_CONSTANTE,
                    fecha=periodo,
                    unidad2=int(item[2]),
                    unidad8=int(item[3]),
                    unidad9=int(item[4]),
                    total=total_unidades,
                )
                valores_patron_instance.save()
        else:
            print(f"Error: No Entidad instance found with NIT '{NIT}'")
            messages.error(request, f"No se encontró ninguna entidad con NIT '{NIT}' en el archivo de patronales {type}.Por favor agregue la entidad")
            continue