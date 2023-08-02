import openpyxl 
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from django.http import HttpResponse
from document_upload.models import *

def get_data_patronales(date):
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

    motivos = Motivo.objects.filter(fecha=date).order_by('NIT__razonEntidad')
    motivos_ordenados = sorted(motivos, key=lambda motivo: orden_personalizado.index(motivo.NIT.razonEntidad))

    # Crear un diccionario para almacenar la información agrupada por NIT
    data_dict = {}

    for motivo in motivos_ordenados:
        NIT = motivo.NIT.NIT
        tipo_patronal = motivo.tipoPatronal.tipo
        rubro = motivo.NIT.rubro
        concepto = motivo.NIT.concepto
        codigo_descuento = motivo.NIT.codigoDescuento
        fecha = motivo.fecha
        total = motivo.total

        # Verificar si ya existe una entrada para el NIT en el diccionario
        if NIT not in data_dict:
            data_dict[NIT] = {
                'RUBRO': rubro,
                'CONCEPTO': concepto,
                'CODIGO DEL CONCEPTO DE DESCUENTO': codigo_descuento,
                'TEMPORAL UN 2': 0,
                'TEMPORAL UN 8': 0,
                'TEMPORAL UN 9': 0,
                'PERMANENTE UN 2': 0,
                'PERMANENTE UN 8': 0,
                'PERMANENTE UN 9': 0,
                'TOTAL': 0
            }

        # Agregar la información a la entrada correspondiente del tipo_patronal
        if tipo_patronal == 'temporal':
            data_dict[NIT]['TEMPORAL UN 2'] += motivo.unidad2
            data_dict[NIT]['TEMPORAL UN 8'] += motivo.unidad8
            data_dict[NIT]['TEMPORAL UN 9'] += motivo.unidad9
        elif tipo_patronal == 'permanente':
            data_dict[NIT]['PERMANENTE UN 2'] += motivo.unidad2
            data_dict[NIT]['PERMANENTE UN 8'] += motivo.unidad8
            data_dict[NIT]['PERMANENTE UN 9'] += motivo.unidad9

        # También almacenamos la información de unidades 2 en la entrada del tipo patronal
        data_dict[NIT][tipo_patronal] = data_dict[NIT].get(tipo_patronal, 0) + motivo.unidad2

        data_dict[NIT]['TOTAL'] += total

    return data_dict

def copy_data_from_existing_sheet(source_sheet, target_sheet):
    # Leer los datos de la hoja original y copiarlos en la nueva hoja
    for row in source_sheet.iter_rows(values_only=True):
        target_sheet.append(row)

def save_data_patronales(sheet,data):
    # Variable para rastrear el número de fila actual en la hoja de Excel
    current_row = 3

    # Recorrer el diccionario por cada NIT
    for nit, item in data.items():
        sheet[f"A{current_row}"] = nit
        sheet[f"B{current_row}"] = item['RUBRO']
        sheet[f"C{current_row}"] = item['CONCEPTO']
        sheet[f"D{current_row}"] = item['CODIGO DEL CONCEPTO DE DESCUENTO']
        sheet[f"E{current_row}"] = item['TEMPORAL UN 2']
        sheet[f"F{current_row}"] = item['TEMPORAL UN 8']
        sheet[f"G{current_row}"] = item['TEMPORAL UN 9']
        sheet[f"H{current_row}"] = item['PERMANENTE UN 2']
        sheet[f"I{current_row}"] = item['PERMANENTE UN 8']
        sheet[f"J{current_row}"] = item['PERMANENTE UN 9']
        sheet[f"K{current_row}"] = item['TOTAL']

        # Incrementar el número de fila actual para la próxima iteración
        current_row += 1


def generate_excel_report_patronales(year, month):
    date = year + '/' + month
    data = get_data_patronales(date)

    source_file  = 'media/plantillas/Resumen_patronales.xlsx'
    # Cargar el archivo de Excel existente
    source_workbook = load_workbook(source_file)

    # Obtener la primera hoja del archivo de Excel existente
    source_sheet = source_workbook.active

    # Crear un nuevo archivo de Excel para los datos de la planilla
    workbook = openpyxl.Workbook()
    sheet1 = workbook.active

    # Copiar los datos desde la hoja de origen a la nueva hoja
    copy_data_from_existing_sheet(source_sheet, sheet1)

    # Asignar el nombre deseado a la hoja
    sheet_name = f"Datos-{year}-{month}"
    sheet1.title = sheet_name

    # Agregar información adicional a la hoja
    save_data_patronales(sheet1, data)

    # Crear la respuesta HTTP y devolver el archivo para su descarga
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Resumen Patronales-{year}-{month}.xlsx"'
    workbook.save(response)

    return response