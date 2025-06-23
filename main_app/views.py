# main_app/views.py

from django.shortcuts import render

def home_view(request):
    # Aquí no necesitamos pasar datos complejos, solo renderizar la plantilla.
    return render(request, 'main_app/home.html', {'titulo_pagina': 'Mi Aplicación Principal'})