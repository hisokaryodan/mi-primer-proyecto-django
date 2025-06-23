# data_loader/forms.py

from django import forms

class CSVUploadForm(forms.Form):
    """
    Formulario simple para cargar un archivo CSV.
    """
    csv_file = forms.FileField(label='Selecciona un archivo CSV',
                               help_text='El archivo debe contener columnas como "month" y "sales".')