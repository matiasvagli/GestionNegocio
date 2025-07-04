import csv
from datetime import date

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from ..models import Empleado, Gasto


def empleados_view(request):
    """Vista principal para gestionar empleados"""
    busqueda = request.GET.get("buscar", "")

    # Filtrar empleados por búsqueda
    empleados = Empleado.objects.all()
    if busqueda:
        empleados = empleados.filter(
            Q(nombre__icontains=busqueda)
            | Q(apellido__icontains=busqueda)
            | Q(dni__icontains=busqueda)
        )

    # Ordenar por activos primero, luego por nombre
    empleados = empleados.order_by("-activo", "nombre")

    context = {
        "empleados": empleados,
        "busqueda": busqueda,
    }
    return render(request, "gastos/empleados.html", context)


def empleado_crear(request):
    """Crear nuevo empleado"""
    if request.method == "POST":
        try:
            empleado = Empleado.objects.create(
                nombre=request.POST["nombre"],
                apellido=request.POST["apellido"],
                dni=request.POST.get("dni", ""),
                telefono=request.POST.get("telefono", ""),
                direccion=request.POST.get("direccion", ""),
                email=request.POST.get("email", ""),
                fecha_ingreso=request.POST.get("fecha_ingreso") or None,
                cbu_cvu=request.POST.get("cbu_cvu", ""),
                activo=True,
            )
            messages.success(
                request, f"Empleado {empleado.nombre} {empleado.apellido} creado exitosamente."
            )
        except Exception as e:
            messages.error(request, f"Error al crear empleado: {str(e)}")

    return redirect("empleados")


def empleado_editar(request, empleado_id):
    """Editar empleado existente"""
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == "POST":
        try:
            empleado.nombre = request.POST["nombre"]
            empleado.apellido = request.POST["apellido"]
            empleado.dni = request.POST.get("dni", "")
            empleado.telefono = request.POST.get("telefono", "")
            empleado.direccion = request.POST.get("direccion", "")
            empleado.email = request.POST.get("email", "")
            empleado.fecha_ingreso = request.POST.get("fecha_ingreso") or None
            empleado.cbu_cvu = request.POST.get("cbu_cvu", "")
            empleado.activo = "activo" in request.POST
            empleado.save()

            messages.success(
                request, f"Empleado {empleado.nombre} {empleado.apellido} actualizado exitosamente."
            )
        except Exception as e:
            messages.error(request, f"Error al actualizar empleado: {str(e)}")

    return redirect("empleados")


def pagar_sueldo(request, empleado_id):
    """Registrar pago de sueldo"""
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == "POST":
        try:
            monto_str = request.POST.get("monto", "").strip()
            if not monto_str:
                raise ValueError("El monto es obligatorio")

            # Limpiar y validar el monto igual que en otros formularios
            from decimal import Decimal, InvalidOperation

            try:
                # Remover espacios y caracteres no numéricos excepto punto y coma
                monto_cleaned = monto_str.replace(" ", "").replace("$", "")

                # Reemplazar coma por punto para decimales
                if "," in monto_cleaned and "." in monto_cleaned:
                    # Si tiene ambos, asumir que . es separador de miles y , es decimal
                    parts = monto_cleaned.split(",")
                    if len(parts) == 2 and len(parts[1]) <= 2:
                        monto_cleaned = monto_cleaned.replace(".", "").replace(",", ".")
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
                if monto <= 0:
                    raise ValueError("El monto debe ser mayor a 0")
                # 13 dígitos enteros + 2 decimales
                if monto > Decimal("9999999999999.99"):
                    raise ValueError("El monto es demasiado grande")

            except (InvalidOperation, ValueError) as ve:
                if "InvalidOperation" in str(type(ve)):
                    raise ValueError(
                        "El monto debe ser un número válido. Ejemplo: 5000 o 1500000.50"
                    )
                else:
                    raise ve

            tipo = request.POST.get("tipo", "sueldo")  # 'sueldo' o 'aguinaldo'
            fecha = request.POST.get("fecha", date.today())
            descripcion = request.POST.get("descripcion", "")

            gasto = Gasto.objects.create(
                empleado=empleado, fecha=fecha, monto=monto, tipo=tipo, descripcion=descripcion
            )

            tipo_display = "Sueldo" if tipo == "sueldo" else "Aguinaldo/Bono"
            messages.success(
                request,
                f"{tipo_display} de ${monto} pagado a {empleado.nombre} {empleado.apellido}.",
            )

        except ValueError as e:
            messages.error(request, f"Error en el monto: {str(e)}")
        except Exception as e:
            import traceback

            traceback.print_exc()
            messages.error(request, f"Error al registrar pago: {str(e)}")

    return redirect("empleados")


@csrf_exempt
def empleado_toggle_activo(request, empleado_id):
    """Activar/desactivar empleado via AJAX"""
    if request.method == "POST":
        empleado = get_object_or_404(Empleado, id=empleado_id)
        empleado.activo = not empleado.activo
        empleado.save()

        return JsonResponse(
            {
                "success": True,
                "activo": empleado.activo,
                "mensaje": f'Empleado {"activado" if empleado.activo else "desactivado"} exitosamente.',
            }
        )

    return JsonResponse({"success": False})


def exportar_sueldos_csv(request):
    """Exportar historial de sueldos de todos los empleados a CSV"""
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="sueldos_empleados.csv"'

    writer = csv.writer(response)

    # Encabezados
    writer.writerow(["Empleado", "DNI", "Tipo de Pago", "Monto", "Fecha", "Descripción", "Estado"])

    # Obtener todos los pagos de sueldos y aguinaldos
    pagos = (
        Gasto.objects.filter(tipo__in=["sueldo", "aguinaldo"])
        .select_related("empleado")
        .order_by("-fecha", "empleado__apellido")
    )

    for pago in pagos:
        writer.writerow(
            [
                (
                    f"{pago.empleado.nombre} {pago.empleado.apellido}"
                    if pago.empleado
                    else "Sin empleado"
                ),
                pago.empleado.dni if pago.empleado else "",
                pago.get_tipo_display(),
                f"${pago.monto}",
                pago.fecha.strftime("%d/%m/%Y"),
                pago.descripcion or "",
                "Activo" if pago.empleado and pago.empleado.activo else "Inactivo",
            ]
        )

    return response
