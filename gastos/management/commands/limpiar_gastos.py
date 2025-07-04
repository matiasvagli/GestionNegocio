from django.core.management.base import BaseCommand

from gastos.models import Gasto


class Command(BaseCommand):
    help = "Limpia datos corruptos en gastos (montos nulos o inválidos)"

    def handle(self, *args, **options):
        # Buscar gastos con monto nulo
        gastos_nulos = Gasto.objects.filter(monto__isnull=True)
        count_nulos = gastos_nulos.count()

        self.stdout.write(f"Encontrados {count_nulos} gastos con monto nulo")

        # Eliminar gastos con monto nulo
        if count_nulos > 0:
            gastos_nulos.delete()
            self.stdout.write(self.style.SUCCESS(f"Eliminados {count_nulos} gastos con monto nulo"))

        # Buscar gastos con monto 0
        gastos_cero = Gasto.objects.filter(monto=0)
        count_cero = gastos_cero.count()

        self.stdout.write(f"Encontrados {count_cero} gastos con monto 0")

        # Verificar gastos con problemas de formato decimal
        problemas = 0
        for gasto in Gasto.objects.all():
            try:
                float(gasto.monto)
            except (ValueError, TypeError, Exception):
                self.stdout.write(f"Gasto con problema: ID {gasto.id}, monto: {gasto.monto}")
                gasto.delete()
                problemas += 1

        if problemas > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Eliminados {problemas} gastos con problemas de formato")
            )

        self.stdout.write(self.style.SUCCESS("Limpieza de datos completada"))
