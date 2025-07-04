# Importaciones consolidadas
from decimal import Decimal


from gastos.models import Gasto
from stock.models import LineaVenta, ProductoHuevo, Venta
from stock.utils.dashboard_utils import gasto_total_por_desperdicio, gasto_total_por_desperdicio_rango


def ganancia_huevos_rango(fecha_inicio, fecha_fin):
    from decimal import Decimal

    total_ganancia = Decimal("0")
    total_costo = Decimal("0")
    lineas = LineaVenta.objects.filter(
        venta__fecha__range=(fecha_inicio, fecha_fin), categoria__in=[
            "blancos", "color"]
    )
    for linea in lineas:
        try:
            prod = ProductoHuevo.objects.get(
                categoria=linea.categoria, subcategoria=linea.subcategoria
            )
        except ProductoHuevo.DoesNotExist:
            continue
        precio_ref = None
        cantidad = linea.cantidad or 0
        huevos = Decimal("0")
        if linea.unidad == "cajon":
            precio_ref = prod.precio_tentativo_cajon
            huevos = Decimal("360") * cantidad
        elif linea.unidad == "maple":
            if cantidad >= 3 and prod.precio_tentativo_3maples:
                precio_ref = prod.precio_tentativo_3maples / Decimal("3")
                huevos = Decimal("30") * cantidad
            else:
                precio_ref = prod.precio_tentativo_maple
                huevos = Decimal("30") * cantidad
        elif linea.unidad == "docena":
            precio_ref = (
                prod.precio_tentativo_maple / Decimal("2.5")
                if prod.precio_tentativo_maple
                else None
            )
            huevos = Decimal("12") * cantidad
        if not precio_ref or not prod.precio_compra:
            continue
        costo_por_huevo = prod.precio_compra / Decimal("360")
        total_ganancia += cantidad * precio_ref
        total_costo += huevos * costo_por_huevo
    return float(total_ganancia - total_costo)


def ganancia_otros_rango(fecha_inicio, fecha_fin):
    from decimal import Decimal

    porcentaje_ganancia = Decimal("0.20")
    ventas = Venta.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
    total_vendido = sum([v.importe_total or 0 for v in ventas])
    lineas_huevos = LineaVenta.objects.filter(
        venta__fecha__range=(fecha_inicio, fecha_fin), categoria__in=[
            "blancos", "color"]
    )
    total_huevos = Decimal("0")
    for linea in lineas_huevos:
        try:
            prod = ProductoHuevo.objects.get(
                categoria=linea.categoria, subcategoria=linea.subcategoria
            )
        except ProductoHuevo.DoesNotExist:
            continue
        precio_ref = None
        cantidad = linea.cantidad or 0
        if linea.unidad == "cajon":
            precio_ref = prod.precio_tentativo_cajon
        elif linea.unidad == "maple":
            if cantidad >= 3 and prod.precio_tentativo_3maples:
                precio_ref = prod.precio_tentativo_3maples / Decimal("3")
            else:
                precio_ref = prod.precio_tentativo_maple
        elif linea.unidad == "docena":
            precio_ref = (
                prod.precio_tentativo_maple / Decimal("2.5")
                if prod.precio_tentativo_maple
                else None
            )
        if not precio_ref:
            continue
        total_huevos += cantidad * precio_ref
    total_otros = Decimal(total_vendido) - total_huevos
    if total_otros < 0:
        total_otros = Decimal("0")
    return float(total_otros * porcentaje_ganancia)


# Funciones públicas simplificadas


def valor_ganancia_diaria_huevos():
    from datetime import date

    hoy = date.today()
    return ganancia_huevos_rango(hoy, hoy)


def ganancias_otros_diaria():
    from datetime import date

    hoy = date.today()
    return ganancia_otros_rango(hoy, hoy)


def ganancias_total_dia():
    return valor_ganancia_diaria_huevos() + ganancias_otros_diaria()


def valor_ganancia_semanal_huevos():
    from datetime import date, timedelta

    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    return ganancia_huevos_rango(inicio_semana, hoy)


def ganancias_otros_semanal():
    from datetime import date, timedelta

    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    return ganancia_otros_rango(inicio_semana, hoy)


def ganancias_total_semana():
    return valor_ganancia_semanal_huevos() + ganancias_otros_semanal()


def valor_ganancia_mensual_huevos():
    from datetime import date

    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    return ganancia_huevos_rango(inicio_mes, hoy)


def ganancias_otros_mensual():
    from datetime import date

    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    return ganancia_otros_rango(inicio_mes, hoy)


def ganancias_total_mes():
    return Decimal(valor_ganancia_mensual_huevos()) + Decimal(ganancias_otros_mensual())


