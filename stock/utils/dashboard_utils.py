from decimal import Decimal


from stock.models import Compra, Desperdicio, LineaVenta, Venta


def stock_actual_en_unidades():
    compradas = sum(c.total_unidades() for c in Compra.objects.all())
    vendidas = sum(l.total_unidades() for l in LineaVenta.objects.all())
    desperdiciadas = sum(d.cantidad for d in Desperdicio.objects.all())
    return compradas - vendidas - desperdiciadas


def stock_actual_en_docenas():
    return stock_actual_en_unidades() / 12


def stock_actual_en_maples():
    return stock_actual_en_unidades() / 30


def stock_actual_en_cajones():
    return stock_actual_en_unidades() / 360


def ganancia_total_estimada():
    """
    Ganancia total obtenida por todas las ventas realizadas.
    NOTA: Como eliminamos precio_unitario, esta función ahora es una estimación
    basada en el importe total de las ventas.
    """
    # Por ahora, retornamos 0 ya que necesitamos implementar una nueva lógica
    # basada en la lista de precios al público
    return 0


def valor_compra_stock_actual():
    """
    Valor de compra del stock actual (stock actual * costo promedio por unidad).
    """
    total_gastado = sum(c.precio_unitario *
                        c.cantidad for c in Compra.objects.all())
    total_unidades_compradas = sum(c.total_unidades()
                                   for c in Compra.objects.all())
    if total_unidades_compradas == 0:
        return 0
    costo_promedio = total_gastado / Decimal(total_unidades_compradas)
    stock_actual = Decimal(stock_actual_en_unidades())
    return round(float(stock_actual * costo_promedio), 2)


def total_desechado():
    return sum(d.cantidad for d in Desperdicio.objects.all())


def total_vendido_por_unidad(fecha_inicio=None, fecha_fin=None):
    """
    Devuelve un diccionario con el total vendido por cada tipo de unidad.
    Solo considera ventas de huevos.
    Permite filtrar por rango de fechas 
    """

    totales = {"unidad": 0.0, "maple": 0.0, "docena": 0.0, "cajon": 0.0}
    qs = LineaVenta.objects.filter(categoria__in=["blancos", "color"])

    # Filtrado por fechas si se proveen
    if fecha_inicio:
        qs = qs.filter(venta__fecha__gte=fecha_inicio)
    if fecha_fin:
        qs = qs.filter(venta__fecha__lte=fecha_fin)

    for l in qs:
        if l.unidad and l.cantidad:
            if l.unidad == "unidad":
                totales["unidad"] += float(l.cantidad)
            elif l.unidad == "maple":
                totales["maple"] += float(l.cantidad)
            elif l.unidad == "docena":
                totales["docena"] += float(l.cantidad)
            elif l.unidad == "cajon":
                totales["cajon"] += float(l.cantidad)
    return totales


def total_vendido_por_unidad_semana():
    """
    Devuelve un diccionario con el total vendido por cada tipo de unidad en la semana actual.
    Solo considera ventas de huevos.
    """

    from datetime import date, timedelta

    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de esta semana
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de esta semana

    totales = {"unidad": 0.0, "maple": 0.0, "docena": 0.0, "cajon": 0.0}
    qs = LineaVenta.objects.filter(
        categoria__in=["blancos", "color"],
        venta__fecha__gte=inicio_semana,
        venta__fecha__lte=fin_semana,
    )

    for l in qs:
        if l.unidad and l.cantidad:
            if l.unidad == "unidad":
                totales["unidad"] += float(l.cantidad)
            elif l.unidad == "maple":
                totales["maple"] += float(l.cantidad)
            elif l.unidad == "docena":
                totales["docena"] += float(l.cantidad)
            elif l.unidad == "cajon":
                totales["cajon"] += float(l.cantidad)
    return totales


def valor_vendido():
    """
    Devuelve el valor total vendido, solo suma importe_total si está presente.
    """
    return sum(v.importe_total for v in Venta.objects.all() if v.importe_total)


def valor_vendido_hoy():
    """
    Devuelve el valor total vendido en el día actual, solo suma importe_total si está presente.
    """
    from datetime import date

    hoy = date.today()
    return sum(v.importe_total for v in Venta.objects.filter(fecha=hoy) if v.importe_total)


def valor_vendido_semana():
    """
    Devuelve el valor total vendido en la semana actual (lunes a domingo).
    Solo suma importe_total si está presente.
    """
    from datetime import date, timedelta

    hoy = date.today()
    # weekday() devuelve 0=lunes, 1=martes, ..., 6=domingo
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Lunes de esta semana
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de esta semana

    return sum(
        v.importe_total
        for v in Venta.objects.filter(fecha__gte=inicio_semana, fecha__lte=fin_semana)
        if v.importe_total
    )


def valor_vendido_mes():
    """
    Devuelve el valor total vendido en el mes actual, solo suma importe_total si está presente.
    """
    from datetime import date

    hoy = date.today()
    return sum(
        v.importe_total
        for v in Venta.objects.filter(fecha__month=hoy.month, fecha__year=hoy.year)
        if v.importe_total
    )


