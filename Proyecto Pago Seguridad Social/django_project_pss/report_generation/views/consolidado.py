import openpyxl 
from openpyxl import load_workbook
from openpyxl.styles import NamedStyle
from django.http import HttpResponse
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

def convert_empty_to_zero(value):
    return value if value != None else 0

def generate_excel_report_consolidado(data, year, month):

    source_file  = 'media/plantillas/Consolidado.xlsx'
    # Load the existing excel file
    source_workbook = load_workbook(source_file)

    # Get the first sheet of the existing excel file
    source_sheet = source_workbook.active

    # Create a new Excel file for the spreadsheet data
    workbook = openpyxl.Workbook()
    sheet1 = workbook.active

    # Copy the data from the source sheet to the new sheet
    copy_data_from_existing_sheet(source_sheet, sheet1)

    # Assign the desired name to the sheet
    sheet_name = f"Datos-{year}-{month}"
    sheet1.title = sheet_name

    # Add additional information to the sheet
    save_data(sheet1, data)

    # Create the HTTP response and return the file for download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="Consolidado-{year}-{month}.xlsx"'
    workbook.save(response)

    return response

def copy_data_from_existing_sheet(source_sheet, target_sheet):
    # Read the data from the original sheet and copy it to the new sheet
    for row in source_sheet.iter_rows(values_only=True):
        target_sheet.append(row)

def get_data_values(date):
    
    empleados = valoresEmpleado.objects.filter(fecha=date).order_by('NIT__razonEntidad')
    empleados_ordenados = sorted(empleados, key=lambda empleado: orden_personalizado.index(empleado.NIT.razonEntidad))

    patrones = valoresPatron.objects.filter(fecha=date).order_by('NIT__razonEntidad')
    patrones_ordenados = sorted(patrones, key=lambda patron: orden_personalizado.index(patron.NIT.razonEntidad))

    # Create a dictionary to store the information grouped by NIT
    data = {
        'Valores patron':patrones_ordenados,
        'Valores empleado':empleados_ordenados
    }
   
    return data

def process_data_empleados(data):
    # Create a dictionary to store the information grouped by NIT
    data_dict = {}

    for motivo in data:
        NIT = motivo.NIT.NIT
        rubro = motivo.NIT.rubro
        concepto = motivo.NIT.concepto
        unidad = motivo.unidad

        # # Check if an entry for the NIT already exists in the dictionary
        if NIT not in data_dict:
            data_dict[NIT] = {
                'RUBRO': rubro,
                'CONCEPTO': concepto,
                'UNIDAD 2': 0,
                'UNIDAD 8': 0,
                'UNIDAD 9': 0,
                'TOTAL': 0
            }

        # # Add the information to the corresponding entry of type_employer
        data_dict[NIT]['TOTAL'] += motivo.saldo

        if unidad == 2:
            data_dict[NIT]['UNIDAD 2'] += motivo.saldo
        elif unidad == 8:
            data_dict[NIT]['UNIDAD 8'] += motivo.saldo
        elif unidad == 9:
            data_dict[NIT]['UNIDAD 9'] += motivo.saldo
    
    return data_dict

def process_data_patron(data):
    # Create a dictionary to store the information grouped by NIT
    data_dict = {}

    for motivo in data:
        NIT = motivo.NIT.NIT
        tipo_patronal = motivo.tipoPatronal.tipo
        rubro = motivo.NIT.rubro
        concepto = motivo.NIT.concepto
        codigo_descuento = motivo.NIT.codigoDescuento
        total = motivo.total

        # Check if an entry for the NIT already exists in the dictionary
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

        # Add the information to the corresponding entry of type_employer
        if tipo_patronal == 'temporal':
            data_dict[NIT]['TEMPORAL UN 2'] += motivo.unidad2
            data_dict[NIT]['TEMPORAL UN 8'] += motivo.unidad8
            data_dict[NIT]['TEMPORAL UN 9'] += motivo.unidad9
        elif tipo_patronal == 'permanente':
            data_dict[NIT]['PERMANENTE UN 2'] += motivo.unidad2
            data_dict[NIT]['PERMANENTE UN 8'] += motivo.unidad8
            data_dict[NIT]['PERMANENTE UN 9'] += motivo.unidad9

        # We also store the information in the entry of the employer type
        data_dict[NIT][tipo_patronal] = data_dict[NIT].get(tipo_patronal, 0) + motivo.unidad2

        data_dict[NIT]['TOTAL'] += total

    return data_dict

def merger_data_consolidado(data_empleadores, data_patron):
    empleado = process_data_empleados(data_empleadores)
    patron = process_data_patron(data_patron)

    # Crear un nuevo diccionario para almacenar la información combinada agrupada por NIT
    new_dictionary = {}

    # Combinar la información de los diccionarios 'empleado' y 'patron'
    for nit, datos in empleado.items():
        if nit not in new_dictionary:
            new_dictionary[nit] = {}
        new_dictionary[nit]['empleado'] = datos

    for nit, datos in patron.items():
        if nit not in new_dictionary:
            new_dictionary[nit] = {}
        new_dictionary[nit]['patron'] = datos      

    return new_dictionary

