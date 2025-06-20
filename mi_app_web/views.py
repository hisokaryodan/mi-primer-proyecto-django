# mi_app_web/views.py

from django.shortcuts import render
from django.http import HttpResponse

def vista_hola_mundo(request):
    return HttpResponse("<h1>¡Hola, soy tu primera vista en Django!</h1>")

def vista_acerca_de(request):
    return HttpResponse("<h2>Esta es la página 'Acerca de' de mi aplicación.</h2>")

def dashboard_graficos(request):
    # Datos de ejemplo para el gráfico de barras (Ventas por Mes)
    ventas_meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
    ventas_valores = [1200, 1900, 3000, 5000, 2300, 4000]

    # Datos de ejemplo para el gráfico de torta (Distribución de Productos)
    productos_nombres = ['Laptop', 'Mouse', 'Teclado', 'Monitor']
    productos_porcentajes = [40, 20, 25, 15] # Asegúrate de que sumen 100 o ajusta los valores

    # Datos de ejemplo para un gráfico de líneas (Crecimiento de Usuarios)
    usuarios_fechas = ['2023-01', '2023-03', '2023-05', '2023-07', '2023-09', '2023-11', '2024-01']
    usuarios_cantidad = [100, 120, 150, 130, 180, 200, 250]


    context = {
        'ventas_meses': ventas_meses,
        'ventas_valores': ventas_valores,
        'productos_nombres': productos_nombres,
        'productos_porcentajes': productos_porcentajes,
        'usuarios_fechas': usuarios_fechas,
        'usuarios_cantidad': usuarios_cantidad,
        'titulo_pagina': 'Dashboard de Gráficos',
    }
    return render(request, 'mi_app_web/dashboard.html', context)