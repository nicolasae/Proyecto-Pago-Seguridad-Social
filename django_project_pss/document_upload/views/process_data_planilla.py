from django.contrib import messages

from ..models import *
from .process_data import *


def extract_data_for_planilla(request,csv_file_path,year,month):
    data = read_data_from_csv(csv_file_path)
    
    # Remove empty strings from the list of lists
    cleaned_data = [[item for item in row if item.strip()] for row in data]

    first_search_word = 'RAZÓN SOCIAL'
    second_search_word = 'TIPO DE PLANILLA'

    min_index = find_index_of_row_by_partial_word(cleaned_data, first_search_word)
    max_index = find_index_of_row_by_partial_word(cleaned_data, second_search_word)

    info_planilla_data = split_data_by_index_range(cleaned_data, min_index, max_index)
    values_planilla_data = split_data_by_index_range(cleaned_data, max_index + 1,len(cleaned_data) -1 )
    
    save_db_info_planilla(request,info_planilla_data,year,month)
    save_db_values_planilla(info_planilla_data,values_planilla_data)

def save_db_info_planilla(request,data,year=None,month=None):
    periodo = year + '/' + month
    numero_planilla = data[8][1]  # Obtener el número de planilla

    try:
        planilla = infoPlanilla.objects.get(numeroPlanilla=numero_planilla)
        print('numeroPlanilla existe')
    except infoPlanilla.DoesNotExist:
        try:
            planilla = infoPlanilla.objects.get(fecha=periodo)
            print('fecha periodo existe')
        except infoPlanilla.DoesNotExist:
            planilla = None
    # print(data)
    if planilla:
        # Update record
        planilla.razonSocial = 'Rama Judicial'
        planilla.fecha = periodo
        planilla.identificacion = data[1][1]
        planilla.codigoDependenciaSucursal = data[2][1]
        planilla.nomDependenciaSucursal = data[3][1]
        planilla.fechaReporte = data[4][1]
        planilla.fechaLimitePago = data[5][1]
        planilla.periodoPension = data[6][1]
        planilla.periodoSalud = data[7][1]
        planilla.totalCotizantes = data[9][1]
        planilla.PIN = data[10][1]
        planilla.tipoPlanilla = data[11][1]
        planilla.save()
    else:
        # Create a new record if it doesn't exist
        planilla = infoPlanilla(
            razonSocial='Rama Judicial',
            fecha=periodo,
            identificacion=data[1][1],
            codigoDependenciaSucursal=data[2][1],
            nomDependenciaSucursal=data[3][1],
            fechaReporte=data[4][1],
            fechaLimitePago=data[5][1],
            periodoPension=data[6][1],
            periodoSalud=data[7][1],
            numeroPlanilla=numero_planilla,
            totalCotizantes=data[9][1],
            PIN=data[10][1],
            tipoPlanilla=data[11][1],
        )
        planilla.save()
    
def save_db_values_planilla(info_planilla_data, values_planilla_data):
    numeroPlanilla = info_planilla_data[8][1]
    for array in values_planilla_data[1:]:
        if len(array) >= 9:
            codigo_entidad = array[0]
            valor_total = array[6] + array[7]
                              
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
                    'numeroAfiliados': array[3],
                    'fondoSolidaridad': array[4],
                    'fondoSubsistencia': array[5],
                    'totalIntereses': array[6],
                    'valorPagarSinIntereses': array[7],
                    'valorPagar': valor_total,
                }
            )

            if not created:
                valores_planilla_instance.NIT = array[1]
                valores_planilla_instance.numeroAfiliados = array[3]
                valores_planilla_instance.fondoSolidaridad = array[4]
                valores_planilla_instance.fondoSubsistencia = array[5]
                valores_planilla_instance.totalIntereses = array[6]
                valores_planilla_instance.valorPagarSinIntereses = array[7]
                valores_planilla_instance.valorPagar = valor_total
                valores_planilla_instance.save()
            # else:
            #     print(f"Created new valoresPlanilla: {valores_planilla_instance}")