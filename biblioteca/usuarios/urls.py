from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views, api_views

urlpatterns = [
    path('registro/', views.registro, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('historial/', views.historial_prestamos, name='historial'),
    path('editar/<int:user_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('eliminar-usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('api/mobile-login/', api_views.mobile_login, name='mobile_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]