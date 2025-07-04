import csv
import io
from decimal import Decimal

import pandas as pd
from django.db.models import Case, IntegerField, When
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from .forms_precios import ProductoHuevoPrecioForm
from .models import SUBCATEGORIAS, CATEGORIAS, ProductoHuevo, LineaVenta, Venta, Desperdicio
from .utils.dashboard_utils import (
    alerta_bajo_stock,
    ganancia_total_estimada,
    gasto_total_por_desperdicio_rango,
    stock_actual_en_cajones,
    stock_actual_en_docenas,
    stock_actual_en_maples,
    stock_actual_en_unidades,
    stock_actual_por_categoria,
    total_desechado,
    total_vendido_por_unidad_semana,
    valor_compra_stock_actual,
    valor_vendido,
    valor_vendido_hoy,
    valor_vendido_semana,
)
from .utils.informes import evolucion_precio_cajon_agrupado
from .utils.reportes_utils import (
    ganancia_huevos_rango,
    ganancia_otros_rango,
    ganancias_otros_diaria,
    ganancias_otros_semanal,
    ganancias_otros_mensual,
    ganancias_total_dia,
    ganancias_total_semana,
    ganancias_total_mes,
    gasto_mensual,
    resultado_mensual,
    valor_ganancia_diaria_huevos,
    valor_ganancia_mensual_huevos,
    valor_ganancia_semanal_huevos,
)
from .utils.stock_categoria_utils import get_stock_agrupado_y_cajones
from gastos.models import Gasto


# Nueva vista basada en clase para el dashboard
class DashboardView(TemplateView):
    template_name = "stock/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stock_agrupado = stock_actual_por_categoria()
        context.update(
            {
                "stock_unidades": stock_actual_en_unidades(),
                "stock_docenas": stock_actual_en_docenas(),
                "stock_maples": stock_actual_en_maples(),
                "stock_cajones": stock_actual_en_cajones(),
                "ganancia": ganancia_total_estimada(),
                "desperdicio": total_desechado(),
                "valor_stock": valor_compra_stock_actual(),
                "valor_vendido_semana": valor_vendido_semana(),
                "vendido_por_unidad": total_vendido_por_unidad_semana(),
                "valor_vendido": valor_vendido(),
                "valor_vendido_hoy": valor_vendido_hoy(),
                "alerta_bajo_stock": alerta_bajo_stock(stock_agrupado),
            }
        )
        return context


class StockPorCategoriaView(TemplateView):
    template_name = "stock/stock_por_categoria.html"

    def get_context_data(self, **kwargs):
        stock_agrupado, total_cajones = get_stock_agrupado_y_cajones()
        return {"stock_agrupado": stock_agrupado, "total_cajones": total_cajones}


# Alias para mantener rutas y firmas existentes
# dashboard y stock_por_categoria ahora apuntan a las CBV
dashboard = DashboardView.as_view()
stock_por_categoria = StockPorCategoriaView.as_view()


