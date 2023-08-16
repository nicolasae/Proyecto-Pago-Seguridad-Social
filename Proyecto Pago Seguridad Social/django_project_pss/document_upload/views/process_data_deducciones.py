from django.db.models import Q

from ..models import *
from .process_data import *

def extract_data_deducciones(csv_file_path, year, month,unidad):
    clean_data_deducciones(csv_file_path)
    data = read_data_from_csv(csv_file_path)

    save_data_to_valores_empleado(data, unidad, year, month)

def clean_data_deducciones(csv_file_path):
    words_to_delete_columns = [
        "Codigo",
        "Fecha Ejec.",
        "Descripcion Transaccion",
        "Posicion Pago No Pptal",        
        "Valor Doc",
        "Base",
        "Tarifa",
        "Tesoreria",
        "PCI Genera Doc",
        "Orden Pago",
        "Obligacion",
        "Tipo",
        "Num Doc Ter",
        "Beneficiario Orden Pago",
        "Tipo Doc Ben Ded",
        "Beneficiario Deduccion",
        "Administrados DTN",
        "Concepto Declaracion Retefuente",
    ]

    # words_to_delete_update = [
    #     "Descrip Posicion Pago No Pptal",
    # ]

    words_to_keep_rows = ["DTOS"]

    delete_columns_by_words(csv_file_path, words_to_delete_columns)
    keep_rows_by_fragments(csv_file_path,words_to_keep_rows)
    # delete_columns_by_words(csv_file_path, words_to_delete_update)

def calculate_accumulated_balance(data):
    sum_by_entity = {}

    # for item in data[1:]:
    for item in data:
        saldo_sin_comas = item[2].replace(",", "")
        partes = saldo_sin_comas.split(".")
        saldo = int(partes[0])
        
        if item[3] in sum_by_entity:
            print('entro')
            if (saldo > 0):
                sum_by_entity[item[3]][0] += saldo
        else:
            sum_by_entity[item[3]] = [saldo, item[1]]
        

    return sum_by_entity

def get_entidad_instance(nit):       
    try:
        # entidad_instace = Entidad.objects.get(NIT=nit)
        entidad_instace = Entidad.objects.filter(NIT=nit).first()
        razones_entidad_filtrar = ['SALUD', 'RIESGOS PROFESIONALES', 'PENSION']

        if (entidad_instace != None) and (entidad_instace.razonEntidad in razones_entidad_filtrar):
            return entidad_instace
        else:
            return None  

    except Entidad.DoesNotExist:
        print(f"Error: No Entidad instance found with NIT '{nit}'")
        return None

def save_data_to_valores_empleado(data, unidad, year=None, month=None):
    periodo = year + '/' + month
    sum_by_entity = calculate_accumulated_balance(data)

    for nit, values in sum_by_entity.items():
        saldo = values[0]
        num_doc = values[1]

        entidad_instance = get_entidad_instance(nit)
        
        if not entidad_instance:
            continue
        
        # Check if the record already exists before creating a new one
        try:
            empleado_instance = valoresEmpleado.objects.get(NIT=entidad_instance, numDoc=num_doc, fecha=periodo)
            # If the record already exists, update it with the new values
            empleado_instance.saldo = saldo
        except valoresEmpleado.DoesNotExist:
            # If the record does not exist, create a new one
            empleado_instance = valoresEmpleado(
                NIT=entidad_instance,
                fecha=periodo,
                unidad=unidad,
                numDoc=num_doc,
                saldo=saldo
            )

        empleado_instance.save()

