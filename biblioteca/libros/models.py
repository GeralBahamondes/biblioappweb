from django.db import models
from usuarios.models import Usuario

GENEROS_CHOICES = [
    ('Ficción', 'Ficción'),
    ('No ficción', 'No ficción'),
    ('Misterio', 'Misterio'),
    ('Ciencia ficción', 'Ciencia ficción'),
    ('Fantasía', 'Fantasía'),
    ('Romance', 'Romance'),
    ('Thriller', 'Thriller'),
    ('Biografía', 'Biografía'),
    ('Historia', 'Historia'),
    ('Ciencia', 'Ciencia'),
    ('Otro', 'Otro'),
]

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    genero = models.CharField(max_length=50, choices=GENEROS_CHOICES)
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
    fecha_devolucion = models.DateField(null=True, blank=True) 
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente de entrega'),
        ('entregado', 'Entregado'),
        ('devuelto', 'Devuelto'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"