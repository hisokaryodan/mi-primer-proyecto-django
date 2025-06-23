
from django.db import models

class MonthlySalesData(models.Model):
    """
    Modelo para almacenar datos de ventas mensuales.
    Se asume que el CSV tendrá columnas 'month' y 'sales'.
    """
    month = models.CharField(max_length=50, unique=True, verbose_name="Mes")
    sales = models.IntegerField(verbose_name="Ventas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        # Ordena los datos por la fecha de creación.
        # Puedes cambiar esto a ['month'] si tus meses son ordenables alfabéticamente
        # o añadir un campo de fecha para un ordenamiento cronológico.
        ordering = ['created_at']
        verbose_name = "Dato de Venta Mensual"
        verbose_name_plural = "Datos de Ventas Mensuales"

    def __str__(self):
        return f"{self.month}: {self.sales}"