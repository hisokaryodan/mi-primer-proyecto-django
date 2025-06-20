# mi_app_web/urls.py

from django.urls import path
from . import views # Importa las vistas de tu app

urlpatterns = [
    path('', views.vista_hola_mundo, name='hola_mundo'),
    path('acerca/', views.vista_acerca_de, name='acerca_de'),
    path('dashboard/', views.dashboard_graficos, name='dashboard_graficos'),
]