def ganacias_diarias():
    """
    Devuelve un diccionario con las ganancias diarias.
    NOTA: Como eliminamos precio_unitario, esta función ahora es una estimación
    basada en el importe total de las ventas.
    """
    # Por ahora, retornamos un diccionario vacío ya que necesitamos implementar
    # una nueva lógica basada en la lista de precios al público
    return {}


def costo_promedio_por_unidad():
    """
    Calcula el costo promedio real por unidad comprada, considerando la unidad de compra.
    """
    total_gastado = sum(float(c.precio_unitario) * float(c.cantidad)
                        for c in Compra.objects.all())
    total_unidades = sum(c.total_unidades() for c in Compra.objects.all())
    if total_unidades == 0:
        return 0
    return total_gastado / float(total_unidades)


def precio_venta_por_huevo(linea):
    """
    NOTA: Esta función ya no es válida porque eliminamos precio_unitario.
    Se debe implementar una nueva lógica basada en la lista de precios al público.
    """
    # Por ahora retornamos 0
    return 0


def alerta_bajo_stock(stock_agrupado):
    """
    Devuelve una lista de mensajes de alerta (uno por cada categoría/subcategoría con bajo stock).
    Omite las subcategorías 'S' y 'R'.
    Si no hay bajo stock, devuelve None.
    Si no hay stock de ningún producto, alerta de stock vacío.
    """
    umbral_bajo = 12
    # Si todos los productos están en 0, mostrar alerta de sin stock
    if not stock_agrupado or all(grupo["stock_unidades"] == 0 for grupo in stock_agrupado):
        return ["¡Sin stock! No hay productos disponibles en el inventario."]
    alertas = []
    for grupo in stock_agrupado:
        if str(grupo["subcategoria"]).upper() in ["S", "R"]:
            continue
        cat = "B" if grupo["categoria"] == "blancos" else "C"
        if grupo["stock_unidades"] == 0:
            alertas.append(
                f"¡Sin stock {cat} - {grupo['subcategoria']} || Avise al encargado.🥸")
        elif grupo["stock_maples"] <= umbral_bajo:
            alertas.append(
                f"¡Stock bajo {cat} - {grupo['subcategoria']} || Revise el inventario.🧐"
            )
    if alertas:
        return alertas
    return None


def stock_actual_por_categoria():
    """
    Devuelve una lista de diccionarios con el stock actual (en huevos, maples y cajones)
    agrupado por categoría y subcategoría, usando total_unidades() para cada movimiento.
    Siempre muestra todas las combinaciones posibles de CATEGORIAS y SUBCATEGORIAS.
    """
    from stock.models import CATEGORIAS, SUBCATEGORIAS, Compra, Desperdicio, LineaVenta

    # Generar todas las combinaciones posibles
    categorias = [
        (cat[0], subcat[0])
        for cat in CATEGORIAS
        if cat[0] in ["blancos", "color"]
        for subcat in SUBCATEGORIAS
    ]
    resultado = []
    for cat, subcat in categorias:
        compradas = sum(
            c.total_unidades() for c in Compra.objects.filter(categoria=cat, subcategoria=subcat)
        )
        vendidas = sum(
            l.total_unidades()
            for l in LineaVenta.objects.filter(categoria=cat, subcategoria=subcat)
        )
        desperdiciadas = sum(
            d.cantidad for d in Desperdicio.objects.filter(categoria=cat, subcategoria=subcat)
        )
        stock_unidades = compradas - vendidas - desperdiciadas
        stock_maples = stock_unidades // 30
        stock_cajones = stock_unidades // 360
        resultado.append(
            {
                "categoria": cat,
                "subcategoria": subcat,
                "stock_unidades": stock_unidades,
                "stock_maples": stock_maples,
                "stock_cajones": stock_cajones,
            }
        )
    return resultado


def gasto_total_por_desperdicio():
    """
    Calcula el gasto total por desperdicio usando el precio_compra de ProductoHuevo
    (precio de referencia de compra, no el real de la última compra).
    """
    from stock.models import ProductoHuevo

    total = 0
    for d in Desperdicio.objects.all():
        producto = ProductoHuevo.objects.filter(
            categoria=d.categoria, subcategoria=d.subcategoria
        ).first()
        if producto and producto.precio_compra:
            precio_unitario = float(
                producto.precio_compra) / 360  # precio por huevo
            total += float(d.cantidad) * precio_unitario
    return round(total, 2)


def gasto_total_por_desperdicio_rango(fecha_inicio=None, fecha_fin=None):
    """
    Calcula el gasto total por desperdicio en un rango de fechas usando el precio_compra de ProductoHuevo
    (precio de referencia de compra, no el real de la última compra).
    """
    from stock.models import ProductoHuevo

    # Filtrar desperdicios por rango de fechas
    desperdicios = Desperdicio.objects.all()
    if fecha_inicio:
        desperdicios = desperdicios.filter(fecha__gte=fecha_inicio)
    if fecha_fin:
        desperdicios = desperdicios.filter(fecha__lte=fecha_fin)

    total = 0
    for d in desperdicios:
        producto = ProductoHuevo.objects.filter(
            categoria=d.categoria, subcategoria=d.subcategoria
        ).first()
        if producto and producto.precio_compra:
            precio_unitario = float(
                producto.precio_compra) / 360  # precio por huevo
            total += float(d.cantidad) * precio_unitario
    return round(total, 2)
