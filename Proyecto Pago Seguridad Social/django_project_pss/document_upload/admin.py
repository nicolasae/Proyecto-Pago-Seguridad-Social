from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Patronal, Gasto, Entidad, valoresPatron,infoPlanilla, valoresPlanilla, valoresEmpleado

# Filters
class EntidadSearchFilter(admin.ModelAdmin):
    search_fields = ['NIT', 'concepto','razonEntidad']  # Search fields
    list_display = ['NIT', 'concepto', 'razonEntidad']  # Fields to show in the list
    # list_filter = ('tipoCuentaPagar',)  # Others filters

class InfoPlanillaSearchFilter(admin.ModelAdmin):
    search_fields = ['numeroPlanilla', 'fecha']  # Search fields
    list_display = ['numeroPlanilla', 'fecha']  # Fields to show in the list

class ValoresPlanillaSearchFilter(admin.ModelAdmin):
    search_fields = ['codigoEntidad__razonEntidad', 'NIT', 'numeroPlanilla__numeroPlanilla','numeroPlanilla__fecha']
    list_display = ('codigoEntidad', 'NIT', 'numeroPlanilla')

class ValoresEmpleadoSearchFilter(admin.ModelAdmin):
    search_fields = ['NIT__NIT','fecha','unidad']
    list_display = ['NIT','fecha','unidad','saldo']

class ValoresPatronSearchFilter(admin.ModelAdmin):
    search_fields = ['NIT__NIT','fecha']
    list_display = ['NIT','fecha','unidad2','unidad8','unidad9','total']

# Register your models here.
admin.site.register(Patronal)
admin.site.register(Gasto)
admin.site.register(Entidad, EntidadSearchFilter)
admin.site.register(infoPlanilla, InfoPlanillaSearchFilter)
admin.site.register(valoresPlanilla, ValoresPlanillaSearchFilter)
admin.site.register(valoresPatron,ValoresPatronSearchFilter)
admin.site.register(valoresEmpleado,ValoresEmpleadoSearchFilter)

