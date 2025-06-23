# data_loader/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_csv_view, name='upload_csv'), # URL para la carga de CSV
]