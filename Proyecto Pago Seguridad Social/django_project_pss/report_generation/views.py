import openpyxl

from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path

from document_upload.models import *

# Create your views here.
def planilla_report_view(request):
    if request.method == 'POST':
        # Acceder a los datos del formulario que se envían a través del método POST
        selected_year = request.POST.get('selectYear')
        selected_month = request.POST.get('selectMonth')

        # create_report(selected_year, selected_month)
        response = create_report(selected_year,selected_month)
        return response
    return render(request, 'generator_planilla.html') 
            
def create_report(year, month):
    # Obtener los objetos de infoPlanilla filtrados por año y mes
    info_planilla = infoPlanilla.objects.filter(año=year, mes=month)
    filename = f'Planilla_Detallada_{year}_{month}.xlsx'

    # Crea un libro de trabajo de Excel
    workbook = openpyxl.Workbook()

    # Crea la hoja "Informacion General"
    info_general_worksheet = workbook.active
    info_general_worksheet.title = f'Informacion General Planilla'  
    valores_worksheet = workbook.create_sheet(title='Valores Planilla')
  
    create_info_sheet_planilla(info_general_worksheet,info_planilla)
    # create_values_sheet_planilla(valores_worksheet,)

    # Guarda el archivo Excel en un objeto de tipo HttpResponse
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename={}'.format(escape_uri_path(filename))

    # Guarda el contenido del libro de trabajo en el objeto de respuesta
    workbook.save(response)

    return response


def create_info_sheet_planilla(worksheet, info_planilla):
    # Mapeo de campos del modelo con los encabezados en el archivo Excel
    field_mapping = {
        'razonSocial': 'RAZON SOCIAL',
        'identificacion': 'IDENTIFICACION',
        'codigoDependenciaSucursal': 'COD. DEPENDENCIA O SUCURSAL',
        'nomDependenciaSucursal': 'NOM. DEPENDENCIA O SUCURSAL',
        'fechaReporte': 'FECHA GENERACION REPORTE',
        'fechaLimitePago': 'FECHA LIMITE DE PAGO',
        'periodoPension': 'PERIODO PENSION',
        'periodoSalud': 'PERIODO SALUD',
        'numeroPlanilla': 'NUMERO PLANILLA',
        'totalCotizantes': 'TOTAL COTIZANTES',
        'PIN': 'REFERENCIA DE PAGO (PIN)',
        'tipoPlanilla': 'TIPO DE PLANILLA',
    }

    # Escribir los encabezados en la columna A
    for row_num, header in enumerate(field_mapping.values(), start=1):
        worksheet.cell(row=row_num, column=1, value=header)

    row_num = 1
    for obj in info_planilla:
        for key in field_mapping:
            attribute_name = key  # Get the attribute name from the field_mapping
            value = getattr(obj, attribute_name, '')  # Get the attribute value using getattr
            worksheet.cell(row = row_num, column = 2, value = value)
            row_num += 1

# def create_values_sheet_planilla(worksheet, values_planilla):
#     print(values_planilla)