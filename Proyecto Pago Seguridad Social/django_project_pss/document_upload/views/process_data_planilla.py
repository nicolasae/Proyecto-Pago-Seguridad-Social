from ..models import *
from .process_data import *

def extract_data_for_planilla(csv_file_path,year,month):
    data = read_data_from_csv(csv_file_path)
    
    # Remove empty strings from the list of lists
    cleaned_data = [[item for item in row if item.strip()] for row in data]

    first_search_word = 'RAZON SOCIAL'
    second_search_word = 'TIPO DE PLANILLA'

    min_index = find_index_of_row_by_partial_word(cleaned_data, first_search_word)
    max_index = find_index_of_row_by_partial_word(cleaned_data, second_search_word)

    info_planilla_data = split_data_by_index_range(cleaned_data, min_index, max_index)
    values_planilla_data = split_data_by_index_range(cleaned_data, max_index + 1,len(cleaned_data) -1 )
    
    save_db_info_planilla(info_planilla_data,year,month)
    save_db_values_planilla(info_planilla_data,values_planilla_data)

def save_db_info_planilla(data,year=None,month=None):
    if not year:
        year = str(datetime.date.today().year)

    if not month:
        month = str(datetime.date.today().month).zfill(2)

    perido_pension = data[6][1]  
    perido_salud = data[7][1] 

    planilla = infoPlanilla (
        razonSocial = 'Rama Judicial',
        año = year,
        mes = month,
        identificacion = data[1][1],
        codigoDependenciaSucursal = data[2][1],
        nomDependenciaSucursal = data[3][1],
        fechaReporte = data[4][1],
        fechaLimitePago = data[5][1],
        periodoPension = perido_pension,
        periodoSalud = perido_salud,
        numeroPlanilla = data[8][1],
        totalCotizantes = data[9][1],
        PIN = data[10][1],
        tipoPlanilla = data[11][1],
    ) 
    planilla.save()
    
def save_db_values_planilla(info_planilla_data, values_planilla_data):
    numeroPlanilla = info_planilla_data[8][1]

    for array in values_planilla_data[1:]:
        if len(array) >= 9:
            codigoEntidad = array[0]

            # Verificar si el registro ya existe
            try:
                values_planilla = valoresPlanilla.objects.get(
                    codigoEntidad = codigoEntidad,
                    numeroPlanilla__numeroPlanilla = numeroPlanilla
                )
            except valoresPlanilla.DoesNotExist:
                # Si no existe, crear uno nuevo
                values_planilla = valoresPlanilla(
                    codigoEntidad=codigoEntidad,
                    NIT=Entidad.objects.get(NIT=array[1]),
                    numeroPlanilla=infoPlanilla.objects.get(numeroPlanilla=numeroPlanilla),
                    numeroAfiliados=array[3],
                    fondoSolidaridad=array[4],
                    fondoSubsistencia=array[5],
                    totalIntereses=array[6],
                    valorPagarSinIntereses=array[7],
                    valorPagar=array[8], 
                )
            else:
                # Si existe, actualizar los valores
                values_planilla.NIT = Entidad.objects.get(NIT=array[1])
                values_planilla.numeroAfiliados = array[3]
                values_planilla.fondoSolidaridad = array[4]
                values_planilla.fondoSubsistencia = array[5]
                values_planilla.totalIntereses = array[6]
                values_planilla.valorPagarSinIntereses = array[7]
                values_planilla.valorPagar = array[8]

            # Guardar el registro
            values_planilla.save()

