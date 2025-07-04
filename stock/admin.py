from django.contrib import admin

from .models import Compra, Desperdicio, ProductoHuevo, Venta, LineaVenta

# Inline para mostrar líneas de venta en el detalle de Venta


class LineaVentaInline(admin.TabularInline):
    model = LineaVenta
    extra = 0

# Configuración personalizada del admin para Venta


class VentaAdmin(admin.ModelAdmin):
    inlines = [LineaVentaInline]
    list_display = ('id', 'fecha', 'importe_total', 'facturada')


admin.site.register(Compra)
admin.site.register(Venta, VentaAdmin)
admin.site.register(Desperdicio)
admin.site.register(ProductoHuevo)


# Register your models here.
