@echo off
rem Cambiar al directorio del script
cd /D "%~dp0"

echo ========================================
echo Gestor de Stock - Mauricio Carrera
echo ========================================
echo.
echo El servidor se iniciará en http://127.0.0.1:8000/dashboard
echo Presione Ctrl+C en esta ventana para finalizar el servidor.
echo.

echo Iniciando el sistema de stock...
call env\Scripts\activate.bat
start http://127.0.0.1:8000/dashboard 
python manage.py runserver
pause
