# mi_app_web/views.py

from django.shortcuts import render
from django.http import HttpResponse # Importa HttpResponse

def vista_hola_mundo(request):
    return HttpResponse("<h1>¡Hola, soy tu primera vista en Django!</h1>")

def vista_acerca_de(request):
    return HttpResponse("<h2>Esta es la página 'Acerca de' de mi aplicación.</h2>")