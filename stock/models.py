# Create your models here.
from django.db import models

UNIDADES_COMPRA = [
    ("docena", "Docena"),
    ("maple", "Maple"),
    ("cajon", "Cajón"),
]

UNIDADES_VENTA = [
    ("cajon", "Cajón"),
    ("maple", "Maple"),
    ("docena", "Docena"),
]

CATEGORIAS = [
    (
        "blancos",
        "Blancos",
    ),
    ("color", "Color"),
    ("otros", "Otros"),
]
SUBCATEGORIAS = [
    ("E", "E"),
    ("1", "1"),
    ("2", "2"),
    ("M", "M"),
    ("3", "3"),
    ("4", "4"),
    ("S", "S"),
    ("R", "R"),
]


class ProductoHuevo(models.Model):
    fecha_creacion = models.DateField(auto_now_add=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIAS)
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # Eliminado precio_venta, solo quedan los tentativos
    precio_tentativo_cajon = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    precio_tentativo_medio_cajon = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    precio_tentativo_3maples = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    precio_tentativo_maple = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    activo = models.BooleanField(default=True)

    def __str__(self):
        cat = dict(CATEGORIAS).get(self.categoria, self.categoria)
        subcat = dict(SUBCATEGORIAS).get(self.subcategoria, self.subcategoria)
        return f"{cat} {subcat}"


class Compra(models.Model):
    fecha = models.DateField()
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    unidad = models.CharField(max_length=10, choices=UNIDADES_COMPRA)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIAS)

    def total_unidades(self):
        from decimal import Decimal

        if self.unidad == "cajon":
            return self.cantidad * Decimal("360")
        elif self.unidad == "maple":
            return self.cantidad * Decimal("30")
        elif self.unidad == "docena":
            return self.cantidad * Decimal("12")
        return self.cantidad

    def __str__(self):
        return f"Compra {self.cantidad} {self.unidad} - {self.fecha}"


class Venta(models.Model):
    fecha = models.DateField()
    importe_total = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    facturada = models.BooleanField(default=False)

    def __str__(self):
        return f"Venta #{self.pk} - {self.fecha} - ${self.importe_total}"


class LineaVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="lineas")
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIAS, blank=True, null=True)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    unidad = models.CharField(max_length=10, choices=UNIDADES_VENTA, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def total_unidades(self):
        from decimal import Decimal

        if not self.cantidad or not self.unidad:
            return 0
        if self.unidad == "docena":
            return self.cantidad * Decimal("12")
        elif self.unidad == "maple":
            return self.cantidad * Decimal("30")
        elif self.unidad == "cajon":
            return self.cantidad * Decimal("360")
        return self.cantidad

    def __str__(self):
        cat = dict(CATEGORIAS).get(self.categoria, self.categoria)
        subcat = dict(SUBCATEGORIAS).get(self.subcategoria or "", self.subcategoria or "")
        if self.cantidad and self.unidad:
            return f"{self.cantidad} {self.unidad} {cat} {subcat or ''}"
        else:
            return f"Otros productos - {cat}"


class Desperdicio(models.Model):
    fecha = models.DateField()
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    motivo = models.CharField(max_length=100, blank=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    subcategoria = models.CharField(max_length=2, choices=SUBCATEGORIAS)

    def __str__(self):
        return f"Desperdicio {self.cantidad} huevos - {self.fecha}"
