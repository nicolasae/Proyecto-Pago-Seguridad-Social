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
    codigo = models.CharField(max_length=100,default = 'COD')
    idTipoGasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    razonEntidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)
    tipoCuentaPagar = models.CharField(max_length=100)
    codigoDescuento = models.CharField(max_length=100, default = 'COD')

    def __str__(self):
        return f"{self.concepto} - NIT: {self.NIT} - Razón Entidad: {self.razonEntidad}"
    
class valoresPatron(models.Model):
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    tipoPatronal = models.ForeignKey(Patronal,on_delete=models.CASCADE)
    fecha = models.CharField(max_length=10)
    unidad2 = models.IntegerField(default=0)
    unidad8 = models.IntegerField(default=0)
    unidad9 = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    class Meta:
        # Definir la combinación de campos que debe ser única
        unique_together = ('NIT', 'tipoPatronal', 'fecha',)

    def __str__(self):
        return f"Fecha:{self.fecha} {self.NIT} - {self.tipoPatronal} - Total: {self.total}"
    
class valoresEmpleado(models.Model):
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    fecha = models.CharField(max_length=10)
    unidad = models.IntegerField()
    numDoc = models.CharField(max_length=30)
    saldo = models.IntegerField(default=0)

    class Meta:
        # Definir la combinación de campos que debe ser única
        unique_together = ('NIT', 'numDoc', 'fecha',)

    def __str__(self):
        return f"{self.NIT} - Unidad: {self.unidad}"

class infoPlanilla(models.Model):
    numeroPlanilla = models.CharField(max_length=100, primary_key=True)
    razonSocial = models.CharField(max_length=100, default="Rama Judicial")
    periodo = models.CharField(max_length=10,default='2023/06')
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
        return f"Fecha reporte: {self.periodo} - Número planilla: {self.numeroPlanilla}"
    
class valoresPlanilla(models.Model):
    codigoEntidad = models.CharField(max_length=100)
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    numeroPlanilla = models.ForeignKey(infoPlanilla,on_delete=models.CASCADE)
    numeroAfiliados = models.IntegerField()
    fondoSolidaridad = models.IntegerField(default=0)
    fondoSubsistencia = models.IntegerField(default=0)
    totalIntereses = models.IntegerField(default=0)
    valorPagarSinIntereses = models.IntegerField(default=0)
    valorPagar = models.IntegerField(default=0)

    class Meta:
        # Definir la combinación de campos que debe ser única
        unique_together = ('numeroPlanilla', 'codigoEntidad',)

    def __str__(self):
        return  f"{self.numeroPlanilla} - {self.NIT} - Valor a Pagar: {self.valorPagar}"
