from django.forms import formset_factory
from django.shortcuts import render

from stock.forms import LineaVentaForm, VentaForm

# Este módulo debe contener solo funciones utilitarias de datos para ventas.
# Si necesitas lógica de vista, debe estar en views.py


def ingreso_venta(request):
    LineaVentaFormSet = formset_factory(LineaVentaForm, extra=0, can_delete=True)

    if request.method == "POST":
        venta_form = VentaForm(request.POST)
        linea_formset = LineaVentaFormSet(request.POST, prefix="lineas")

        if venta_form.is_valid() and linea_formset.is_valid():
            # Guardar la venta principal
            venta = venta_form.save()

            # Guardar las líneas de venta
            for linea_form in linea_formset:
                if linea_form.cleaned_data and not linea_form.cleaned_data.get("DELETE"):
                    linea = linea_form.save(commit=False)
                    linea.venta = venta
                    linea.save()

            mensaje = f"¡Venta registrada exitosamente! Importe: ${venta.importe_total}"
            venta_form = VentaForm()
            linea_formset = LineaVentaFormSet(prefix="lineas")
        else:
            mensaje = "Por favor, corrija los errores en el formulario."
    else:
        venta_form = VentaForm()
        linea_formset = LineaVentaFormSet(prefix="lineas")
        mensaje = None

    return render(
        request,
        "stock/ingreso_venta.html",
        {"venta_form": venta_form, "linea_formset": linea_formset, "mensaje": mensaje},
    )
