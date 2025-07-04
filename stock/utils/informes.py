from collections import defaultdict

from django.db.models import Max
from django.db.models.functions import TruncDay, TruncMonth, TruncWeek

from stock.models import SUBCATEGORIAS, Compra


def evolucion_precio_cajon(categoria, subcategoria):
    compras = Compra.objects.filter(
        categoria=categoria, subcategoria=subcategoria, unidad="cajon"
    ).order_by("fecha")
    return [(c.fecha, c.precio_unitario) for c in compras]


def evolucion_precio_cajon_todas():
    """Devuelve un dict: {(categoria, subcategoria): {fecha: precio}} y lista de fechas ordenadas."""
    compras = Compra.objects.filter(unidad="cajon").order_by("fecha")
    data = defaultdict(dict)
    fechas_set = set()
    for c in compras:
        key = (c.categoria, c.subcategoria)
        data[key][c.fecha] = c.precio_unitario
        fechas_set.add(c.fecha)
    fechas = sorted(fechas_set)
    return data, fechas


def evolucion_precio_cajon_agrupado(agrupamiento="dia"):
    """Devuelve data, fechas según agrupamiento: dia (máx 7), semana, mes. Toma el último precio de compra de cada periodo."""
    if agrupamiento == "semana":
        trunc = TruncWeek("fecha")
        max_fechas = 12
    elif agrupamiento == "mes":
        trunc = TruncMonth("fecha")
        max_fechas = None
    else:
        trunc = TruncDay("fecha")
        max_fechas = 7
    qs = Compra.objects.filter(unidad="cajon").annotate(periodo=trunc)
    data = defaultdict(dict)
    fechas_set = set()
    for cat in ["blancos", "color"]:
        for subcat, _ in SUBCATEGORIAS:
            compras = qs.filter(categoria=cat, subcategoria=subcat)
            # Agrupar por periodo y tomar la compra con la fecha más reciente
            periodos = compras.values("periodo").annotate(ult_fecha=Max("fecha"))
            for p in periodos:
                ult = (
                    compras.filter(periodo=p["periodo"], fecha=p["ult_fecha"])
                    .order_by("-id")
                    .first()
                )
                if ult:
                    data[(cat, subcat)][p["periodo"]] = ult.precio_unitario
                    fechas_set.add(p["periodo"])
    fechas = sorted(fechas_set)
    if max_fechas:
        fechas = fechas[-max_fechas:]
    return data, fechas
