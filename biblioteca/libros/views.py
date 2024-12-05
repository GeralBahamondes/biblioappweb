from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Libro, Prestamo
from .forms import LibroForm
from datetime import date, timedelta
from usuarios.models import Usuario
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
from django.db.models import Q

def index(request):
    return render(request, 'libros/index.html')

@login_required
def libros(request):
    query = request.GET.get('q')
    libros = Libro.objects.filter(cantidad__gt=0)
    
    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(genero__icontains=query)
        )
    
    prestamos_usuario = Prestamo.objects.filter(
        usuario=request.user,
        libro__in=libros,
        estado__in=['pendiente', 'entregado']
    )
    libros_prestados = [prestamo.libro.id for prestamo in prestamos_usuario]
    
    for libro in libros:
        libro.prestado = libro.id in libros_prestados
    
    return render(request, 'libros/books.html', {'libros': libros, 'query': query})

@login_required
def realizar_prestamo(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    if libro.cantidad > 0:
        prestamo_existente = Prestamo.objects.filter(usuario=request.user, libro=libro, estado__in=['pendiente', 'entregado']).exists()
        if prestamo_existente:
            messages.error(request, "Ya tienes un préstamo activo de este libro.")
            return redirect('libros')
        
        prestamo = Prestamo.objects.create(
            usuario=request.user,
            libro=libro,
            estado='pendiente'
        )
        libro.cantidad -= 1
        libro.save()
        messages.success(request, "Préstamo realizado correctamente. Pendiente de entrega.")
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
    query = request.GET.get('q')
    libros = Libro.objects.all()

    if query:
        libros = libros.filter(
            Q(titulo__icontains=query) |
            Q(autor__icontains=query) |
            Q(genero__icontains=query)
        )

    return render(request, 'libros/gestion_libros.html', {'libros': libros, 'query': query})

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
    if prestamo.estado != 'devuelto':
        prestamo.fecha_devolucion = timezone.now()
        prestamo.estado = 'devuelto'
        prestamo.libro.cantidad += 1
        prestamo.libro.save()
        prestamo.save()
        messages.success(request, f"El libro '{prestamo.libro.titulo}' ha sido devuelto exitosamente.")
    return redirect('historial_todos_usuarios')

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def entregar_libro(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    if prestamo.estado == 'pendiente':
        prestamo.estado = 'entregado'
        prestamo.save()
        messages.success(request, f"El libro '{prestamo.libro.titulo}' ha sido entregado exitosamente.")
    return redirect('historial_todos_usuarios')

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def historial_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    prestamos = Prestamo.objects.filter(usuario=usuario).order_by('-fecha_prestamo')
    return render(request, 'libros/historial_usuario.html', {'usuario': usuario, 'prestamos': prestamos})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def dashboard_bibliotecario(request):
    # Libros más prestados
    libros_populares = Prestamo.objects.values('libro__titulo').annotate(
        prestamos=Count('libro')
    ).order_by('-prestamos')[:5]

    # Obtener el máximo número de préstamos para el cálculo de porcentajes
    max_prestamos = libros_populares[0]['prestamos'] if libros_populares else 0

    # Calcular la altura de las barras para cada libro
    for libro in libros_populares:
        # Calcular el porcentaje basado en los préstamos
        libro['altura_barra'] = (libro['prestamos'] / max_prestamos) * 100 if max_prestamos > 0 else 0

    # Estadísticas de usuarios
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(last_login__gte=timezone.now() - timedelta(days=30)).count()
    nuevos_usuarios = Usuario.objects.filter(date_joined__gte=timezone.now() - timedelta(days=30)).count()

    # Últimos préstamos
    ultimos_prestamos = Prestamo.objects.select_related('libro', 'usuario').order_by('-fecha_prestamo')[:5]

    context = {
        'libros_populares': libros_populares,
        'max_prestamos': max_prestamos,
        'estadisticas_usuarios': [
            {'nombre': 'Usuarios Registrados', 'valor': total_usuarios},
            {'nombre': 'Nuevos este mes', 'valor': nuevos_usuarios},
        ],
        'ultimos_prestamos': ultimos_prestamos,
    }

    return render(request, 'libros/dashboard_bibliotecario.html', context)
