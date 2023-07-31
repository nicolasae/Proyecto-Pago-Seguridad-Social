from ..models import *
from .process_data import *

def process_entidad_row(row):
    # Assuming the values are in the following order:
    # NIT, idTipoGasto (foreign keys), concepto, razonEntidad, rubro, tipoCuentaPagar, codigo

    # Get the Gasto instance that matches the value of idTipoGasto in the xlsx file
    try:
        gasto_instance = Gasto.objects.get(tipo=row[1])
    except Gasto.DoesNotExist:
        print(f"Error: No Gasto instance found with type '{row[1]}'")
        return
    except IndexError:
        print("Error: Column 'idTipoGasto' not found in the file")
        return

    # Create an Entidad instance and save it to the database
    entidad = Entidad(
        NIT=row[0],
        idTipoGasto=gasto_instance,
        concepto=row[2],
        razonEntidad=row[3],
        rubro=row[4],
        tipoCuentaPagar=row[5],
        codigo=row[6]
    )
    entidad.save()
