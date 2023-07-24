import os

from django.shortcuts import render
from .models import Gasto, Entidad

def lista_gastos(request):
    gastos = Gasto.objects.all()
    return render(request, 'entidad/lista_gastos.html', {'gastos': gastos})

def cargar_datos_entidades(request):
    if request.method == 'POST' and request.FILES['formFile']:
        archivo_adjunto = request.FILES['formFile']
        
        # Nombre específico del archivo que deseas guardar
        nombre_nuevo_archivo = "datos entidades.xlsx"
        ruta_guardado = os.path.join("C:\\Users\\naguie\\Desktop\\DSAJ\\Proyecto Pago Seguridad Social\\django_project_pss\\entidad\\static", nombre_nuevo_archivo)
        print(ruta_guardado)

        # Procesa el archivo adjunto aquí
        with open(ruta_guardado, 'wb') as destino:
            for chunk in archivo_adjunto.chunks():
                destino.write(chunk)
        
        # Aquí puedes realizar más operaciones con el archivo, como guardar datos en la base de datos, etc.
        # return render(request, 'archivo_cargado.html')
    return render(request, 'entidad/cargar_datos_entidades.html')
    

