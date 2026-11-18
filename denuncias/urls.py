from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.registrar_denuncia, name='registrar_denuncia'),
    path('exito/', views.denuncia_exito, name='denuncia_exito'),
    path('contacto/', views.contacto_soporte, name='contacto_soporte'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Rutas de autenticacion de Django (login, logout, password_change)
    path('accounts/', include('django.contrib.auth.urls')),
]
