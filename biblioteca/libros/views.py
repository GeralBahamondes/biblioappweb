from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Libro, Prestamo
from .forms import LibroForm
from datetime import date, timedelta
from usuarios.models import Usuario
from django.contrib import messages
from django.utils import timezone


def index(request):
    return render(request, 'libros/index.html')

@login_required
def libros(request):
    libros = Libro.objects.filter(cantidad__gt=0)
    prestamos_usuario = Prestamo.objects.filter(usuario=request.user, libro__in=libros, fecha_devolucion__isnull=True)
    libros_prestados = [prestamo.libro.id for prestamo in prestamos_usuario]
    
    for libro in libros:
        libro.prestado = libro.id in libros_prestados
    
    return render(request, 'libros/books.html', {'libros': libros})

@login_required
def realizar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if libro.cantidad > 0:
        prestamo_existente = Prestamo.objects.filter(usuario=request.user, libro=libro, fecha_devolucion__isnull=True).exists()
        if prestamo_existente:
            messages.error(request, "Ya tienes un préstamo activo de este libro.")
            return redirect('libros')
        
        # Crear el préstamo sin una fecha de devolución
        prestamo = Prestamo.objects.create(
            usuario=request.user,
            libro=libro
        )
        libro.cantidad -= 1
        libro.save()
        messages.success(request, "Préstamo realizado correctamente.")
    else:
        messages.error(request, "El libro no está disponible.")
    return redirect('libros')


@login_required
def devolver_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if prestamo.usuario == request.user:
        prestamo.libro.cantidad += 1
        prestamo.libro.save()
        prestamo.fecha_devolucion = date.today()
        prestamo.save()
        messages.success(request, f"Has devuelto el libro '{prestamo.libro.titulo}' exitosamente.")
    return redirect('historial')

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def gestion_libros(request):
    libros = Libro.objects.all()
    return render(request, 'libros/gestion_libros.html', {'libros': libros})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'El libro ha sido agregado exitosamente.')
            return redirect('gestion_libros')
    else:
        form = LibroForm()
    return render(request, 'libros/agregar_libro.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def editar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, 'El libro ha sido actualizado exitosamente.')
            return redirect('gestion_libros')
    else:
        form = LibroForm(instance=libro)
    return render(request, 'libros/editar_libro.html', {'form': form, 'libro': libro})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def eliminar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, 'El libro ha sido eliminado exitosamente.')
        return redirect('gestion_libros')
    return render(request, 'libros/eliminar_libro.html', {'libro': libro})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def gestion_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'libros/gestion_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def historial_todos_usuarios(request):
    usuarios = Usuario.objects.all()
    prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')
    return render(request, 'libros/historial_todos_usuarios.html', {'usuarios': usuarios, 'prestamos': prestamos})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def devolver_libro_admin(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if not prestamo.fecha_devolucion:
        prestamo.fecha_devolucion = timezone.now()
        prestamo.libro.cantidad += 1
        prestamo.libro.save()
        prestamo.save()
        messages.success(request, f"El libro '{prestamo.libro.titulo}' ha sido devuelto exitosamente.")
    return redirect('historial_todos_usuarios')

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def historial_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    prestamos = Prestamo.objects.filter(usuario=usuario).order_by('-fecha_prestamo')
    return render(request, 'libros/historial_usuario.html', {'usuario': usuario, 'prestamos': prestamos})