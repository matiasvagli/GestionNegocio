# 🥚 Sistema de Gestión de Stock de Huevos

Sistema completo para la gestión de inventario, ventas y reportes de una distribuidora de huevos.

## 🚀 Características

- **Gestión de Stock**: Control de inventario por categorías y subcategorías
- **Registro de Ventas**: Sistema de tickets con múltiples productos
- **Reportes de Ganancias**: Análisis diario, semanal y mensual
- **Control de Gastos**: Registro de gastos generales y desperdicios
- **Gestion de empleados** :Ingreso , pagos de haberes , informacion personal
- **Precios de Referencia**: Gestión de precios por categorías
- **Dashboard Interactivo**: Visualización en tiempo real

## 🛠️ Tecnologías

- **Backend**: Django 5.2
- **Base de Datos**: SQLite
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Otros**: Python 3.x, django-extensions

## ⚙️ Instalación y Configuración

### **👤 Para USUARIOS FINALES (Súper Fácil)**

#### **Opción 1: Instalación COMPLETA (RECOMENDADA)**
**Instala Python 3.13.5 + Sistema automáticamente**
1. Ejecuta: `instalar_completo.bat` (como administrador si es posible)
2. Espera a que se complete la instalación (puede tomar varios minutos)
3. El sistema se iniciará automáticamente

#### **Opción 2: Instalación RÁPIDA (Si ya tienes Python)**
1. Ejecuta: `instalar.bat`
2. Espera a que se instalen las dependencias
3. El sistema se iniciará automáticamente

**📊 DATOS DE PRUEBA INCLUIDOS:**
- ✅ La base de datos SQLite viene con **datos de ejemplo** precargados
- ✅ Productos, ventas, stock y precios listos para probar
- ✅ Puedes empezar a usar el sistema inmediatamente
- ✅ Ideal para **evaluar todas las funcionalidades**

---

### **👨‍💻 Para DESARROLLADORES (Docker)**
**¿Vas a modificar o desarrollar el código?**

#### **Requisitos:**
1. ✅ Descargar Docker Desktop: https://desktop.docker.com/
2. ✅ Instalar y reiniciar PC
3. ✅ Asegurarse de que Docker Desktop esté ejecutándose

#### **Uso:**
```batch
# ¡Un solo comando y todo funciona!
iniciar_docker.bat
```

#### **Comandos disponibles:**
```batch
iniciar_docker.bat     # Iniciar sistema completo
detener_docker.bat     # Detener sistema
limpiar_docker.bat     # Limpiar datos y contenedores
logs_docker.bat        # Ver logs del sistema
```

#### **Ventajas de Docker:**
- ✅ **Entorno aislado**: No afecta tu sistema
- ✅ **Consistente**: Mismo entorno en todas las PCs
- ✅ **Fácil limpieza**: Un comando y todo se resetea
- ✅ **Independiente**: No necesitas instalar Python
- ✅ **Profesional**: Igual que en producción

### **Opción 3: Instalación Manual (Para desarrolladores)**

#### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/huevos-stock.git
cd huevos-stock
```

#### 2. Crear entorno virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno
```bash
# Copiar el archivo de ejemplo
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
```

Editar `.env` con tus configuraciones:
```env
SECRET_KEY=tu-clave-secreta-super-segura
DEBUG=True
```

#### 5. Configurar base de datos
```bash
python manage.py migrate
python manage.py createsuperuser
```

#### 6. Ejecutar servidor
```bash
python manage.py runserver
```

## 🔐 Seguridad

### Variables de Entorno
El proyecto utiliza variables de entorno para proteger datos sensibles:

- **SECRET_KEY**: Clave secreta de Django (⚠️ CRÍTICO)
- **DEBUG**: Modo de desarrollo/producción

**⚠️ IMPORTANTE PARA SEGURIDAD**: 
- **NUNCA** subas el archivo `.env` a GitHub
- Usa una SECRET_KEY diferente y segura en producción
- Pon `DEBUG=False` en producción
- El archivo `.env` ya está excluido en `.gitignore`

### Generar Nueva SECRET_KEY Segura
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Configuración de Producción
```env
SECRET_KEY=clave-super-secura-de-50-caracteres-minimo
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com
```

## 🎯 Primeros Pasos

### **Después de la instalación automática:**
1. **🌐 Abrir navegador**: Ve a `http://localhost:8000`
2. **📊 Explorar Dashboard**: Verás el resumen con datos de ejemplo
3. **🎫 Probar Ventas**: Registra una venta en "Registrar Venta"
4. **📈 Ver Reportes**: Analiza ganancias en "Reporte de Ganancias"
5. **⚙️ Gestión**: Ajusta precios en "Precios de Referencia"

### **🔑 Credenciales de Prueba:**
- **👤 Usuario administrador**: `admin`
- **🔒 Contraseña**: `admin`
- **🌐 Panel admin**: `http://localhost:8000/admin`

### **Datos de ejemplo incluidos:**
- **🥚 Productos**: Huevos blancos y de color (diferentes tamaños)
- **📦 Stock**: Inventario inicial para probar el sistema
- **💰 Ventas**: Algunas ventas de ejemplo para ver reportes
- **💵 Precios**: Precios de referencia configurados

### **Para empezar con datos reales:**
1. **🧹 Opcional**: Ejecuta `limpiar_datos.bat` para empezar desde cero
2. **⚙️ Configura**: Ajusta precios según tu negocio
3. **📦 Carga**: Ingresa tu stock inicial
4. **🚀 ¡Listo!**: Comienza a usar el sistema

## 💬 Contacto y Feedback

### **¿Te gustó el proyecto?**
⭐ **¡Dale una estrella en GitHub!** - Eso me ayuda mucho y motiva a seguir mejorando

### **¿Tienes dudas o sugerencias?**
📧 **Contáctame**: Estoy disponible para ayudarte .

- 📧 Vaglimatias@gmail.com


### **¿Encontraste un bug?**
🐛 **Reporta issues**: Abre un issue en GitHub describiendo el problema

### **¿Quieres contribuir?**
🤝 **Pull Requests bienvenidos**: Mejoras, nuevas funcionalidades, correcciones

### **Servicios profesionales:**
💼 **Desarrollo personalizado**: Adaptaciones específicas para tu negocio
🎓 **Capacitación**: Entrenamiento en el uso del sistema
🛠️ **Soporte técnico**: Instalación y mantenimiento

---

### **📈 Estadísticas del proyecto:**
- 🏆 **Estado**: Activo y en desarrollo
- 📅 **Última actualización**: Julio 2025  
- 🔄 **Versión**: v1.0.0
- 🎯 **Próximas funcionalidades**: Docker, reportes avanzados, móvil

**💡 Este proyecto fue desarrollado con pasión para ayudar a pequeños y medianos emprendedores del sector avícola a digitalizar y optimizar su gestión de stock y ventas.**

---

⭐ **Si este proyecto te ayuda, ¡dale una estrella en GitHub!** ⭐
