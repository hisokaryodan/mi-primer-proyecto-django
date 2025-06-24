# mi_app_web/views.py

from django.shortcuts import render
from django.http import HttpResponse
from data_loader.models import MonthlyRecyclingData # <-- ¡CORREGIDO AQUÍ! Ahora importa MonthlyRecyclingData
from django.contrib.auth.models import User # Necesitamos el modelo User para el filtro de empresas
import collections # Importar collections para defaultdict

def vista_hola_mundo(request):
    return HttpResponse("<h1>¡Hola, soy tu primera vista en Django!</h1>")

def vista_acerca_de(request):
    return HttpResponse("<h2>Esta es la página 'Acerca de' de mi aplicación.</h2>")

def dashboard_graficos(request):
    # Obtener el ID del usuario/empresa desde el parámetro de la URL si existe
    selected_company_id = request.GET.get('company_id')

    # Obtener todas las empresas/usuarios para el filtro en el dashboard
    all_companies = User.objects.all().order_by('username')

    # Base de la consulta para los datos de reciclaje
    recycling_data_query = MonthlyRecyclingData.objects.all()

    # Si se seleccionó una empresa, filtramos los datos por ese usuario
    if selected_company_id:
        try:
            selected_company_id = int(selected_company_id)
            recycling_data_query = recycling_data_query.filter(user_id=selected_company_id)
        except ValueError:
            selected_company_id = None
            pass

    # Obtener los datos de reciclaje finales (filtrados o todos)
    recycling_data_from_db = recycling_data_query.order_by('year', 'material_type')

    # --- Prepara los datos para los gráficos ---

    # Gráfico de Barras: Cantidad de Material Reciclado por Tipo (sumando todos los años)
    # Usamos defaultdict para agrupar y sumar fácilmente
    amount_recycled_by_material = collections.defaultdict(float) # Cambiado a float para precisión
    
    for data in recycling_data_from_db:
        amount_recycled_by_material[data.material_type] += data.amount_recycled

    # Obtener etiquetas y datos ordenados alfabéticamente por tipo de material
    material_types = sorted(amount_recycled_by_material.keys())
    material_data = [amount_recycled_by_material[mt] for mt in material_types]

    # Gráfico de Torta: Distribución de Materiales Reciclados (Proporción de cada material)
    total_recycled = sum(material_data)
    if total_recycled > 0:
        material_percentages = [(amount / total_recycled) * 100 for amount in material_data]
    else:
        material_percentages = []

    # Gráfico de Líneas (Mantenemos los datos de ejemplo por ahora, ya que el modelo actual
    # no está optimizado para un "crecimiento de usuarios" directamente, sino por reciclaje.
    # Si quieres datos DB para líneas, necesitaríamos una lógica de agrupación de tiempo.)
    usuarios_fechas = ['2023-01', '2023-03', '2023-05', '2023-07', '2023-09', '2023-11', '2024-01']
    usuarios_cantidad = [100, 120, 150, 130, 180, 200, 250]


    context = {
        'titulo_pagina': 'Dashboard de Reciclaje',
        'bar_labels': material_types,
        'bar_data': material_data,
        'pie_labels': material_types,
        'pie_data': material_percentages,
        'line_labels': usuarios_fechas,
        'line_data': usuarios_cantidad,
        'all_companies': all_companies,
        'selected_company_id': selected_company_id,
    }
    return render(request, 'mi_app_web/dashboard.html', context)
