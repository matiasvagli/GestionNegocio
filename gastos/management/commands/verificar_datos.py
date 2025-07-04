from django.core.management.base import BaseCommand

from gastos.models import Empleado, Gasto


class Command(BaseCommand):
    help = "Verifica el estado de empleados y gastos en la base de datos"

    def handle(self, *args, **options):
        # Verificar empleados
        empleados = Empleado.objects.all()
        self.stdout.write(f"Total de empleados: {empleados.count()}")

        for empleado in empleados:
            self.stdout.write(f"- {empleado.nombre} {empleado.apellido} (ID: {empleado.id})")

        # Verificar gastos
        gastos = Gasto.objects.all()
        self.stdout.write(f"\nTotal de gastos: {gastos.count()}")

        for gasto in gastos:
            empleado_nombre = gasto.empleado.nombre if gasto.empleado else "Sin empleado"
            self.stdout.write(f"- {gasto.get_tipo_display()}: ${gasto.monto} - {empleado_nombre}")

        # Verificar últimos sueldos y aguinaldos
        self.stdout.write(f"\nVerificando métodos ultimo_sueldo y ultimo_aguinaldo:")
        for empleado in empleados:
            try:
                ultimo_sueldo = empleado.ultimo_sueldo()
                ultimo_aguinaldo = empleado.ultimo_aguinaldo()
                self.stdout.write(
                    f"- {empleado.nombre}: Último sueldo = {ultimo_sueldo}, Último aguinaldo = {ultimo_aguinaldo}"
                )
            except Exception as e:
                self.stdout.write(f"- {empleado.nombre}: ERROR - {e}")
