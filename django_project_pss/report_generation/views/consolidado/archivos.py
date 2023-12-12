from document_upload.models import *
from django.db.models import Sum

from ..functions import *
from ..constants import *

def get_data(date):
    
    resultados_filtrados_permanente = valoresPatron.objects.filter(
        fecha=date,
        tipoPatronal__tipo='permanente'
    )

    resultados_filtrados_temporal = valoresPatron.objects.filter(
        fecha=date,
        tipoPatronal__tipo='temporal'
    )
   
    suma_total_un2_permanente = resultados_filtrados_permanente.aggregate(suma_total=Sum('unidad2'))['suma_total']
    suma_total_un8_permanente = resultados_filtrados_permanente.aggregate(suma_total=Sum('unidad8'))['suma_total']
    suma_total_un9_permanente = resultados_filtrados_permanente.aggregate(suma_total=Sum('unidad9'))['suma_total']
    
    suma_total_un2_temporal = resultados_filtrados_temporal.aggregate(suma_total=Sum('unidad2'))['suma_total']
    suma_total_un8_temporal = resultados_filtrados_temporal.aggregate(suma_total=Sum('unidad8'))['suma_total']
    suma_total_un9_temporal = resultados_filtrados_temporal.aggregate(suma_total=Sum('unidad9'))['suma_total']

    suma_total_un2_permanente = suma_total_un2_permanente or 0
    suma_total_un8_permanente = suma_total_un8_permanente or 0
    suma_total_un9_permanente = suma_total_un9_permanente or 0

    suma_total_un2_temporal = suma_total_un2_temporal or 0
    suma_total_un8_temporal = suma_total_un8_temporal or 0
    suma_total_un9_temporal = suma_total_un9_temporal or 0

    print("Suma total de unidad2:", suma_total_un2_permanente)
    print("Suma total de unidad8:", suma_total_un8_permanente)
    print("Suma total de unidad9:", suma_total_un9_permanente)
    print("Suma total de unidad2:", suma_total_un2_temporal)
    print("Suma total de unidad8:", suma_total_un8_temporal)
    print("Suma total de unidad9:", suma_total_un9_temporal)