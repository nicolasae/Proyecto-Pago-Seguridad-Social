import openpyxl
from django.http import HttpResponse
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse

from document_upload.models import *

orden_personalizado = [
    'SALUD',
    'RIESGOS PROFESIONALES',
    'PENSION',
    'MEN',
    'SENA',
    'ESAP',
    'ICBF',
    'CAJA DE COMPENSACION FAMILIAR',
]

def get_info_planilla(date):
    # Obtener los objetos de infoPlanilla filtrados por año y mes
    info_planilla = infoPlanilla.objects.filter(periodo=date)
    return info_planilla

def get_values_planilla(date):
    # Primero, obtén el objeto infoPlanilla correspondiente al periodo deseado
    info_planilla = infoPlanilla.objects.get(periodo=date)
    
    # Luego, realiza la consulta para obtener todos los valores de valoresPlanilla asociados al periodo
    valores_planilla_filtrados = valoresPlanilla.objects.filter(numeroPlanilla=info_planilla).order_by('NIT__razonEntidad')

    return valores_planilla_filtrados

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
    sheet = workbook.active
    sheet = workbook.create_sheet(title='Valores Planilla')
    
    headers_sheet = {
        1: "CODIGO ENTIDAD",
        2: "NIT",
        3: "NOMBRE",
        4: "NUMERO AFILIADOS",
        5: "FONDO SOLIDARIDAD",
        6: "FONDO SUBSISTENCIA",
        7: "TOTAL INTERESES",
        8: "VALOR PAGAR SIN INTERESES",
        9: "VALOR PAGAR",
    }

    for col_idx, header_text in headers_sheet.items():
        cell = sheet.cell(row=1, column=col_idx, value=header_text)

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
    distinct_razon_entidades = Entidad.objects.order_by('razonEntidad').values_list('razonEntidad', flat=True).distinct()

    # Initialize row_index for the first group
    row_index = 2

    for razon_entidad in distinct_razon_entidades:
        # Filter values_planilla for the current razon_entidad
        values_planilla_filtered = values_planilla.filter(NIT__razonEntidad=razon_entidad)

        suma_num_afiliados = 0
        suma_fondo_solidaridad = 0
        suma_fondo_subsistencia = 0
        suma_intereses = 0
        suma_sin_intereses = 0
        suma_total = 0

        for planilla in values_planilla_filtered: 
            suma_num_afiliados += planilla.numeroAfiliados
            suma_fondo_solidaridad += planilla.fondoSolidaridad
            suma_fondo_subsistencia += planilla.fondoSubsistencia
            suma_intereses += planilla.totalIntereses
            suma_sin_intereses += planilla.valorPagarSinIntereses
            suma_total += planilla.valorPagar

            sheet[f"A{row_index}"] = planilla.NIT.codigo
            sheet[f"B{row_index}"] = planilla.NIT_id
            sheet[f"C{row_index}"] = planilla.NIT.concepto
            sheet[f"D{row_index}"] = planilla.numeroAfiliados
            sheet[f"E{row_index}"] = planilla.fondoSolidaridad
            sheet[f"F{row_index}"] = planilla.fondoSubsistencia
            sheet[f"G{row_index}"] = planilla.totalIntereses
            sheet[f"H{row_index}"] = planilla.valorPagarSinIntereses
            sheet[f"I{row_index}"] = planilla.valorPagar

            # Increment the row_index for the next row
            row_index += 1

        total_data = [
            "",
            "",
            f"SUBTOTAL {razon_entidad}",
            suma_num_afiliados,
            suma_fondo_solidaridad,
            suma_fondo_subsistencia,
            suma_intereses,
            suma_sin_intereses,
            suma_total
        ]

        sheet.cell(row=row_index, column=1, value=total_data[0])
        sheet.cell(row=row_index, column=2, value=total_data[1])
        sheet.cell(row=row_index, column=3, value=total_data[2])
        for col_idx, value in enumerate(total_data[3:], start=4):
            sheet.cell(row=row_index, column=col_idx, value=value)

        # Increment the row_index for the next group
        row_index += 1

    # Calculate the grand total using all values in values_planilla
    grand_total_data = [
        "",
        "",
        "TOTAL",
        values_planilla.aggregate(Sum('numeroAfiliados'))['numeroAfiliados__sum'],
        values_planilla.aggregate(Sum('fondoSolidaridad'))['fondoSolidaridad__sum'],
        values_planilla.aggregate(Sum('fondoSubsistencia'))['fondoSubsistencia__sum'],
        values_planilla.aggregate(Sum('totalIntereses'))['totalIntereses__sum'],
        values_planilla.aggregate(Sum('valorPagarSinIntereses'))['valorPagarSinIntereses__sum'],
        values_planilla.aggregate(Sum('valorPagar'))['valorPagar__sum']
    ]

    sheet.cell(row=row_index, column=1, value=grand_total_data[0])
    sheet.cell(row=row_index, column=2, value=grand_total_data[1])
    sheet.cell(row=row_index, column=3, value=grand_total_data[2])
    for col_idx, value in enumerate(grand_total_data[3:], start=4):
        sheet.cell(row=row_index, column=col_idx, value=value)