from django.urls import path

from .utils.empleados_views import (
    empleado_crear,
    empleado_editar,
    empleado_toggle_activo,
    empleados_view,
    exportar_sueldos_csv,
    pagar_sueldo,
)

urlpatterns = [
    path("empleados/", empleados_view, name="empleados"),
    path("empleados/crear/", empleado_crear, name="empleado_crear"),
    path("empleados/<int:empleado_id>/editar/", empleado_editar, name="empleado_editar"),
    path("empleados/<int:empleado_id>/pagar/", pagar_sueldo, name="pagar_sueldo"),
    path(
        "empleados/<int:empleado_id>/toggle/", empleado_toggle_activo, name="empleado_toggle_activo"
    ),
    path("empleados/exportar-sueldos/", exportar_sueldos_csv, name="exportar_sueldos_csv"),
]
