from django.shortcuts import render
from .models import Gasto

# Create your views here.
from .models import Gasto

def lista_gastos(request):
    gastos = Gasto.objects.all()
    return render(request, 'entidad/lista_gastos.html', {'gastos': gastos})