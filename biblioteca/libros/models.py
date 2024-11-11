from django.db import models
from usuarios.models import Usuario

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField(default=1)
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='libros/', null=True, blank=True)
    restriccion_edad = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField()

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"