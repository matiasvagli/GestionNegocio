@echo off
echo.
echo 🧹 Limpiando Sistema de Gestión de Huevos (Docker)...
echo.
echo ⚠️  ADVERTENCIA: Esto eliminará TODOS los contenedores y datos
echo.
set /p respuesta="¿Estás seguro? (s/N): "

if /i "%respuesta%"=="s" (
    echo.
    echo 🗑️ Deteniendo contenedores...
    docker-compose down
    
    echo 🗑️ Eliminando imágenes del proyecto...
    for /f "tokens=3" %%i in ('docker images --filter "reference=huevos_stock*" --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}"') do (
        if not "%%i"=="ID" docker rmi %%i 2>nul
    )
    
    echo 🗑️ Limpiando sistema Docker...
    docker system prune -f
    
    echo ✅ Sistema limpiado completamente
    echo.
    echo 💡 Para volver a iniciar ejecuta: iniciar_docker.bat
) else (
    echo ❌ Operación cancelada
)

echo.
pause
