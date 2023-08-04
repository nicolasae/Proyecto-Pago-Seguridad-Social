from django.contrib import admin
from .models import Patronal, Gasto, Entidad, valoresPatron,infoPlanilla, valoresPlanilla, valoresEmpleado

# Register your models here.
admin.site.register(Patronal)
admin.site.register(Gasto)
admin.site.register(Entidad)
admin.site.register(infoPlanilla)
admin.site.register(valoresPlanilla)
admin.site.register(valoresPatron)
admin.site.register(valoresEmpleado)