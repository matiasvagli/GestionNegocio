from stock.utils.dashboard_utils import stock_actual_por_categoria


def get_stock_agrupado_y_cajones():
    stock_agrupado = stock_actual_por_categoria()
    total_cajones = sum(grupo["stock_cajones"] for grupo in stock_agrupado)
    return stock_agrupado, total_cajones
