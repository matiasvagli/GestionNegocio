from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Normaliza montos muy grandes que pueden causar problemas"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Actualizar montos muy grandes (reducir por factor de 100 o 1000)
            cursor.execute(
                """
                UPDATE gastos_gasto 
                SET monto = ROUND(CAST(monto AS REAL) / 1000.0, 2) 
                WHERE CAST(monto AS REAL) > 10000000
            """
            )
            affected = cursor.rowcount
            self.stdout.write(f"Montos normalizados: {affected}")

            # Mostrar los montos actualizados
            cursor.execute("SELECT id, monto, tipo FROM gastos_gasto ORDER BY monto DESC LIMIT 10")
            rows = cursor.fetchall()

            self.stdout.write("\nMontos después de normalización:")
            for row in rows:
                self.stdout.write(f"ID: {row[0]}, Monto: {row[1]}, Tipo: {row[2]}")
