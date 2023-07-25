from django.contrib import admin
from .models import Patronal, Gasto, Entidad, Motivo

# Register your models here.
admin.site.register(Patronal)
admin.site.register(Gasto)
admin.site.register(Entidad)
admin.site.register(Motivo)