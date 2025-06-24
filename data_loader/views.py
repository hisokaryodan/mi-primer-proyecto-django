# data_loader/views.py

import csv
from io import TextIOWrapper # Para leer el archivo cargado como texto
from django.shortcuts import render, redirect
from django.contrib import messages # Para mostrar mensajes de éxito/error en la plantilla
from django.urls import reverse # Para construir URLs dinámicamente
from django.contrib.auth.decorators import login_required # Importamos el decorador

from .forms import CSVUploadForm
from .models import MonthlyRecyclingData # <-- ¡CORREGIDO! Ahora importa MonthlyRecyclingData


@login_required # Esto asegura que solo usuarios logeados puedan acceder a esta vista
def upload_csv_view(request):
    """
    Vista para manejar la carga de archivos CSV de datos de reciclaje.
    Asocia los datos con el usuario logeado.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'El archivo debe ser un CSV (.csv).')
                return render(request, 'data_loader/upload.html', {'form': form})

            file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.reader(file_data)

            try:
                # Se espera que el encabezado sea: year,month_name,material_type,amount_recycled
                header = [h.strip() for h in next(reader)] # Limpiar espacios en blanco
                expected_header = ['year', 'month_name', 'material_type', 'amount_recycled']
                if header != expected_header:
                    messages.error(request, f"Encabezados CSV incorrectos. Se esperan: {', '.join(expected_header)}")
                    return render(request, 'data_loader/upload.html', {'form': form})
            except StopIteration:
                messages.error(request, "El archivo CSV está vacío.")
                return render(request, 'data_loader/upload.html', {'form': form})

            # Opcional: Eliminar datos existentes para el usuario logeado antes de cargar nuevos
            MonthlyRecyclingData.objects.filter(user=request.user).delete()
            
            rows_processed = 0
            errors_found = False

            for row in reader:
                if len(row) == 4: # Asegura que la fila tiene las 4 columnas esperadas
                    try:
                        year = int(row[0])
                        month_name = row[1]
                        material_type = row[2]
                        amount_recycled = float(row[3])
                        
                        MonthlyRecyclingData.objects.create(
                            user=request.user,
                            year=year,
                            month_name=month_name,
                            material_type=material_type,
                            amount_recycled=amount_recycled
                        )
                        rows_processed += 1
                    except ValueError:
                        messages.error(request, f"Error de formato en fila '{row}': 'year' o 'amount_recycled' tienen formato incorrecto.")
                        errors_found = True
                        break
                    except Exception as e:
                        messages.error(request, f"Error al procesar fila '{row}': {e}")
                        errors_found = True
                        break
                else:
                    messages.warning(request, f"Fila omitida por formato incorrecto (se esperan 4 columnas): {row}")
                    
            if not errors_found:
                messages.success(request, f"¡CSV de reciclaje cargado exitosamente! {rows_processed} filas procesadas para {request.user.username}.")
                return redirect(reverse('dashboard_graficos'))
            else:
                messages.error(request, "La carga del CSV ha fallado debido a errores.")

        else:
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        form = CSVUploadForm()
    
    return render(request, 'data_loader/upload.html', {'form': form})

