from django.urls import path

from .utils.compras_utils import ingreso_compra
from .utils.precios_referencia_utils import precios_referencia
from .utils.ventas_utils import ingreso_venta

# Importa todas las vistas de stock/views.py en una sola línea
from .views import (
    dashboard,
    eliminar_ultimo_ticket,
    gastos_ingreso,
    precios_referencia_editar,
    reporte_evolucion_precio_cajon,
    reporte_ganancias_view,
    stock_por_categoria,
)

urlpatterns = [
    # ahora la raíz muestra el dashboard
    path("", dashboard, name="dashboard"),
    path("dashboard/", dashboard, name="dashboard"),
    path("stock_por_categoria/", stock_por_categoria, name="stock_por_categoria"),
    path("ingreso_venta/", ingreso_venta, name="ingreso_venta"),
    path("ingreso_compra/", ingreso_compra, name="ingreso_compra"),
    path("precios_referencia/", precios_referencia, name="precios_referencia"),
    path("precios_referencia/editar/", precios_referencia_editar, name="precios_referencia_editar"),
    path("reporte_ganancias/", reporte_ganancias_view, name="reporte_ganancias"),
    path("eliminar_ultimo_ticket/", eliminar_ultimo_ticket, name="eliminar_ultimo_ticket"),
    path(
        "reporte_evolucion_precio_cajon/",
        reporte_evolucion_precio_cajon,
        name="reporte_evolucion_precio_cajon",
    ),
    path(
        "reporte_evolucion_precio_cajon/<str:categoria>/<str:subcategoria>/",
        reporte_evolucion_precio_cajon,
        name="reporte_evolucion_precio_cajon_param",
    ),
    path("gastos_ingreso/", gastos_ingreso, name="gastos_ingreso"),
]
