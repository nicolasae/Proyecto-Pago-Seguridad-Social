import os
import openpyxl

from django.shortcuts import render
from django.conf import settings

from .models import Gasto, Entidad

def load_data_entidades(request):
    if request.method == 'POST' and request.FILES.get('formFile'):
        archivo_adjunto = request.FILES['formFile']
        save_path = save_uploaded_file(archivo_adjunto)

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

    return render(request, 'entidad/load_data_entidades.html')

def save_uploaded_file(uploaded_file):
    new_file_name = "datos entidades.xlsx"
    save_path = os.path.join(settings.STATIC_ROOT, new_file_name)

    with open(save_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return save_path

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

def list_entidad(request):
    entidades = Entidad.objects.all()
    print(entidades[0].idTipoGasto)
    return render(request, 'entidad/list_entidades.html', {'entidades':entidades})