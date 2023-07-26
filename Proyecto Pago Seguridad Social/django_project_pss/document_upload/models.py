from django.db import models
from django.utils import timezone

# Create your models here.
class Patronal(models.Model):
    TIPO_CHOICES = (
        ('temporal','Temporal'),
        ('permanente','Permanente')
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return self.tipo
    
class Gasto(models.Model):
    TIPO_CHOICES = (
        ('contribuciones', 'Contribuciones efectivas'),
        ('aportes', 'Aportes sobre nómina'),
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    def __str__(self):
        return f"{self.tipo}"

class Entidad(models.Model):
    NIT = models.CharField(max_length=50, primary_key=True, unique=True)
    idTipoGasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    razonEntidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)
    tipoCuentaPagar = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.concepto} - {self.NIT}"
    
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
    razonSocial = models.CharField(max_length=100, default="Rama Judicial")
    identificacion = models.CharField(max_length=100)
    codigoDependenciaSucursal = models.CharField(max_length=100)
    nomDependenciaSucursal = models.CharField(max_length=100)
    fechaReporte = models.DateField()
    fechaLimitePago = models.DateField()
    periodoPension = models.DateField()
    periodoSalud = models.DateField()
    numeroPlanilla = models.CharField(max_length=100)
    totalCotizantes = models.IntegerField()
    PIN = models.CharField(max_length=100)
    tipoPlanilla = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fechaReporte} - {self.numeroPlanilla}"
    
class valoresPlanilla(models.Model):
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    idPlantilla = models.ForeignKey(infoPlanilla,on_delete=models.CASCADE)
    numeroAfiliados = models.IntegerField()
    fondoSolidaridad = models.IntegerField()
    fondoSubsistencia = models.IntegerField()
    totalIntereses = models.IntegerField()
    valorPagarSinIntereses = models.IntegerField()
    valorPagar = models.IntegerField()

    def __str__(self):
        return  f"{self.idPlantilla} - {self.valorPagar}"
