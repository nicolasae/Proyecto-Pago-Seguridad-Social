import os
import openpyxl

from django.contrib import messages
from django.shortcuts import render,redirect
from django.conf import settings

from .process_files import *
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


# This function handles document uploads and processing when the HTTP request method is POST.
def upload_documents( request ):    
    if request.method == 'POST':
        # Access the data from the form submitted via the POST method.
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        # Define a list of dictionaries representing different file types and their new names.
        filesDict = [
            {
                'nombreFormulario': 'planilla',
                'nuevoNombreArchivo': f'Planilla Detallada {selected_year}-{selected_month}.xlsx',
                'nuevoNombreArchivoCSV': f'Planilla Detallada {selected_year}-{selected_month} converted.csv',
            },
            {
                'nombreFormulario': 'patronalesTemporales',
                'nuevoNombreArchivo': f'Patronales Temporales {selected_year}-{selected_month}.xlsx',
                'nuevoNombreArchivoCSV': f'Patronales Temporales {selected_year}-{selected_month} converted.csv',
            },
            {
                'nombreFormulario': 'patronalesPermanentes',
                'nuevoNombreArchivo': f'Patronales Permanentes {selected_year}-{selected_month}.xlsx',
                'nuevoNombreArchivoCSV': f'Patronales Permanentes {selected_year}-{selected_month} converted.csv',
            },
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

       # Define the folder paths for saving the uploaded files in xlsx and csv formats.
        folder_path_xlsx = os.path.join(settings.MEDIA_ROOT, 'xlsx', selected_year, selected_month)
        folder_path_csv = os.path.join(settings.MEDIA_ROOT, 'csv', selected_year, selected_month)
        
        # Ensure that the folders for saving the files exist; if not, create them.
        create_folder_if_not_exists(folder_path_xlsx)
        create_folder_if_not_exists(folder_path_csv)

        # Lista para almacenar los nombres de los formularios que no se proporcionaron.
        missing_files = []

        # Loop through each file type and process the uploaded files.
        for file_info in filesDict:
            form_name = file_info['nombreFormulario']
            new_filename = file_info['nuevoNombreArchivo']
            new_filename_csv = file_info['nuevoNombreArchivoCSV']
            
            # Get the uploaded file for the current file type.
            file = request.FILES.get(form_name)

            # Check if a file was provided for the current form_name before proceeding.
            if file:
                # Set the file paths for the xlsx and csv files.
                path_file_xlsx = os.path.join(folder_path_xlsx, new_filename)
                path_file_csv = os.path.join(folder_path_csv, new_filename_csv)

                # Save the uploaded file to the xlsx folder.
                save_uploaded_file(file, path_file_xlsx)

                # Convert the xlsx file to csv format and save it in the csv folder.           
                converter_xlsx_to_csv(path_file_xlsx, path_file_csv)

                # Clean up the csv file by removing any empty rows.
                clean_empty_rows_csv(path_file_csv)

                # Based on the type of form, extract data from the processed csv file and save it.
                if form_name == 'planilla':
                    extract_data_for_planilla(path_file_csv, selected_year, selected_month)
                if form_name == 'patronalesTemporales':
                    extract_data_patronales_temporales(path_file_csv, selected_year, selected_month)
                if form_name == 'patronalesPermanentes':
                    extract_data_patronales_permanentes(path_file_csv, selected_year, selected_month)
            else:
                # Si no se proporcionó el archivo, agregar el nombre del formulario a la lista de archivos faltantes.
                missing_files.append(form_name)

        # Determine if all files were provided or if some are missing.
        show_alert = len(missing_files) == 0
        alert_type = "success" if show_alert else "danger"
        message = 'Los archivos se han procesado correctamente.' if show_alert else 'Faltan archivos por subir.'

    else:
        # If it is not a POST request, initialize variables so that the alert is not shown.
        missing_files = []
        show_alert = False
        alert_type = "success"  # Puedes establecerlo a "danger" si deseas un mensaje de error por defecto.
        message = ''

    # Dictionary with the context to pass to the 'load_documents.html' template.
    context = {
        'missing_files': missing_files,
        'show_alert': show_alert,
        'alert_type': alert_type,
        'message': message,
    }

    # Render the 'load_documents.html' template with the provided context.
    return render(request, 'load_documents.html', context)


# Render views
def render_list_entidades (request):
    entidades = Entidad.objects.all()
    return render(request, 'list_entidades.html', {'entidades':entidades})

def render_list_plantillas(request):
    return render (request, 'list_plantillas.html')