from django.urls import path

from . import views

urlpatterns = [
    path("", views.admin_login, name="admin_login"),
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("empleados/", views.admin_empleados, name="admin_empleados"),
    path("reportes/", views.admin_reportes, name="admin_reportes"),
]
