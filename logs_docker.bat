@echo off
echo.
echo 📋 Mostrando logs del Sistema de Gestión de Huevos (Docker)...
echo.
echo 💡 Presiona Ctrl+C para salir de los logs
echo.

docker-compose logs -f --tail=100

pause
