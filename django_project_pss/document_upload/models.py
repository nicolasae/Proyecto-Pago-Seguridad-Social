from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.
class Patronal(models.Model):
    TIPO_CHOICES = (
        ('temporal','Temporal'),
        ('permanente','Permanente')
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    class  Meta:
        verbose_name_plural  =  "Patronales"

    def __str__(self):
        return f"Tipo: {self.tipo}"

class Gasto(models.Model):
    TIPO_CHOICES = (
        ('contribuciones', 'Contribuciones efectivas'),
        ('aportes', 'Aportes sobre nómina'),
    )
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)

    class  Meta:
        verbose_name_plural  =  "Gastos"

    def __str__(self):
        return f"Tipo: {self.tipo}"

class Entidad(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True, default = 'COD')
    NIT = models.CharField(max_length=50)
    idTipoGasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    razonEntidad = models.CharField(max_length=100)
    # rubro = models.CharField(max_length=100)
    rubroPermanente = models.CharField(max_length=100)
    rubroTemporal = models.CharField(max_length=100)
    tipoCuentaPagar = models.CharField(max_length=100)
    codigoDescuento = models.CharField(max_length=100, default = 'COD')
    tipo = models.CharField(max_length=100,default='tipo')

    class  Meta:
        verbose_name_plural  =  "Entidades"

    def __str__(self):
        return f"NIT: {self.NIT} - {self.concepto} - Razón Entidad: {self.razonEntidad}"

class infoPlanilla(models.Model):
    numeroPlanilla = models.CharField(max_length=100, primary_key=True)
    razonSocial = models.CharField(max_length=100, default="Rama Judicial")
    fecha = models.CharField(max_length=10,default='2024/06')
    identificacion = models.CharField(max_length=100)
    fechaLimitePago = models.DateField()
    periodoPension = models.CharField(max_length=7)
    periodoSalud = models.CharField(max_length=7)
    tipoPlanilla = models.CharField(max_length=100)

    class  Meta:
        verbose_name_plural  =  "Información Planillas"

    def __str__(self):
        return f"Fecha reporte: {self.fecha} - Número planilla: {self.numeroPlanilla}"

class valoresPlanilla(models.Model):
    codigoEntidad = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    NIT = models.CharField(max_length=50)
    numeroPlanilla = models.ForeignKey(infoPlanilla,on_delete=models.CASCADE)
    fondoSolidaridad = models.IntegerField(default=0)
    fondoSubsistencia = models.IntegerField(default=0)
    valorPagar = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural  =  "Valores Planilla"
        # Define the combination of fields that must be unique
        unique_together = ('numeroPlanilla', 'codigoEntidad',)

    def __str__(self):
        return  f"{self.numeroPlanilla} - NIT:{self.NIT} - Valor a Pagar: {self.valorPagar}"

class valoresPatron(models.Model):
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    tipoPatronal = models.ForeignKey(Patronal,on_delete=models.CASCADE)
    fecha = models.CharField(max_length=10)
    unidad2 = models.IntegerField(default=0)
    unidad8 = models.IntegerField(default=0)
    unidad9 = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural  =  "Valores Patrón"
        # Define the combination of fields that must be unique
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
        verbose_name_plural  =  "Valores Empleados"
        # Define the combination of fields that must be unique
        unique_together = ('NIT', 'numDoc', 'fecha',)

    def __str__(self):
        return f"Fecha:{self.fecha} {self.NIT} - Unidad: {self.unidad}"


# Definición de la función para manejar el borrado de registros relacionados
@receiver(pre_delete, sender=infoPlanilla)
def delete_related_values(sender, instance, **kwargs):
    valoresPatron.objects.filter(fecha=instance.fecha).delete()
    valoresEmpleado.objects.filter(fecha=instance.fecha).delete()

# Conexión de la señal
pre_delete.connect(delete_related_values, sender=infoPlanilla)