def reporte_ganancias_view(request):
    """Vista para el reporte de ganancias."""
    import calendar
    from datetime import date, datetime, timedelta

    rango = request.GET.get("rango", "mes")
    export = request.GET.get("export")
    hoy = date.today()
    # Años disponibles (últimos 5)
    anios = list(range(hoy.year, hoy.year - 5, -1))
    meses = [(i, calendar.month_name[i]) for i in range(1, 13)]
    semanas = list(range(1, 54))
    # Valores por defecto
    fecha = request.GET.get("fecha", hoy.strftime("%Y-%m-%d"))
    anio_mes = int(request.GET.get("anio_mes", hoy.year))
    mes = int(request.GET.get("mes", hoy.month))
    anio_semana = int(request.GET.get("anio_semana", hoy.year))
    semana = int(request.GET.get("semana", hoy.isocalendar()[1]))
    # Determinar rango de fechas
    if rango == "dia":
        inicio = fin = datetime.strptime(fecha, "%Y-%m-%d").date()
        ganancia_huevos = ganancia_huevos_rango(inicio, fin)
        ganancia_otros = ganancia_otros_rango(inicio, fin)
        total = ganancia_huevos + ganancia_otros
    elif rango == "semana":
        inicio = datetime.strptime(
            f"{anio_semana}-W{semana}-1", "%G-W%V-%u").date()
        fin = inicio + timedelta(days=6)
        ganancia_huevos = ganancia_huevos_rango(inicio, fin)
        ganancia_otros = ganancia_otros_rango(inicio, fin)
        total = ganancia_huevos + ganancia_otros
    elif rango == "mes_anterior":
        mes_anterior = hoy.month - 1 if hoy.month > 1 else 12
        anio_mes_anterior = hoy.year if hoy.month > 1 else hoy.year - 1
        inicio = date(anio_mes_anterior, mes_anterior, 1)
        fin = date(anio_mes_anterior, mes_anterior,
                   calendar.monthrange(anio_mes_anterior, mes_anterior)[1])
        ganancia_huevos = ganancia_huevos_rango(inicio, fin)
        ganancia_otros = ganancia_otros_rango(inicio, fin)
        total = ganancia_huevos + ganancia_otros

        # Calcular gastos del mes anterior
        gastos_generales = Gasto.total_gastos_mes(
            anio_mes_anterior, mes_anterior)
        gastos_desperdicios = Decimal(
            gasto_total_por_desperdicio_rango(inicio, fin))
        gastos_rango = Decimal(gastos_generales) + gastos_desperdicios
        ganancia_neta = Decimal(total) - gastos_rango
        # Convertir total a Decimal para evitar errores de tipo
        total = Decimal(total)
        contexto = {
            "ganancia_huevos": ganancia_huevos,
            "ganancia_otros": ganancia_otros,
            "total_ganancia": total,
            "gastos_generales": gastos_generales,
            "gastos_desperdicios": gastos_desperdicios,
            "gastos_rango": gastos_rango,
            "ganancia_neta": ganancia_neta,
            "fecha_inicio": inicio,
            "fecha_fin": fin,
        }
        # Agregar variables de diagnóstico
        contexto.pop("diagnostico_aguinaldos", None)
        contexto.pop("gastos_generales_orig", None)
        contexto.pop("aguinaldos_valor", None)
        contexto.pop("total_sin_aguinaldos", None)
        return render(request, "stock/reporte_ganancias.html", contexto)
    else:
        inicio = date(anio_mes, mes, 1)
        fin = date(anio_mes, mes, calendar.monthrange(anio_mes, mes)[1])
        ganancia_huevos = ganancia_huevos_rango(inicio, fin)
        ganancia_otros = ganancia_otros_rango(inicio, fin)
        total = ganancia_huevos + ganancia_otros
    # Calcular gastos en el rango seleccionado y ganancia neta como floats
    # Vamos a calcular los gastos generales utilizando ambos métodos
    # para garantizar consistencia con el cálculo del gasto_mensual()

    # Método 1: Calculando todos los gastos con total_gastos_generales
    gastos_generales_metodo1 = float(Gasto.total_gastos_generales(inicio, fin))

    # Método 2: Calculando separadamente y sumando
    gastos_sin_aguinaldos = Gasto.objects.exclude(tipo="aguinaldo").filter(
        fecha__gte=inicio, fecha__lte=fin, monto__isnull=False
    )
    total_sin_aguinaldos = float(sum(
        g.monto for g in gastos_sin_aguinaldos if g.monto is not None))

    # Calcular aguinaldos directamente
    aguinaldos = float(Gasto.total_aguinaldos(inicio, fin))

    # Combinar para asegurar que todos los gastos estén incluidos
    gastos_generales_metodo2 = total_sin_aguinaldos + aguinaldos

    # Guardar el valor original para diagnóstico
    gastos_generales_orig = gastos_generales_metodo1

    # Elegir el valor más alto para los gastos generales
    # gastos_generales = max(gastos_generales_metodo1, gastos_generales_metodo2)

    # CORRECCIÓN: Calcular gastos generales usando el rango seleccionado
    gastos_generales = Decimal(Gasto.total_gastos_generales(inicio, fin))
    gastos_desperdicios = Decimal(
        gasto_total_por_desperdicio_rango(inicio, fin))
    gastos_rango = gastos_generales + gastos_desperdicios
    # Convertir total a Decimal para evitar errores de tipo
    total = Decimal(total)
    ganancia_neta = Decimal(total) - gastos_rango

    # No necesitamos guardar estas variables en nuevas variables,
    # pero asegurémonos de pasarlas al contexto correctamente

    if export == "csv":
        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"] = f'attachment; filename="reporte_ganancias_{rango}.csv"'
        writer = csv.writer(response)
        writer.writerow([
            "Rango", "Desde", "Hasta", "Ganancia Huevos",
            "Ganancia Otros", "Gastos Generales",
            "Gastos Desperdicios", "Total Gastos", "Ganancia Neta"
        ])
        writer.writerow([
            rango,
            inicio.strftime("%d/%m/%Y"),
            fin.strftime("%d/%m/%Y"),
            f"{ganancia_huevos:.2f}",
            f"{ganancia_otros:.2f}",
            f"{gastos_generales:.2f}",
            f"{gastos_desperdicios:.2f}",
            f"{gastos_rango:.2f}",
            f"{ganancia_neta:.2f}",
        ])
        return response
    contexto = {
        "ganancia_diaria": valor_ganancia_diaria_huevos(),
        "ganancia_otros_diaria": ganancias_otros_diaria(),
        "total_ganancia_diaria": ganancias_total_dia(),
        "ganancia_semanal": valor_ganancia_semanal_huevos(),
        "ganancia_otros_semanal": ganancias_otros_semanal(),
        "total_ganancia_semanal": ganancias_total_semana(),
        "ganancia_mensual": valor_ganancia_mensual_huevos(),
        "ganancia_otros_mensual": ganancias_otros_mensual(),
        "total_ganancia_mensual": ganancias_total_mes(),
        "resultado_mes": resultado_mensual(),
        "gasto_mensual": gasto_mensual(),
        "rango": rango,
        "anios": anios,
        "meses": meses,
        "semanas": semanas,
        "anio_mes": anio_mes,
        "mes": mes,
        "anio_semana": anio_semana,
        "semana": semana,
        "fecha": fecha,
        # Variables para la tabla de detalle del rango seleccionado
        "ganancia_huevos": ganancia_huevos,
        "ganancia_otros": ganancia_otros,
        "total_ganancia": total,
        "gastos_generales": gastos_generales,
        "gastos_desperdicios": gastos_desperdicios,
        "gastos_rango": gastos_rango,
        "ganancia_neta": ganancia_neta,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
        # Eliminación de variables de diagnóstico
        "diagnostico_aguinaldos": None,
        "gastos_generales_orig": None,
        "aguinaldos_valor": None,
        "total_sin_aguinaldos": None,
    }
    # Ajustar el contexto para no incluir información de diagnóstico
    contexto.pop("diagnostico_aguinaldos", None)
    contexto.pop("gastos_generales_orig", None)
    contexto.pop("aguinaldos_valor", None)
    contexto.pop("total_sin_aguinaldos", None)
    return render(request, "stock/reporte_ganancias.html", contexto)


