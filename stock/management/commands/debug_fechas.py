from django.core.management.base import BaseCommand
from stock.utils.dashboard_utils import debug_ventas_fechas


class Command(BaseCommand):
    help = 'Debug de fechas y ventas para revisar inconsistencias'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            'Ejecutando debug de fechas y ventas...'))
        debug_ventas_fechas()
        self.stdout.write(self.style.SUCCESS('Debug completado.'))
