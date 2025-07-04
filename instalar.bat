@echo off
echo ========================================
echo   INSTALADOR - Sistema de Stock Huevos
echo ========================================
echo.
echo Verificando entorno virtual...

if not exist "env" (
    echo Creando entorno virtual...
    python -m venv env
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        echo Asegurate de tener Python instalado.
        pause
        exit /b 1
    )
)

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para ejecutar el sistema, usa: iniciar.bat
echo.
pause
