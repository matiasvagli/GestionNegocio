from django.shortcuts import render

from stock.forms import CompraForm

# Este módulo debe contener solo funciones utilitarias de datos para compras.


def ingreso_compra(request):
    mensaje = None
    if request.method == "POST":
        form = CompraForm(request.POST)
        if form.is_valid():
            form.save()
            mensaje = "¡Compra registrada exitosamente!"
            form = CompraForm()  # Limpiar el formulario para nueva carga
    else:
        form = CompraForm()
    return render(request, "stock/ingreso_compra.html", {"form": form, "mensaje": mensaje})
