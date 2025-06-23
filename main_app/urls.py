# main_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'), # La URL raíz de esta app
]