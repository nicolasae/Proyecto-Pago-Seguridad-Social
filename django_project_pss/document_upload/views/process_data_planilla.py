from ..models import *
from .process_data import *

def extract_data_for_planilla(request,csv_file_path,year,month):
    data = read_data_from_csv(csv_file_path)
    
    # Remove empty strings from the list of lists
    cleaned_data = [[item for item in row if item.strip()] for row in data]

    first_search_word = 'Datos del Aportante'
    second_search_word = 'Totales de la planilla por administradora'
    third_search_word = 'TOTALES'

    min_index = find_index_of_row_by_partial_word(cleaned_data, first_search_word)
    max_index = find_index_of_row_by_partial_word(cleaned_data, second_search_word)
    max_index_totales = find_index_of_row_by_partial_word(cleaned_data, third_search_word)
    
    info_planilla_data = split_data_by_index_range(cleaned_data, min_index, max_index)
    values_planilla_data = split_data_by_index_range(cleaned_data, max_index + 3,max_index_totales - 1)

    save_db_info_planilla(request,info_planilla_data,year,month)
    save_db_values_planilla(info_planilla_data,values_planilla_data)

def save_db_info_planilla(request,data,year=None,month=None):
    periodo = year + '/' + month
    numero_planilla = data[7][0]
    fecha_limite = data[7][4].replace('/','-')
    try:
        planilla = infoPlanilla.objects.get(numeroPlanilla=numero_planilla)
        print('numeroPlanilla existe')
    except infoPlanilla.DoesNotExist:
        try:
            planilla = infoPlanilla.objects.get(fecha=periodo)
            print('fecha periodo existe')
        except infoPlanilla.DoesNotExist:
            planilla = None
    print(data)
    if planilla:
        # Update record
        planilla.razonSocial = data[3][3]
        planilla.fecha = periodo
        planilla.identificacion = data[3][1]
        planilla.fechaLimitePago = fecha_limite
        planilla.periodoPension = data[7][2]
        planilla.periodoSalud = data[7][3]
        planilla.tipoPlanilla = data[7][1]
        planilla.save()
    else:
        # Create a new record if it doesn't exist
        planilla = infoPlanilla(
            razonSocial = data[3][3],
            fecha = periodo,
            identificacion = data[3][1],
            fechaLimitePago = fecha_limite,
            periodoPension = data[7][2],
            periodoSalud = data[7][3],
            tipoPlanilla = data[7][1],
            numeroPlanilla = numero_planilla,
        )
        planilla.save()
    
def save_db_values_planilla(info_planilla_data, values_planilla_data):
    numeroPlanilla = info_planilla_data[7][0]

    for array in values_planilla_data[0:]:
        codigo_entidad = array[4]
        valor_total = array[16] 

        try:
            planilla_instance = infoPlanilla.objects.get(numeroPlanilla=numeroPlanilla)
        except infoPlanilla.DoesNotExist:
            print(f"Error: No infoPlanilla instance found with number '{numeroPlanilla}'")
            return

        try:
            entidad_instance = Entidad.objects.get(codigo=codigo_entidad)
        except Entidad.DoesNotExist:
            print(f"Warning: No Entidad instance found with codigo '{codigo_entidad}'")
            continue

        valores_planilla_instance, created = valoresPlanilla.objects.get_or_create(
            numeroPlanilla=planilla_instance,
            codigoEntidad=entidad_instance,
            defaults={
                'NIT': array[1],
                'fondoSolidaridad': array[6],
                'fondoSubsistencia': array[7],
                'valorPagar': valor_total,
            }
        )

        if not created:
            valores_planilla_instance.NIT = array[1]
            valores_planilla_instance.fondoSolidaridad = array[6]
            valores_planilla_instance.fondoSubsistencia = array[7]
            valores_planilla_instance.valorPagar = valor_total
            valores_planilla_instance.save()
        # else:
        #     print(f"Created new valoresPlanilla: {valores_planilla_instance}")