def save_data(sheet,data):
    merge_data = merger_data_consolidado(data['Valores empleado'], data['Valores patron'])
    
    # Variable to track the current row number in the excel sheet
    current_row = 3
    sum_empleado_un2 = 0
    sum_empleado_un8 = 0
    sum_empleado_un9 = 0
    total_empleado = 0
    sum_patron_temp2 = 0
    sum_patron_temp8 = 0
    sum_patron_temp9 = 0
    sum_patron_perm2 = 0
    sum_patron_perm8 = 0
    sum_patron_perm9 = 0
    total_patron = 0
    total = 0

    currency_style = NamedStyle(name='currency_style', number_format='"$"#,##0')

    for nit, item in merge_data.items():
        entidad = Entidad.objects.filter(NIT=nit).first()

        sum_empleado_un2 += convert_empty_to_zero(item.get('empleado', {}).get('UNIDAD 2'))      
        sum_empleado_un8 += convert_empty_to_zero(item.get('empleado', {}).get('UNIDAD 8'))      
        sum_empleado_un9 += convert_empty_to_zero(item.get('empleado', {}).get('UNIDAD 9'))      
        total_empleado += convert_empty_to_zero(item.get('empleado', {}).get('TOTAL'))
        sum_patron_temp2 += convert_empty_to_zero(item.get('patron', {}).get('TEMPORAL UN 2')) 
        sum_patron_temp8 += convert_empty_to_zero(item.get('patron', {}).get('TEMPORAL UN 8')) 
        sum_patron_temp9 += convert_empty_to_zero(item.get('patron', {}).get('TEMPORAL UN 9')) 
        sum_patron_perm2 += convert_empty_to_zero(item.get('patron', {}).get('PERMANENTE UN 2'))
        sum_patron_perm8 += convert_empty_to_zero(item.get('patron', {}).get('PERMANENTE UN 8'))
        sum_patron_perm9 += convert_empty_to_zero(item.get('patron', {}).get('PERMANENTE UN 9'))
        total_patron += convert_empty_to_zero(item.get('patron', {}).get('TOTAL'))
        total = total_empleado + total_patron

        sheet[f"A{current_row}"] = entidad.NIT
        sheet[f"B{current_row}"] = entidad.rubro
        sheet[f"C{current_row}"] = entidad.concepto
        sheet[f"D{current_row}"] = convert_empty_to_zero(item.get('empleado', {}).get('UNIDAD 2')) 
        sheet[f"D{current_row}"].style = currency_style
        sheet[f"E{current_row}"] = convert_empty_to_zero(item.get('empleado', {}).get('UNIDAD 8')) 
        sheet[f"E{current_row}"].style = currency_style
        sheet[f"F{current_row}"] = convert_empty_to_zero(item.get('empleado', {}).get('UNIDAD 9')) 
        sheet[f"F{current_row}"].style = currency_style
        sheet[f"G{current_row}"] = convert_empty_to_zero(item.get('empleado', {}).get('TOTAL'))
        sheet[f"G{current_row}"].style = currency_style
        sheet[f"H{current_row}"] = convert_empty_to_zero(item.get('patron', {}).get('TEMPORAL UN 2')) 
        sheet[f"H{current_row}"].style = currency_style
        sheet[f"I{current_row}"] = convert_empty_to_zero(item.get('patron', {}).get('TEMPORAL UN 8')) 
        sheet[f"I{current_row}"].style = currency_style
        sheet[f"J{current_row}"] = convert_empty_to_zero(item.get('patron', {}).get('TEMPORAL UN 9'))
        sheet[f"J{current_row}"].style = currency_style
        sheet[f"K{current_row}"] = convert_empty_to_zero(item.get('patron', {}).get('PERMANENTE UN 2')) 
        sheet[f"K{current_row}"].style = currency_style
        sheet[f"L{current_row}"] = convert_empty_to_zero(item.get('patron', {}).get('PERMANENTE UN 8')) 
        sheet[f"L{current_row}"].style = currency_style
        sheet[f"M{current_row}"] = convert_empty_to_zero(item.get('patron', {}).get('PERMANENTE UN 9')) 
        sheet[f"M{current_row}"].style = currency_style
        sheet[f"N{current_row}"] = convert_empty_to_zero(item.get('patron', {}).get('TOTAL')) 
        sheet[f"N{current_row}"].style = currency_style
        sheet[f"O{current_row}"] = total
        sheet[f"O{current_row}"].style = currency_style

        # Increment the current row number for the next iteration
        current_row += 1
    
    total_data = [
        "",
        "",
        "TOTAL",
        sum_empleado_un2,
        sum_empleado_un8,
        sum_empleado_un9,
        total_empleado,
        sum_patron_temp2,
        sum_patron_temp8,
        sum_patron_temp9,
        sum_patron_perm2,
        sum_patron_perm8,
        sum_patron_perm9,
        total_patron,
    ]

    additional_row_index = current_row 
    for col_idx, value in enumerate(total_data, start=1):
        cell = sheet.cell(row=additional_row_index, column=col_idx, value=value)
        if isinstance(value, (int, float)):
            cell.style = currency_style
     