def precios_referencia_editar(request):
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
    productos = (
        ProductoHuevo.objects.all().annotate(
            _orden=orden_subcat).order_by("categoria", "_orden")
    )
    if request.method == "POST":
        for p in productos:
            form = ProductoHuevoPrecioForm(
                request.POST, instance=p, prefix=str(p.pk))
            if form.is_valid():
                form.save()
        # Redirige a la página de precios de referencia
        return redirect("precios_referencia")
    else:
        forms_list = [ProductoHuevoPrecioForm(
            instance=p, prefix=str(p.pk)) for p in productos]
    return render(
        request,
        "stock/precios_referencia_editar.html",
        {
            "forms_list": forms_list,
            "productos": productos,
        },
    )


def eliminar_ultimo_ticket(request):
    """
    Elimina la última venta registrada (por fecha más reciente).
    Redirige al listado de ventas después de eliminar.
    """
    from django.shortcuts import redirect

    from .models import Venta

    ultima_venta = Venta.objects.order_by("-fecha", "-pk").first()
    if ultima_venta:
        ultima_venta.delete()
    return redirect("ingreso_venta")


def reporte_evolucion_precio_cajon(request, *args, **kwargs):
    agrupamiento = request.GET.get("agrupamiento", "dia")
    export = request.GET.get("export")
    data, fechas = evolucion_precio_cajon_agrupado(agrupamiento)
    categorias = ["blancos", "color"]
    subcategorias = [s[0] for s in SUBCATEGORIAS]
    tablas = {}
    for cat in categorias:
        filas = []
        for subcat in subcategorias:
            key = (cat, subcat)
            precios = [data.get(key, {}).get(f, None) for f in fechas]
            filas.append({"subcategoria": subcat, "precios": precios})
        tablas[cat] = filas
    if export == "excel":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            for cat in categorias:
                # Ordenar filas por subcategoría según el orden definido
                filas_ordenadas = [fila for fila in tablas[cat]]
                # Construir DataFrame con columnas: Categoría, Subcategoría, fechas...
                data_rows = []
                for fila in filas_ordenadas:
                    row = [cat.title(), fila["subcategoria"]]
                    row.extend(fila["precios"])
                    data_rows.append(row)
                columns = ["Categoría", "Subcategoría"] + \
                    [f.strftime("%d/%m/%Y") for f in fechas]
                df = pd.DataFrame(data_rows, columns=columns)
                # Exportar el DataFrame sin aplicar estilos personalizados
                df.to_excel(
                    writer, sheet_name=f"Huevos {cat.title()}", index=False
                )
        output.seek(0)
        response = HttpResponse(
            output.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = "attachment; filename=evolucion_precio_cajon.xlsx"
        return response
    contexto = {
        "tablas": tablas,
        "fechas": fechas,
        "subcategorias": subcategorias,
        "agrupamiento": agrupamiento,
    }
    return render(request, "stock/evolucion_precio_cajon.html", contexto)


def gastos_ingreso(request):
    from decimal import Decimal, InvalidOperation

    from django.utils import timezone

    mensaje = None
    GASTO_TIPOS = Gasto.TIPO_CHOICES
    if request.method == "POST":
        tipo = request.POST.get("tipo")
        descripcion = request.POST.get("descripcion")
        monto_raw = request.POST.get("monto")
        categoria = request.POST.get("categoria")
        subcategoria = request.POST.get("subcategoria")
        hoy = timezone.now().date()

        # Limpiar y validar el monto
        try:
            if monto_raw:
                # Remover espacios y caracteres no numéricos excepto punto y coma
                monto_cleaned = monto_raw.strip().replace(" ", "").replace("$", "")

                # Reemplazar coma por punto para decimales
                if "," in monto_cleaned and "." in monto_cleaned:
                    # Si tiene ambos, asumir que . es separador de miles y , es decimal
                    parts = monto_cleaned.split(",")
                    if len(parts) == 2 and len(parts[1]) <= 2:
                        monto_cleaned = monto_cleaned.replace(
                            ".", "").replace(",", ".")
                    else:
                        monto_cleaned = monto_cleaned.replace(",", "")
                elif "," in monto_cleaned:
                    # Solo coma, puede ser decimal
                    parts = monto_cleaned.split(",")
                    if len(parts) == 2 and len(parts[1]) <= 2:
                        monto_cleaned = monto_cleaned.replace(",", ".")
                    else:
                        monto_cleaned = monto_cleaned.replace(",", "")

                monto = Decimal(monto_cleaned)
            else:
                monto = None

        except (InvalidOperation, ValueError):
            mensaje = "Error: Ingrese un monto válido. Ejemplo: 5000 o 1500000.50"
            return render(
                request,
                "stock/gastos_ingreso.html",
                {
                    "mensaje": mensaje,
                    "gasto_tipos": GASTO_TIPOS,
                    "categorias": CATEGORIAS,
                    "subcategorias": SUBCATEGORIAS,
                },
            )

        if tipo == "gasto" and monto:
            Gasto.objects.create(fecha=hoy, monto=monto, tipo=descripcion)
            mensaje = "Gasto registrado correctamente."
        elif tipo == "desperdicio" and monto:
            Desperdicio.objects.create(
                fecha=hoy,
                cantidad=monto,
                motivo="Desperdicio",
                categoria=categoria,
                subcategoria=subcategoria,
            )
            mensaje = "Desperdicio registrado correctamente."
        else:
            mensaje = "Error: Debe ingresar un monto válido."

    return render(
        request,
        "stock/gastos_ingreso.html",
        {
            "mensaje": mensaje,
            "gasto_tipos": GASTO_TIPOS,
            "categorias": CATEGORIAS,
            "subcategorias": SUBCATEGORIAS,
        },
    )
