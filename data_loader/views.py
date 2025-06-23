# data_loader/views.py

import csv
from io import TextIOWrapper # Para leer el archivo cargado como texto
from django.shortcuts import render, redirect
from django.contrib import messages # Para mostrar mensajes de éxito/error en la plantilla
from django.urls import reverse # Para construir URLs dinámicamente

from .forms import CSVUploadForm
from .models import MonthlySalesData

def upload_csv_view(request):
    """
    Vista para manejar la carga de archivos CSV.
    - GET: Muestra el formulario de carga.
    - POST: Procesa el archivo CSV, guarda los datos en la base de datos
            y redirige al dashboard.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtiene el archivo CSV de la solicitud
            csv_file = request.FILES['csv_file']

            # Verifica si el archivo es CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'El archivo debe ser un CSV (.csv).')
                return render(request, 'data_loader/upload.html', {'form': form})

            # Usa TextIOWrapper para leer el archivo binario como texto
            # Asegúrate de la codificación correcta, 'utf-8' es común.
            file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.reader(file_data)

            # Opcional: Saltar la fila de encabezados si tu CSV tiene una
            try:
                header = next(reader)
                # Puedes validar el encabezado aquí si quieres, ej:
                # if header[0] != 'month' or header[1] != 'sales':
                #     messages.error(request, "Encabezados CSV incorrectos. Se esperan 'month,sales'.")
                #     return render(request, 'data_loader/upload.html', {'form': form})
            except StopIteration:
                messages.error(request, "El archivo CSV está vacío.")
                return render(request, 'data_loader/upload.html', {'form': form})


            # Opcional: Eliminar datos existentes para simplicidad antes de cargar nuevos
            # Esto es útil si cada carga reemplaza los datos anteriores.
            # Si necesitas añadir incrementalmente, remueve esta línea y añade lógica de actualización/creación.
            MonthlySalesData.objects.all().delete()
            
            rows_processed = 0
            errors_found = False

            for row in reader:
                if len(row) >= 2: # Asegura que la fila tiene al menos 2 columnas
                    try:
                        month_data = row[0]
                        sales_data = int(row[1])
                        
                        # Crea una nueva instancia del modelo y la guarda en la base de datos
                        MonthlySalesData.objects.create(month=month_data, sales=sales_data)
                        rows_processed += 1
                    except ValueError:
                        messages.error(request, f"Error de formato en fila '{row}': 'sales' debe ser un número entero.")
                        errors_found = True
                        break # O continúa procesando si prefieres guardar filas válidas
                    except Exception as e: # Captura cualquier otro error durante la creación
                        messages.error(request, f"Error al procesar fila '{row}': {e}")
                        errors_found = True
                        break
                else:
                    messages.warning(request, f"Fila omitida por formato incorrecto (menos de 2 columnas): {row}")
                    
            if not errors_found:
                messages.success(request, f"¡CSV cargado exitosamente! {rows_processed} filas procesadas.")
                # Redirige al dashboard después de una carga exitosa
                return redirect(reverse('dashboard_graficos'))
            else:
                messages.error(request, "La carga del CSV ha fallado debido a errores.")

        else:
            # Si el formulario no es válido, muestra los errores
            messages.error(request, "Por favor, corrige los errores del formulario.")
    else:
        # Si es una solicitud GET, muestra el formulario vacío
        form = CSVUploadForm()
    
    return render(request, 'data_loader/upload.html', {'form': form})

