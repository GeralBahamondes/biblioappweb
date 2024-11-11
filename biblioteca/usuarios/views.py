from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm, LoginForm, UsuarioChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from libros.models import Prestamo
from django.contrib import messages
from .models import Usuario

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Te has registrado exitosamente.')
            return redirect('libros')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('RUT')
            password = form.cleaned_data.get('password')
            user = authenticate(request, RUT=rut, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Has iniciado sesión correctamente.')
                return redirect('libros')
            else:
                messages.error(request, 'RUT o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def perfil(request):
    prestamos_activos = Prestamo.objects.filter(usuario=request.user, fecha_devolucion__isnull=True)
    return render(request, 'usuarios/profile.html', {'prestamos_activos': prestamos_activos})

@login_required
def historial_prestamos(request):
    prestamos = Prestamo.objects.filter(usuario=request.user).order_by('-fecha_prestamo')
    return render(request, 'usuarios/loan_history.html', {'prestamos': prestamos})

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil ha sido actualizado correctamente.')
            return redirect('perfil')
    else:
        form = UsuarioChangeForm(instance=request.user)
    return render(request, 'usuarios/editar_perfil.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.es_bibliotecario)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        form = UsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.es_bibliotecario = request.POST.get('es_bibliotecario') == 'True'
            usuario.save()
            messages.success(request, f'El perfil de {usuario.username} ha sido actualizado correctamente.')
            return redirect('gestion_usuarios')
    else:
        form = UsuarioChangeForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})