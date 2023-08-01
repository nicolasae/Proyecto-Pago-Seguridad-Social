import openpyxl
from django.http import HttpResponse

from document_upload.models import *

def get_info_planilla(date):
    # Obtener los objetos de infoPlanilla filtrados por año y mes
    info_planilla = infoPlanilla.objects.filter(periodo=date)
    return info_planilla

def get_values_planilla(date):
    # # Primero, obtén el objeto infoPlanilla correspondiente al periodo deseado
    # info_planilla = infoPlanilla.objects.get(periodo=date)
    
    # # Luego, realiza la consulta para obtener todos los valores de valoresPlanilla asociados al periodo
    # valores_planilla_filtrados = valoresPlanilla.objects.filter(numeroPlanilla=info_planilla)

    # # Ahora puedes iterar sobre los valores filtrados y acceder a sus atributos
    # for valor_planilla in valores_planilla_filtrados:
    #     print(valor_planilla)

    other_data = [
        {'campo1': 'valor1', 'campo2': 'valor2'},
        {'campo1': 'valor3', 'campo2': 'valor4'},
        # Agrega más datos aquí según sea necesario
    ]
    return other_data

def generate_excel_report(info_planilla,values_planilla, year, month):
    # Crear un archivo de Excel para los datos de la planilla
    workbook = openpyxl.Workbook()
    sheet1 = create_sheet_info_planilla(workbook)
    sheet2 = create_sheet_values_planilla(workbook)

    # Escribir los datos para la primera hoja
    write_info_planilla_data(sheet1, info_planilla)

    # Escribir los datos para la segunda hoja
    write_values_planilla_data(sheet2, values_planilla)

    # Crear la respuesta HTTP y devolver el archivo para su descarga
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Planilla_Detallada-{year}-{month}.xlsx"'
    workbook.save(response)

    return response

def create_sheet_info_planilla(workbook):
    sheet = workbook.active
    sheet.title = f"Info Planilla"

    # Mapeo de campos del modelo con los encabezados en el archivo Excel
    field_mapping = {
        'razonSocial': 'RAZON SOCIAL',
        'periodo': 'PERIODO',
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
        sheet.cell(row=row_num, column=1, value=header)

    return sheet

def create_sheet_values_planilla(workbook):
    sheet = workbook.create_sheet(title='Valores Planilla')
    # Escribir los encabezados para la segunda hoja
    sheet.cell(row=1, column=1, value='Campo 1')
    sheet.cell(row=1, column=2, value='Campo 2')

    return sheet

def write_info_planilla_data(sheet, info_planilla):
    # Mapeo de campos del modelo con los encabezados en el archivo Excel
    field_mapping = {
        'razonSocial': 'RAZON SOCIAL',
        'periodo':'PERIODO',
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

    # # Escribir los encabezados en la columna A
    for row_num, header in enumerate(field_mapping.values(), start=1):
        sheet.cell(row=row_num, column=1, value=header)

    row_num = 1
    for obj in info_planilla:
        for key in field_mapping:
            attribute_name = key  # Get the attribute name from the field_mapping
            value = getattr(obj, attribute_name, '')  # Get the attribute value using getattr
            sheet.cell(row = row_num, column = 2, value = value)
            row_num += 1

def write_values_planilla_data(sheet, values_planilla):
    row_num = 2

    for item in values_planilla:
        sheet.cell(row=row_num, column=1, value=item['campo1'])
        sheet.cell(row=row_num, column=2, value=item['campo2'])
        row_num += 1
