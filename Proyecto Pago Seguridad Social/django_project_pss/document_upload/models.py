from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Patronal(models.Model):
    TIPO_CHOICES = (
        ('temporal','Temporal'),
        ('permanente','Permanente')
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return f"Tipo: {self.tipo}"
    
class Gasto(models.Model):
    TIPO_CHOICES = (
        ('contribuciones', 'Contribuciones efectivas'),
        ('aportes', 'Aportes sobre nómina'),
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return f"Tipo: {self.tipo}"

class Entidad(models.Model):
    NIT = models.CharField(max_length=50, primary_key=True, unique=True)
    idTipoGasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    razonEntidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)
    tipoCuentaPagar = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.concepto} - NIT: {self.NIT} - Razón Entidad: {self.razonEntidad}"
    
class Motivo(models.Model):
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    idPatronal = models.ForeignKey(Patronal,on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    unidad2 = models.IntegerField()
    unidad8 = models.IntegerField()
    unidad9 = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.total

class infoPlanilla(models.Model):
    numeroPlanilla = models.CharField(max_length=100, primary_key=True)
    razonSocial = models.CharField(max_length=100, default="Rama Judicial")
    año = models.CharField(max_length=4)
    mes = models.CharField(max_length=2)
    identificacion = models.CharField(max_length=100)
    codigoDependenciaSucursal = models.CharField(max_length=100)
    nomDependenciaSucursal = models.CharField(max_length=100)
    fechaReporte = models.DateField()
    fechaLimitePago = models.DateField()
    periodoPension = models.CharField(max_length=7)
    periodoSalud = models.CharField(max_length=7)
    totalCotizantes = models.IntegerField()
    PIN = models.CharField(max_length=100)
    tipoPlanilla = models.CharField(max_length=100)

    def __str__(self):
        return f"Fecha reporte: {self.año}/{self.mes} - Número planilla: {self.numeroPlanilla}"
    
class valoresPlanilla(models.Model):
    codigoEntidad = models.CharField(max_length=100)
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    numeroPlanilla = models.ForeignKey(infoPlanilla,on_delete=models.CASCADE)
    numeroAfiliados = models.IntegerField()
    fondoSolidaridad = models.IntegerField()
    fondoSubsistencia = models.IntegerField()
    totalIntereses = models.IntegerField()
    valorPagarSinIntereses = models.IntegerField()
    valorPagar = models.IntegerField()

    class Meta:
        # Definir la combinación de campos que debe ser única
        unique_together = ('numeroPlanilla', 'codigoEntidad',)

    def __str__(self):
        return  f"{self.numeroPlanilla} - {self.NIT} - Valor a Pagar: {self.valorPagar}"
