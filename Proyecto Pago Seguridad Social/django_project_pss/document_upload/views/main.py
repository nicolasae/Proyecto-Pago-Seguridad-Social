import os
import openpyxl

from django.contrib import messages
from django.shortcuts import render,redirect
from django.conf import settings

from .upload_files import *
from .process_data import *
from .process_data_entidad import *
from .process_data_planilla import *
from .process_data_patronales import * 


def upload_data_entidades(request):
    if request.method == 'POST' and request.FILES.get('formFile'):
        upload_file = request.FILES['formFile']
        new_file_name = 'datos_entidades.xlsx'
        path = os.path.join(settings.MEDIA_ROOT, new_file_name)
        save_path = save_uploaded_file(upload_file, path)
        show_alert = False

        try:
            workbook = openpyxl.load_workbook(save_path)
            worksheet = workbook.active
            last_row = worksheet.max_row

            context = {
                'show_alert': True,
                'alert_type':"success",
                'message':'El archivo se ha procesado correctamente.',
            }

            for row in worksheet.iter_rows(min_row=2, max_row=last_row, values_only=True):
                process_entidad_row(row)

            # You can perform more operations or redirect to a success page here
            return render(request, 'load_data_entidades.html', context)

        except Exception as e:
            context = {
                'show_alert': True,
                'alert_type':"danger",
                'message':'Ocurrió un error al procesar el archivo.',
            }

            # Error handling if something goes wrong while processing the file
            print(f"Error processing the file: {str(e)}")

            # You can add an error message in the response or redirect to an error page
            return render(request, 'load_data_entidades.html', context)

    return render(request, 'load_data_entidades.html')

def upload_documents( request ):
    if request.method == 'POST':
        # Acceder a los datos del formulario que se envían a través del método POST
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        # Definir la lista de diccionarios para los archivos
        filesDict = [
            # {
            #     'nombreFormulario': 'planilla',
            #     'nuevoNombreArchivo': f'Planilla Detallada {selected_year}-{selected_month}.xlsx',
            #     'nuevoNombreArchivoCSV': f'Planilla Detallada {selected_year}-{selected_month} converted.csv',
            # },
            {
                'nombreFormulario': 'patronalesTemporales',
                'nuevoNombreArchivo': f'Patronales Temporales {selected_year}-{selected_month}.xlsx',
                'nuevoNombreArchivoCSV': f'Patronales Temporales {selected_year}-{selected_month} converted.csv',
            },
            # {
            #     'nombreFormulario': 'patronalesPermanentes',
            #     'nuevoNombreArchivo': f'Patronales Permanentes {selected_year}-{selected_month}.xlsx',
            #     'nuevoNombreArchivoCSV': f'Patronales Permanentes {selected_year}-{selected_month} converted.csv',
            # },
            # {
            #     'nombreFormulario': 'deduc2',
            #     'nuevoNombreArchivo': f'Deducibles Unidad 2 {selected_year}-{selected_month}.xlsx',
            #     'nuevoNombreArchivoCSV': f'Deducibles Unidad 2 {selected_year}-{selected_month} converted.csv',
            # },
            # {
            #     'nombreFormulario': 'deduc8',
            #     'nuevoNombreArchivo': f'Deducibles Unidad 8 {selected_year}-{selected_month}.xlsx',
            #     'nuevoNombreArchivoCSV': f'Deducibles Unidad 8 {selected_year}-{selected_month} converted.csv',
            # },
            # {
            #     'nombreFormulario': 'deduc9',
            #     'nuevoNombreArchivo': f'Deducibles Unidad 9 {selected_year}-{selected_month}.xlsx',
            #     'nuevoNombreArchivoCSV': f'Deducibles Unidad 9 {selected_year}-{selected_month} converted.csv',
            # },
        ]

        folder_path_xlsx = os.path.join(settings.MEDIA_ROOT, 'xlsx', selected_year, selected_month)
        folder_path_csv = os.path.join(settings.MEDIA_ROOT, 'csv', selected_year, selected_month)
        
        create_folder_if_not_exists(folder_path_xlsx)
        create_folder_if_not_exists(folder_path_csv)

        for file_info in filesDict:
            form_name = file_info['nombreFormulario']
            new_filename = file_info['nuevoNombreArchivo']
            new_filename_csv = file_info['nuevoNombreArchivoCSV']
            
            file = request.FILES.get(form_name)
            path_file_xlsx = os.path.join(folder_path_xlsx, new_filename)
            path_file_csv = os.path.join(folder_path_csv, new_filename_csv)

            save_uploaded_file(file, path_file_xlsx)
            converter_xlsx_to_csv(path_file_xlsx,path_file_csv)
            clean_empty_rows_csv(path_file_csv)
            # Guardar informacion de Planilla
            if ( form_name == 'planilla'):
                print('entro a planilla')
                # extract_data_for_planilla(path_file_csv,selected_year,selected_month)
            if ( form_name == 'patronalesTemporales'):
                print('entro a temporales')
                extract_data_patronales_temporales(path_file_csv,selected_year,selected_month)
                
                        
    return render( request, 'load_documents.html')

def render_list_entidades (request):
    entidades = Entidad.objects.all()
    return render(request, 'list_entidades.html', {'entidades':entidades})