def gasto_mensual():
    from datetime import date

    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    # Vamos a calcular los gastos generales utilizando ambos métodos
    # para asegurarnos de que no falte ningún gasto

    # Método 1: Calculando todos los gastos con total_gastos_generales
    gastos_generales_metodo1 = Gasto.total_gastos_generales(inicio_mes, hoy)

    # Método 2: Calculando separadamente y sumando
    gastos_sin_aguinaldos = Gasto.objects.exclude(tipo="aguinaldo").filter(
        fecha__gte=inicio_mes, fecha__lte=hoy, monto__isnull=False
    )
    total_sin_aguinaldos = sum(
        g.monto for g in gastos_sin_aguinaldos if g.monto is not None)

    # Calcular aguinaldos directamente
    aguinaldos = Gasto.total_aguinaldos(inicio_mes, hoy)

    # Usar el método que proporcione el valor más alto para asegurar que
    # todos los gastos estén incluidos correctamente
    gastos_generales_metodo2 = total_sin_aguinaldos + aguinaldos

    # Elegir el valor más alto entre los dos métodos
    gastos_totales = max(gastos_generales_metodo1, gastos_generales_metodo2)

    # Añadir los gastos por desperdicios
    gastos_desperdicios = Decimal(
        gasto_total_por_desperdicio_rango(inicio_mes, hoy))

    return gastos_totales + gastos_desperdicios


def resultado_mensual():
    return ganancias_total_mes() - gasto_mensual()


def diagnostico_aguinaldos():
    """
    Función temporal para diagnosticar problemas con los aguinaldos.
    Compara los aguinaldos encontrados directamente vs los incluidos en gastos_generales.
    """
    from datetime import date

    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    # 1. Calcular aguinaldos directamente
    aguinaldos_directos = Gasto.total_aguinaldos(inicio_mes, hoy)

    # 2. Contar registros de aguinaldos
    registros_aguinaldo = Gasto.objects.filter(
        tipo="aguinaldo", fecha__gte=inicio_mes, fecha__lte=hoy, monto__isnull=False
    ).count()

    # 3. Calcular gastos generales excluyendo explícitamente aguinaldos
    gastos_sin_aguinaldos = Gasto.objects.exclude(tipo="aguinaldo").filter(
        fecha__gte=inicio_mes, fecha__lte=hoy, monto__isnull=False
    )
    total_sin_aguinaldos = sum(
        g.monto for g in gastos_sin_aguinaldos if g.monto is not None)

    # 4. Calcular gastos generales con el método estándar (debería incluir aguinaldos)
    gastos_generales_estandar = Gasto.total_gastos_generales(inicio_mes, hoy)

    # 5. La diferencia debería ser igual a los aguinaldos directos
    diferencia = gastos_generales_estandar - total_sin_aguinaldos

    # 6. Retornar diccionario con los datos
    return {
        "aguinaldos_directos": float(aguinaldos_directos),
        "registros_aguinaldo": registros_aguinaldo,
        "total_sin_aguinaldos": float(total_sin_aguinaldos),
        "gastos_generales_estandar": float(gastos_generales_estandar),
        "diferencia": float(diferencia),
        "aguinaldos_incluidos_en_generales": float(diferencia) == float(aguinaldos_directos)
    }


def diagnostico_aguinaldos_rango(inicio, fin):
    """
    Función para diagnosticar problemas con los aguinaldos en un rango específico.
    Compara los aguinaldos encontrados directamente vs los incluidos en gastos_generales.
    """

    # 1. Calcular aguinaldos directamente
    aguinaldos_directos = Gasto.total_aguinaldos(inicio, fin)

    # 2. Contar registros de aguinaldos
    registros_aguinaldo = Gasto.objects.filter(
        tipo="aguinaldo", fecha__gte=inicio, fecha__lte=fin, monto__isnull=False
    ).count()

    # 3. Calcular gastos generales excluyendo explícitamente aguinaldos
    gastos_sin_aguinaldos = Gasto.objects.exclude(tipo="aguinaldo").filter(
        fecha__gte=inicio, fecha__lte=fin, monto__isnull=False
    )
    total_sin_aguinaldos = sum(
        g.monto for g in gastos_sin_aguinaldos if g.monto is not None)

    # 4. Calcular gastos generales con el método estándar (debería incluir aguinaldos)
    gastos_generales_estandar = Gasto.total_gastos_generales(inicio, fin)

    # 5. La diferencia debería ser igual a los aguinaldos directos
    diferencia = gastos_generales_estandar - total_sin_aguinaldos

    # 6. Mostrar los registros específicos de aguinaldos para inspección
    aguinaldos_registros = list(Gasto.objects.filter(
        tipo="aguinaldo", fecha__gte=inicio, fecha__lte=fin, monto__isnull=False
    ).values('id', 'fecha', 'monto', 'empleado__nombre', 'descripcion'))

    # 7. Retornar diccionario con los datos
    return {
        "aguinaldos_directos": float(aguinaldos_directos),
        "registros_aguinaldo": registros_aguinaldo,
        "aguinaldos_registros": aguinaldos_registros,
        "total_sin_aguinaldos": float(total_sin_aguinaldos),
        "gastos_generales_estandar": float(gastos_generales_estandar),
        "diferencia": float(diferencia),
        "aguinaldos_incluidos_en_generales": abs(float(diferencia) - float(aguinaldos_directos)) < 0.01
    }
