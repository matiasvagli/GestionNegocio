from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Limpia datos corruptos usando SQL directo"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Primero ver qué datos hay
            cursor.execute("SELECT id, monto, tipo, descripcion FROM gastos_gasto LIMIT 10")
            rows = cursor.fetchall()

            self.stdout.write("Primeros 10 gastos:")
            for row in rows:
                self.stdout.write(f"ID: {row[0]}, Monto: {row[1]}, Tipo: {row[2]}, Desc: {row[3]}")

            # Buscar registros con monto problemático
            cursor.execute("SELECT id, monto FROM gastos_gasto WHERE monto IS NULL OR monto = ''")
            problematicos = cursor.fetchall()

            self.stdout.write(f"\nRegistros problemáticos: {len(problematicos)}")
            for row in problematicos:
                self.stdout.write(f"ID: {row[0]}, Monto: '{row[1]}'")

            # Eliminar registros problemáticos
            if problematicos:
                cursor.execute("DELETE FROM gastos_gasto WHERE monto IS NULL OR monto = ''")
                self.stdout.write(f"Eliminados {len(problematicos)} registros problemáticos")

            # Verificar si quedan registros
            cursor.execute("SELECT COUNT(*) FROM gastos_gasto")
            total = cursor.fetchone()[0]
            self.stdout.write(f"Total de gastos restantes: {total}")
