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
        "Descrip Posicion Pago No Pptal",
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

    delete_columns_by_words(csv_file_path, words_to_delete_columns)

def calculate_accumulated_balance(data):
    sum_by_entity = {}

    for item in data[1:]:
        saldo_sin_comas = item[1].replace(",", "")
        partes = saldo_sin_comas.split(".")
        saldo = int(partes[0])

        if item[2] in sum_by_entity:
            sum_by_entity[item[2]][0] += saldo
        else:
            sum_by_entity[item[2]] = [saldo, item[0]]

    return sum_by_entity

def get_entidad_instance(nit):       
    try:
        entidad_instace = Entidad.objects.get(NIT=nit)
        razones_entidad_filtrar = ['SALUD', 'RIESGOS PROFESIONALES', 'PENSION']
        if entidad_instace.razonEntidad in razones_entidad_filtrar:
            print(entidad_instace)
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

