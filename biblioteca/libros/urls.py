from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.libros, name='libros'),
    path('prestamo/<int:libro_id>/', views.realizar_prestamo, name='realizar_prestamo'),
    path('devolver/<int:prestamo_id>/', views.devolver_libro, name='devolver_libro'),
    path('gestion-libros/', views.gestion_libros, name='gestion_libros'),
    path('gestion-libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('gestion-libros/editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('gestion-libros/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),
    path('gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('historial_usuario/<int:usuario_id>/', views.historial_usuario, name='historial_usuario'),
    path('devolver-libro-admin/<int:prestamo_id>/', views.devolver_libro_admin, name='devolver_libro_admin'),
    path('historial-todos-usuarios/', views.historial_todos_usuarios, name='historial_todos_usuarios'),

]