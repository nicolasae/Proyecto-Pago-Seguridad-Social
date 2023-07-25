import os
import openpyxl

from django.shortcuts import render
from django.conf import settings

from .models import Patronal, Gasto, Entidad, Motivo

# Create your views here.
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

def save_uploaded_file(uploaded_file, path):
    with open(path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return path

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

def upload_data_entidades(request):
    if request.method == 'POST' and request.FILES.get('formFile'):
        upload_file = request.FILES['formFile']
        new_file_name = 'datos entidades.xlsx'
        path = os.path.join(settings.MEDIA_ROOT, new_file_name)
        save_path = save_uploaded_file(upload_file, path)

        try:
            workbook = openpyxl.load_workbook(save_path)
            worksheet = workbook.active
            last_row = worksheet.max_row

            for row in worksheet.iter_rows(min_row=2, max_row=last_row, values_only=True):
                process_entidad_row(row)

            # You can perform more operations or redirect to a success page here
            # return render(request, 'archivo_cargado.html')

        except Exception as e:
            # Error handling if something goes wrong while processing the file
            print(f"Error processing the file: {str(e)}")
            # You can add an error message in the response or redirect to an error page
            # return render(request, 'error.html')

    return render(request, 'load_data_entidades.html')

def upload_documents( request ):
    if request.method == 'POST':
        # Acceder a los datos del formulario que se envían a través del método POST
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        planilla = request.FILES.get('planilla')
        patronalesTemporales = request.FILES.get('patronalesTemporales')
        patronalesPermanentes = request.FILES.get('patronalesPermanentes')

        planilla_new_name = 'Planilla Detallada' + selected_year + '-' + selected_month + '.xlsx' 

        folder_path = os.path.join(settings.MEDIA_ROOT,'xlsx',selected_year,selected_month)
        planilla_path = os.path.join(folder_path, planilla_new_name)

        create_folder_if_not_exists(folder_path)
        print(planilla_path)
        save_uploaded_file(planilla,planilla_path)        

    return render( request, 'load_documents.html')

