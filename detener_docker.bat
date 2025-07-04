@echo off
echo.
echo 🛑 Deteniendo Sistema de Gestión de Huevos (Docker)...
echo.

docker-compose down

if %errorlevel% equ 0 (
    echo ✅ Sistema detenido exitosamente
    echo.
    echo 💡 Para volver a iniciarlo ejecuta: iniciar_docker.bat
) else (
    echo ❌ Error al detener el sistema
    echo.
    echo 🔍 Revisa si Docker Desktop está funcionando
)

echo.
pause
