from ..models import *
from .process_data import *

def process_entidad_row(row):
    try:
        entidad_instance = Entidad.objects.get(codigo=row[1])
        entidad_instance.NIT = row[0]
        entidad_instance.idTipoGasto = Gasto.objects.get(tipo=row[2])
        entidad_instance.concepto = row[3]
        entidad_instance.razonEntidad = row[4]
        entidad_instance.rubro = row[5]
        entidad_instance.tipoCuentaPagar = row[6]
        entidad_instance.codigoDescuento = row[7]
        entidad_instance.codigoDescuento = row[8]
        entidad_instance.save()
        print(f"Updated existing Entidad: {entidad_instance}")
    except Entidad.DoesNotExist:
        try:
            gasto_instance = Gasto.objects.get(tipo=row[2])
        except Gasto.DoesNotExist:
            print(f"Error: No Gasto instance found with type '{row[2]}'")
            return
        except IndexError:
            print("Error: Column 'idTipoGasto' not found in the file")
            return

        entidad = Entidad(
            NIT=row[0],
            codigo=row[1],
            idTipoGasto=gasto_instance,
            concepto=row[3],
            razonEntidad=row[4],
            rubro=row[5],
            tipoCuentaPagar=row[6],
            codigoDescuento=row[7],
            tipo=row[8]
        )
        entidad.save()
