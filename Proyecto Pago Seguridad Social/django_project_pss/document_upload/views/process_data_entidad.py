from ..models import *
from .process_data import *

def process_entidad_row(row):
    # Get the Gasto instance that matches the value of idTipoGasto in the xlsx file
    try:
        gasto_instance = Gasto.objects.get(tipo=row[2])
    except Gasto.DoesNotExist:
        print(f"Error: No Gasto instance found with type '{row[2]}'")
        return
    except IndexError:
        print("Error: Column 'idTipoGasto' not found in the file")
        return

    # Create an Entidad instance and save it to the database
    entidad = Entidad(
        NIT=row[0],
        codigo=row[1],
        idTipoGasto=gasto_instance,
        concepto=row[3],
        razonEntidad=row[4],
        rubro=row[5],
        tipoCuentaPagar=row[6],
        codigoDescuento=row[7]
    )
    entidad.save()
