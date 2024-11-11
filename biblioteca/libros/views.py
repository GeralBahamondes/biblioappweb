from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Libro, Prestamo
from .forms import LibroForm
from datetime import date, timedelta
from usuarios.models import Usuario
from django.contrib import messages

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
        if Prestamo.objects.filter(usuario=request.user, libro=libro, fecha_devolucion__isnull=True).exists():
            messages.error(request, f"Ya tienes prestado el libro '{libro.titulo}'.")
            return redirect('libros')
        
        if libro.restriccion_edad > 0:
            edad = (date.today() - request.user.fecha_nacimiento).days // 365
            if edad < libro.restriccion_edad:
                messages.error(request, f"Lo siento, debes ser mayor de {libro.restriccion_edad} años para pedir este libro.")
                return redirect('libros')
        
        fecha_devolucion = date.today() + timedelta(weeks=4)
        Prestamo.objects.create(usuario=request.user, libro=libro, fecha_devolucion=fecha_devolucion)
        libro.cantidad -= 1
        libro.save()
        messages.success(request, f"Has pedido prestado el libro '{libro.titulo}' exitosamente.")
    else:
        messages.error(request, f"Lo siento, el libro '{libro.titulo}' no está disponible en este momento.")
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