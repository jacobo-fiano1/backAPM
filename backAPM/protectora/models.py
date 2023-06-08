from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Protectora(models.Model):
    name = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=500)
    telefono = models.CharField(max_length=10)
    url = models.CharField(max_length=200)
    correo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=500)
    imagen = models.FileField(upload_to='protectoras/images/', blank='', default='')

    class Meta:
        managed = True
        db_table = 'protectora_protectora'
    
    def __str__(self):
        return f"{self.name} {self.url}"
    
class Animal(models.Model):
    class Estado(models.TextChoices):
        ADOPTADO = "AD", _("Adoptado")
        RESERVADO = "RV", _("Reservado")
        DISPONIBLE = "DP", _("Disponible")
    
    class Edad(models.TextChoices):
        CACHORRO = "CA", _("Cachorro")
        ADULTO = "AD", _("Adulto")
        SENIOR = "SN", _("Senior")

    name = models.CharField(max_length=200)
    fechaNacimiento = models.DateField()
    descripcion = models.CharField(max_length=500)
    imagen = models.FileField(upload_to='animals/images/', blank='', default='')
    tipo = models.CharField(max_length=50)
    edad = models.CharField(choices=Edad.choices, default=Edad.ADULTO, max_length=2)
    protectora = models.ForeignKey(Protectora, on_delete=models.DO_NOTHING)
    estado = models.CharField(choices=Estado.choices, default=Estado.DISPONIBLE, max_length=2)
    vacunas = ArrayField(models.CharField(max_length=200), default=list)

    class Meta:
        managed = True
        db_table = 'protectora_animal'

    def __str__(self):
        return f"{self.name}, {self.protectora}"
    