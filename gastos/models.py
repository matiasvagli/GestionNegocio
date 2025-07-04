# Create your models here.
from django.db import models


class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_ingreso = models.DateField(blank=True, null=True)
    cbu_cvu = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def ultimo_sueldo(self):
        """Último sueldo pagado a este empleado."""
        try:
            ultimo = (
                self.gasto_set.filter(tipo="sueldo", monto__isnull=False)
                .order_by("-fecha", "-id")
                .first()
            )
            # Verificar que el monto sea válido
            if ultimo and ultimo.monto is not None:
                return ultimo
        except Exception:
            pass
        return None

    def ultimo_aguinaldo(self):
        """Último aguinaldo pagado a este empleado."""
        try:
            ultimo = (
                self.gasto_set.filter(tipo="aguinaldo", monto__isnull=False)
                .order_by("-fecha", "-id")
                .first()
            )
            # Verificar que el monto sea válido
            if ultimo and ultimo.monto is not None:
                return ultimo
        except Exception:
            pass
        return None

    def total_sueldos(self):
        """Total de sueldos pagados a este empleado."""
        try:
            gastos = self.gasto_set.filter(tipo="sueldo", monto__isnull=False)
            return sum(g.monto for g in gastos if g.monto is not None)
        except Exception:
            return 0

    def total_otros_gastos(self):
        """Total de otros gastos (no sueldos) asociados a este empleado."""
        try:
            gastos = self.gasto_set.exclude(
                tipo="sueldo").filter(monto__isnull=False)
            return sum(g.monto for g in gastos if g.monto is not None)
        except Exception:
            return 0

    def total_gastos(self):
        """Total de todos los gastos asociados a este empleado."""
        try:
            gastos = self.gasto_set.filter(monto__isnull=False)
            return sum(g.monto for g in gastos if g.monto is not None)
        except Exception:
            return 0


class Gasto(models.Model):
    TIPO_CHOICES = [
        ("sueldo", "Sueldo"),
        ("aguinaldo", "Aguinaldo"),
        ("compra", "Compra"),
        ("servicio", "Servicio(luz, agua, etc.)"),
        ("alquiler", "Alquiler"),
        ("otro", "Otro"),
    ]
    empleado = models.ForeignKey(
        Empleado, on_delete=models.SET_NULL, blank=True, null=True)
    fecha = models.DateField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        if self.empleado:
            return f"{self.get_tipo_display()} - {self.empleado.nombre} - {self.monto}"
        return f"{self.get_tipo_display()} - {self.monto}"

    @classmethod
    def total_sueldos_pagados(cls, desde=None, hasta=None):
        qs = cls.objects.filter(tipo="sueldo", monto__isnull=False)
        if desde:
            qs = qs.filter(fecha__gte=desde)
        if hasta:
            qs = qs.filter(fecha__lte=hasta)
        try:
            return sum(g.monto for g in qs if g.monto is not None)
        except Exception:
            return 0

    @classmethod
    def total_otros_gastos(cls, desde=None, hasta=None):
        qs = cls.objects.exclude(tipo="sueldo").filter(monto__isnull=False)
        if desde:
            qs = qs.filter(fecha__gte=desde)
        if hasta:
            qs = qs.filter(fecha__lte=hasta)
        try:
            return sum(g.monto for g in qs if g.monto is not None)
        except Exception:
            return 0

    @classmethod
    def total_gastos_generales(cls, desde=None, hasta=None):
        """
        Calcula el total de todos los gastos generales, incluyendo sueldos y aguinaldos.
        """
        qs = cls.objects.filter(monto__isnull=False)
        if desde:
            qs = qs.filter(fecha__gte=desde)
        if hasta:
            qs = qs.filter(fecha__lte=hasta)
        try:
            return sum(g.monto for g in qs if g.monto is not None)
        except Exception:
            return 0

    @classmethod
    def total_gastos_mes(cls, year=None, month=None):
        from datetime import date

        hoy = date.today()
        if not year:
            year = hoy.year
        if not month:
            month = hoy.month
        qs = cls.objects.filter(
            fecha__year=year, fecha__month=month, monto__isnull=False)
        try:
            return sum(g.monto for g in qs if g.monto is not None)
        except Exception:
            return 0

    @classmethod
    def total_aguinaldos(cls, desde=None, hasta=None):
        """
        Calcula el total de aguinaldos pagados en un período.
        """
        qs = cls.objects.filter(tipo="aguinaldo", monto__isnull=False)
        if desde:
            qs = qs.filter(fecha__gte=desde)
        if hasta:
            qs = qs.filter(fecha__lte=hasta)
        try:
            return sum(g.monto for g in qs if g.monto is not None)
        except Exception:
            return 0
