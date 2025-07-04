from django import template

register = template.Library()


@register.filter
def formato_dinero(value):
    """
    Formatea un número como dinero con separadores de miles y símbolo de peso.
    Ejemplo: 10000 -> $10.000, 10000.50 -> $10.000,50
    """
    if value is None:
        return ""

    try:
        # Convertir a float si es necesario
        if isinstance(value, str):
            value = float(value)

        # Redondear a 2 decimales máximo
        value = round(float(value), 2)

        # Separar parte entera y decimal
        integer_part = int(value)
        decimal_part = round((value - integer_part) * 100)

        # Formatear parte entera con separadores de miles
        integer_with_dots = f"{integer_part:,}".replace(",", ".")

        # Si hay decimales, agregarlos con coma
        if decimal_part > 0:
            return f"${integer_with_dots},{decimal_part:02d}"
        else:
            return f"${integer_with_dots}"

    except (ValueError, TypeError):
        return str(value)


@register.filter
def formato_numero(value):
    """
    Formatea un número con separadores de miles pero sin símbolo de peso.
    Ejemplo: 10000 -> 10.000, 10000.50 -> 10.000,50
    """
    if value is None:
        return ""

    try:
        # Convertir a float y redondear a 2 decimales máximo
        value = round(float(value), 2)

        # Separar parte entera y decimal
        integer_part = int(value)
        decimal_part = round((value - integer_part) * 100)

        # Formatear parte entera con separadores de miles
        integer_with_dots = f"{integer_part:,}".replace(",", ".")

        # Si hay decimales, agregarlos con coma
        if decimal_part > 0:
            return f"{integer_with_dots},{decimal_part:02d}"
        else:
            return integer_with_dots

    except (ValueError, TypeError):
        return str(value)
