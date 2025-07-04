# Este módulo debe contener solo funciones utilitarias de datos para precios de referencia.


from django.db.models import Case, IntegerField, When
from django.shortcuts import render

from stock.models import ProductoHuevo


def precios_referencia(request):
    orden_subcat = Case(
        When(subcategoria="E", then=0),
        When(subcategoria="1", then=1),
        When(subcategoria="2", then=2),
        When(subcategoria="M", then=3),
        When(subcategoria="3", then=4),
        When(subcategoria="4", then=5),
        When(subcategoria="S", then=6),
        When(subcategoria="R", then=7),
        default=8,
        output_field=IntegerField(),
    )
    productos_blancos = (
        ProductoHuevo.objects.filter(categoria="blancos")
        .annotate(_orden=orden_subcat)
        .order_by("_orden")
    )
    productos_color = (
        ProductoHuevo.objects.filter(categoria="color")
        .annotate(_orden=orden_subcat)
        .order_by("_orden")
    )
    return render(
        request,
        "stock/precios_referencia.html",
        {"productos_blancos": productos_blancos,
            "productos_color": productos_color},
    )
