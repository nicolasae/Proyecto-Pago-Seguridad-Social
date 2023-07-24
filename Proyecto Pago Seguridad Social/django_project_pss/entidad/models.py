from django.db import models

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
        return self.tipo

class Entidad(models.Model):
    NIT = models.CharField(max_length=50, primary_key=True, unique=True)
    idTipoGasto = models.ForeignKey(Gasto, on_delete=models.CASCADE)
    concepto = models.CharField(max_length=100)
    razonEntidad = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)
    tipoCuentaPagar = models.IntegerField()
    codigo = models.IntegerField()

    def __str__(self):
        return self.NIT
    
class Motivo(models.Model):
    NIT = models.ForeignKey(Entidad,on_delete=models.CASCADE)
    idPatronal = models.ForeignKey(Patronal,on_delete=models.CASCADE)
    unidad2 = models.IntegerField()
    unidad8 = models.IntegerField()
    unidad9 = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.total

