# mi_app_web/views.py

from django.shortcuts import render
from django.http import HttpResponse
from data_loader.models import MonthlySalesData # <-- ¡Importa tu nuevo modelo!

def vista_hola_mundo(request):
    return HttpResponse("<h1>¡Hola, soy tu primera vista en Django!</h1>")

def vista_acerca_de(request):
    return HttpResponse("<h2>Esta es la página 'Acerca de' de mi aplicación.</h2>")

def dashboard_graficos(request):
    # NUEVO: Obtener datos de ventas desde la base de datos
    # Ordena por el campo 'month' o 'id' para asegurar un orden consistente
    sales_data_from_db = MonthlySalesData.objects.all().order_by('id') # Ordena por ID

    # Prepara los datos para el gráfico de barras de Chart.js
    ventas_meses = [data.month for data in sales_data_from_db]
    ventas_valores = [data.sales for data in sales_data_from_db]

    # Mantenemos los datos de ejemplo para otros gráficos que no están conectados a la DB aún
    productos_nombres = ['Laptop', 'Mouse', 'Teclado', 'Monitor']
    productos_porcentajes = [40, 20, 25, 15]

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
