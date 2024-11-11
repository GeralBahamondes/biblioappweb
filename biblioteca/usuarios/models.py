from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    RUT = models.CharField(max_length=12, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    es_bibliotecario = models.BooleanField(default=False)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'RUT'
    REQUIRED_FIELDS = ['username', 'email', 'direccion', 'telefono', 'fecha_nacimiento']

    def __str__(self):
        return self.username