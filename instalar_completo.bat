@echo off
echo ================================================================
echo   INSTALADOR COMPLETO - Sistema de Stock Huevos
echo   Instala Python 3.13.5 + Dependencias + Sistema
echo ================================================================
echo.

REM Verificar si Python ya está instalado y es la versión correcta
python --version 2>nul | findstr "3.13" >nul
if %errorlevel% == 0 (
    echo Python 3.13 ya esta instalado.
    goto :instalar_dependencias
)

echo Python 3.13 no encontrado. Descargando e instalando...
echo.

REM Crear directorio temporal si no existe
if not exist "temp" mkdir temp

REM URL de descarga de Python 3.13.5 para Windows x64
set PYTHON_URL=https://www.python.org/ftp/python/3.13.5/python-3.13.5-amd64.exe
set PYTHON_INSTALLER=temp\python-3.13.5-amd64.exe

echo Descargando Python 3.13.5...
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}"
if errorlevel 1 (
    echo ERROR: No se pudo descargar Python.
    echo Verifica tu conexion a internet.
    pause
    exit /b 1
)

echo Instalando Python 3.13.5...
echo IMPORTANTE: Se instalara Python automaticamente con las opciones recomendadas.
echo.
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_launcher=1
if errorlevel 1 (
    echo ERROR: No se pudo instalar Python.
    echo Intenta ejecutar como administrador.
    pause
    exit /b 1
)

echo Python instalado exitosamente.
echo Refrescando variables de entorno...
REM Actualizar PATH para la sesión actual
set PATH=%PATH%;C:\Program Files\Python313;C:\Program Files\Python313\Scripts

REM Limpiar archivos temporales
if exist "temp" rmdir /s /q temp

:instalar_dependencias
echo.
echo ================================================================
echo   INSTALANDO ENTORNO VIRTUAL Y DEPENDENCIAS
echo ================================================================
echo.

echo Verificando entorno virtual...
if not exist "env" (
    echo Creando entorno virtual...
    python -m venv env
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual.
        echo Reinicia el CMD e intenta nuevamente.
        pause
        exit /b 1
    )
)

echo Activando entorno virtual...
call env\Scripts\activate.bat

echo Actualizando pip...
python -m pip install --upgrade pip

echo Instalando dependencias del sistema...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias.
    echo Verifica tu conexion a internet.
    pause
    exit /b 1
)

echo Instalando pandas...
pip install pandas
if errorlevel 1 (
    echo ERROR: No se pudo instalar pandas.
    echo Verifica tu conexion a internet.
    pause
    exit /b 1
)

echo.
echo ================================================================
echo   INSTALACION COMPLETADA EXITOSAMENTE
echo ================================================================
echo.
echo Python 3.13.5: INSTALADO
echo Entorno virtual: CREADO
echo Dependencias: INSTALADAS
echo Sistema: LISTO PARA USAR
echo.
echo Para ejecutar el sistema, usa: iniciar.bat
echo Para ver la documentacion completa: README.md
echo.
echo NOTA: Si es la primera instalacion, reinicia el CMD antes de usar iniciar.bat
echo.
pause
