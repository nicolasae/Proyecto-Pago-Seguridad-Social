from document_upload.models import *

from ..functions import *
from ..constants import *

def get_number_planilla(date):
     # Get the datasheet objects filtered by year and month
    info_planilla = infoPlanilla.objects.filter(fecha=date)

    for planilla in info_planilla:
        numero_planilla = planilla.numeroPlanilla
    
    return numero_planilla

def get_list_entidades():    
    # Get a list of dictionaries with unique NIT records
    entidades_unicas = Entidad.objects.values('NIT').distinct()
    
    # Get the complete Entity objects for the unique NITs
    entidades_completas = Entidad.objects.filter(NIT__in=[entidad['NIT'] for entidad in entidades_unicas])

    entidades_ordenadas = sorted(entidades_completas, key=lambda entidad: PERSONALIZED_ORDER.index(entidad.razonEntidad))

    return entidades_ordenadas

def get_data_permanentes(date):
    # Filter by tipoPatronal permanente and date
    data = valoresPatron.objects.filter(tipoPatronal__tipo='permanente', fecha=date).order_by('NIT__razonEntidad')
    data_organized = sorted(data, key=lambda item: PERSONALIZED_ORDER.index(item.NIT.razonEntidad))
    return data_organized


def save_data_permanentes(sheet, date):
    data = get_data_permanentes(date)
    numero_planilla = get_number_planilla(date)
    entidades = get_list_entidades()

    suma_unidad2 = 0
    suma_unidad8 = 0
    suma_unidad9 = 0

    sheet[f"C{1}"] = numero_planilla

    # Create a dictionary to store data for each NIT
    nit_data = {}

    # Initialize the nit_data dictionary with zeros and empty fields for each NIT
    for entidad in entidades:
        nit = entidad.NIT 
        nit_data[nit] = {
            'rubro': entidad.rubro,
            'concepto': entidad.concepto,
            'tipoCuentaPagar':entidad.tipoCuentaPagar,
            'codigoDescuento': entidad.codigoDescuento,
            'unidad2': 0,
            'unidad8': 0,
            'unidad9': 0
        }
    

    for entidad in data:
        if entidad.NIT.NIT in nit_data:
            nit_data[entidad.NIT.NIT]['rubro'] = entidad.NIT.rubro
            nit_data[entidad.NIT.NIT]['concepto'] = entidad.NIT.concepto
            nit_data[entidad.NIT.NIT]['tipoCuentaPagar'] = entidad.NIT.tipoCuentaPagar
            nit_data[entidad.NIT.NIT]['codigoDescuento'] = entidad.NIT.codigoDescuento
            nit_data[entidad.NIT.NIT]['unidad2'] += entidad.unidad2
            nit_data[entidad.NIT.NIT]['unidad8'] += entidad.unidad8
            nit_data[entidad.NIT.NIT]['unidad9'] += entidad.unidad9
        else:
            # Store information for NITs that are not in data
            nit_data[entidad.NIT.NIT] = {
                'rubro': entidad.NIT.rubro,
                'concepto': entidad.NIT.concepto,
                'tipoCuentaPagar': entidad.NIT.tipoCuentaPagar,
                'codigoDescuento': entidad.NIT.codigoDescuento,
                'unidad2': 0,
                'unidad8': 0,
                'unidad9': 0
            }

    # Write the data to the Excel sheet
    row_index = 3
    for nit, data in nit_data.items():
        sheet[f"A{row_index}"] = nit
        sheet[f"B{row_index}"] = data['rubro']
        sheet[f"C{row_index}"] = data['concepto']
        sheet[f"D{row_index}"] = data['tipoCuentaPagar']
        sheet[f"E{row_index}"] = data['codigoDescuento']
        sheet[f"I{row_index}"] = data['unidad2']
        sheet[f"J{row_index}"] = data['unidad8']
        sheet[f"K{row_index}"] = data['unidad9']

        #  Add styles to the cells
        sheet[f"I{row_index}"].style = currency_style 
        sheet[f"J{row_index}"].style = currency_style 
        sheet[f"K{row_index}"].style = currency_style 

        suma_unidad2 += data['unidad2']
        suma_unidad8 += data['unidad8']
        suma_unidad9 += data['unidad9']

        row_index += 1

    # Write the total sums to the Excel sheet
    total_data = [
        "supernume",  
        "A0102..",
        "TOTAL",
        "",
        "",        
        0,
        0,
        0,
        suma_unidad2,
        suma_unidad8,
        suma_unidad9
    ]
    
    for col_idx, value in enumerate(total_data, start=1):
        cell = sheet.cell(row=row_index, column=col_idx, value=value)
        if col_idx > 4:
            cell.style = currency_style
        cell.font = bold_font


  