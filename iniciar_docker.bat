@echo off
echo.
echo ========================================
echo   🥚 SISTEMA DE GESTION DE HUEVOS 🥚
echo ========================================
echo           🐳 VERSION DOCKER 🐳
echo ========================================
echo.

REM Verificar si Docker está instalado y funcionando
echo ✅ Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker no está instalado o no funciona
    echo.
    echo 📥 Por favor descarga Docker Desktop desde:
    echo    https://desktop.docker.com/win/main/amd64/Docker Desktop Installer.exe
    echo.
    pause
    exit /b 1
)

REM Verificar si Docker Desktop está corriendo
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Docker Desktop no está ejecutándose
    echo.
    echo 🚀 Por favor inicia Docker Desktop y espera a que esté listo
    echo    Luego ejecuta este script nuevamente
    echo.
    pause
    exit /b 1
)

echo ✅ Docker está funcionando correctamente
echo.

REM Verificar si .env existe, si no crearlo
if not exist .env (
    echo 📝 Creando archivo .env desde ejemplo...
    copy .env.example .env >nul
    if %errorlevel% neq 0 (
        echo ❌ Error al crear archivo .env
        pause
        exit /b 1
    )
)

echo 🏗️ Construyendo contenedores Docker...
echo    (Esto puede tomar unos minutos la primera vez)
echo.

docker-compose up --build -d

if %errorlevel% neq 0 (
    echo ❌ Error al construir o iniciar contenedores
    echo.
    echo 🔍 Revisa los logs con: docker-compose logs
    pause
    exit /b 1
)

echo.
echo ⏳ Esperando que el servicio esté listo...
timeout /t 15 /nobreak >nul

echo.
echo 🎉 ¡Sistema iniciado exitosamente con Docker!
echo.
echo 🌐 Abre tu navegador en: http://localhost:8000
echo 🔑 Usuario: admin | Contraseña: admin
echo 🛠️ Panel admin en: http://localhost:8000/admin
echo.
echo 📋 Comandos útiles:
echo    detener_docker.bat    - Detener el sistema
echo    limpiar_docker.bat    - Limpiar contenedores y datos
echo    logs_docker.bat       - Ver logs del sistema
echo.

REM Abrir navegador automáticamente
start http://localhost:8000

echo 💡 TIP: Los datos se guardan en la carpeta 'data'
echo     Para empezar desde cero, usa limpiar_docker.bat
echo.
pause
