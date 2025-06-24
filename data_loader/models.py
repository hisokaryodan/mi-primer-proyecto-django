# data_loader/models.py

from django.db import models
from django.contrib.auth.models import User # Importamos el modelo User de Django

class MonthlyRecyclingData(models.Model):
    """
    Modelo para almacenar datos de reciclaje mensuales por empresa (usuario).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Empresa")
    year = models.IntegerField(verbose_name="Año")
    month_name = models.CharField(max_length=20, verbose_name="Mes") # Ej: Enero, Febrero
    material_type = models.CharField(max_length=100, verbose_name="Tipo de Material") # Ej: Plástico, Papel, Vidrio
    amount_recycled = models.FloatField(verbose_name="Cantidad Reciclada (kg)") # Puede ser flotante para precisión
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        # Los datos se ordenarán por empresa, luego por año y tipo de material.
        # Puedes cambiar 'year' y 'month_name' a un campo de fecha si tu CSV tiene fecha completa.
        ordering = ['user__username', 'year', 'month_name', 'material_type']
        verbose_name = "Dato de Reciclaje Mensual"
        verbose_name_plural = "Datos de Reciclaje Mensuales"
        # Opcional: Asegurar que una empresa no suba el mismo tipo de material para el mismo mes/año
        unique_together = ('user', 'year', 'month_name', 'material_type') 

    def __str__(self):
        return f"{self.user.username} - {self.material_type} ({self.month_name} {self.year}): {self.amount_recycled} kg"