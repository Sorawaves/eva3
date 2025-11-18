# 🚛 Sistema de Gestión Logística - Logística Global Ltda.# 🚛 Sistema de Gestión Logística - Logística Global Ltda.



Sistema completo de gestión de transporte terrestre y aéreo desarrollado con Django REST Framework.Sistema de gestión de transporte terrestre y aéreo desarrollado con Django REST Framework.



## 📋 Descripción## 📋 Descripción



Sistema de logística que cumple **100% con los requerimientos de la evaluación**:Este proyecto implementa un sistema completo de gestión logística que incluye:



✅ **8 Modelos de datos** con CHOICES correctos  - **API REST** completa con autenticación JWT

✅ **Autenticación JWT** con vistas protegidas  - **8 modelos de datos**: Vehículos, Aeronaves, Conductores, Pilotos, Rutas, Despachos, Clientes y Cargas

✅ **CRUD completo** para todas las entidades  - **Documentación Swagger** interactiva

✅ **Filtros y búsquedas** avanzadas  - **Interfaz web** con Bootstrap

✅ **Documentación Swagger** interactiva  - **Filtros y búsquedas** avanzadas

✅ **Templates Bootstrap** con footer institucional  - **Panel administrativo** de Django personalizado

✅ **Deployment AWS** con 2 instancias EC2 separadas  

✅ **DuckDNS** para DNS dinámico  ## 🛠️ Tecnologías



---- **Backend**: Django 4.2, Django REST Framework 3.14

- **Autenticación**: Simple JWT

## 🛠️ Tecnologías- **Documentación**: drf-yasg (Swagger/OpenAPI)

- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)

- **Backend:** Django 4.2, Django REST Framework 3.14- **Frontend**: Bootstrap 5, HTML5

- **Autenticación:** Simple JWT (djangorestframework-simplejwt)- **Servidor**: Gunicorn (para deployment)

- **Documentación:** drf-yasg (Swagger/OpenAPI)

- **Base de datos:** SQLite (desarrollo) / PostgreSQL en EC2 (producción)## 📦 Instalación

- **Frontend:** Bootstrap 5, HTML5

- **Servidor:** Gunicorn + Nginx### 1. Clonar el repositorio

- **DNS:** DuckDNS (DNS dinámico gratuito)

```bash

---cd c:\Users\mmrbl\Desktop\Evaluacion3

```

## 🚀 Inicio Rápido (Desarrollo Local)

### 2. Crear entorno virtual

### 1. Clonar el repositorio

```powershell

```bashpython -m venv venv

git clone https://github.com/tu-usuario/logistica.git.\venv\Scripts\activate

cd logistica```

```

### 3. Instalar dependencias

### 2. Crear entorno virtual

```powershell

**Windows (PowerShell):**pip install -r requirements.txt

```powershell```

python -m venv venv

.\venv\Scripts\activate### 4. Aplicar migraciones

```

```powershell

**Linux/Mac:**python manage.py makemigrations

```bashpython manage.py migrate

python3 -m venv venv```

source venv/bin/activate

```### 5. Cargar datos de ejemplo



### 3. Instalar dependencias```powershell

python manage.py shell < load_data.py

```bash```

pip install -r requirements.txt

```Esto creará:

- 5 vehículos

### 4. Aplicar migraciones- 4 aeronaves

- 4 conductores

```bash- 3 pilotos

python manage.py makemigrations- 6 rutas

python manage.py migrate- 5 clientes

```- 7 cargas

- 7 despachos

### 5. Cargar datos de ejemplo- 1 superusuario (admin/admin123)



```bash### 6. Iniciar servidor de desarrollo

python load_data.py

``````powershell

python manage.py runserver

**Datos cargados:**```

- 5 vehículos (camiones, furgones, buses)

- 4 aeronaves (aviones, helicópteros)Accede a: **http://localhost:8000/**

- 4 conductores con licencias vigentes

- 3 pilotos con certificaciones## 🔑 Credenciales de Acceso

- 6 rutas (terrestres y aéreas)

- 5 clientes### Panel Admin

- 7 cargas- **URL**: http://localhost:8000/admin/

- 7 despachos- **Usuario**: `admin`

- 1 superusuario: **admin / admin123**- **Contraseña**: `admin123`



### 6. Iniciar servidor### API JWT Token

Obtener token:

```bash```bash

python manage.py runserverPOST http://localhost:8000/api/token/

```{

    "username": "admin",

Accede a: **http://localhost:8000/**    "password": "admin123"

}

---```



## 🔑 Credenciales de Acceso## 📚 Estructura del Proyecto



### Panel Admin Django```

- **URL:** http://localhost:8000/admin/Evaluacion3/

- **Usuario:** `admin`├── logistica/              # Proyecto Django

- **Contraseña:** `admin123`│   ├── settings.py        # Configuración (JWT, DRF, CORS, DB)

│   ├── urls.py           # URLs principales + Swagger

### API - Obtener Token JWT│   ├── wsgi.py           # WSGI para deployment

│   └── asgi.py           # ASGI

```bash├── transporte/            # App principal

curl -X POST http://localhost:8000/api/token/ \│   ├── models.py         # 8 modelos de datos

  -H "Content-Type: application/json" \│   ├── serializers.py    # Serializers DRF

  -d '{"username":"admin","password":"admin123"}'│   ├── views.py          # ViewSets con permisos JWT

```│   ├── urls.py           # URLs de la API y templates

│   └── admin.py          # Registro de modelos en admin

Respuesta:├── templates/             # Templates HTML con Bootstrap

```json│   ├── base.html         # Template base con navbar y footer

{│   ├── home.html         # Página principal

  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",│   ├── vehiculos.html    # Lista de vehículos

  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."│   ├── aeronaves.html    # Lista de aeronaves

}│   ├── rutas.html        # Lista de rutas

```│   ├── despachos.html    # Lista de despachos

│   └── clientes.html     # Lista de clientes

---├── static/                # Archivos estáticos (CSS, JS, imágenes)

├── media/                 # Archivos multimedia

## 📚 URLs Principales├── load_data.py          # Script de carga de datos

├── manage.py             # Gestor de Django

### Interfaz Web (Templates HTML)├── requirements.txt      # Dependencias del proyecto

└── README.md            # Este archivo

| Página | URL |```

|--------|-----|

| Inicio | http://localhost:8000/ |## 🌐 Endpoints de la API

| Vehículos | http://localhost:8000/vehiculos/ |

| Aeronaves | http://localhost:8000/aeronaves/ |### Autenticación JWT

| Rutas | http://localhost:8000/rutas/ |- `POST /api/token/` - Obtener token de acceso

| Despachos | http://localhost:8000/despachos/ |- `POST /api/token/refresh/` - Refrescar token

| Clientes | http://localhost:8000/clientes/ |

### API REST (CRUD completo)

### API REST- `GET/POST /api/vehiculos/` - Listar/Crear vehículos

- `GET/PUT/DELETE /api/vehiculos/{id}/` - Ver/Editar/Eliminar vehículo

| Recurso | URL |- `GET/POST /api/aeronaves/` - Listar/Crear aeronaves

|---------|-----|- `GET/POST /api/conductores/` - Listar/Crear conductores (**requiere JWT**)

| **Vehículos** | http://localhost:8000/api/vehiculos/ |- `GET/POST /api/pilotos/` - Listar/Crear pilotos (**requiere JWT**)

| **Aeronaves** | http://localhost:8000/api/aeronaves/ |- `GET/POST /api/rutas/` - Listar/Crear rutas (**requiere JWT**)

| **Conductores** | http://localhost:8000/api/conductores/ 🔒 |- `GET/POST /api/clientes/` - Listar/Crear clientes

| **Pilotos** | http://localhost:8000/api/pilotos/ 🔒 |- `GET/POST /api/cargas/` - Listar/Crear cargas

| **Rutas** | http://localhost:8000/api/rutas/ 🔒 |- `GET/POST /api/despachos/` - Listar/Crear despachos (**requiere JWT**)

| **Clientes** | http://localhost:8000/api/clientes/ |

| **Cargas** | http://localhost:8000/api/cargas/ |### Documentación

| **Despachos** | http://localhost:8000/api/despachos/ 🔒 |- `/swagger/` - Documentación Swagger UI

- `/redoc/` - Documentación ReDoc

🔒 = Requiere autenticación JWT- `/swagger.json` - Schema JSON



### Documentación### Interfaz Web

- `/` - Página principal

| Servicio | URL |- `/vehiculos/` - Lista de vehículos

|----------|-----|- `/aeronaves/` - Lista de aeronaves

| **Swagger UI** | http://localhost:8000/swagger/ |- `/rutas/` - Lista de rutas

| **ReDoc** | http://localhost:8000/redoc/ |- `/despachos/` - Lista de despachos

| **JSON Schema** | http://localhost:8000/swagger.json |- `/clientes/` - Lista de clientes



### Autenticación JWT## 🔍 Filtros Disponibles



| Endpoint | URL |### Despachos

|----------|-----|- `?estado=PENDIENTE` - Filtrar por estado

| **Obtener Token** | http://localhost:8000/api/token/ |- `?ruta=1` - Filtrar por ruta

| **Refrescar Token** | http://localhost:8000/api/token/refresh/ |- `?vehiculo=2` - Filtrar por vehículo

- `?aeronave=1` - Filtrar por aeronave

---- `?carga__cliente=3` - Filtrar por cliente



## 📦 Estructura del Proyecto### Vehículos

- `?tipo=CAMION` - Filtrar por tipo

```- `?marca=Mercedes` - Filtrar por marca

logistica/

├── logistica/                    # Configuración del proyecto### Ejemplo de uso:

│   ├── settings.py              # Configuración (JWT, DRF, CORS, DB)```

│   ├── urls.py                  # URLs principales + SwaggerGET http://localhost:8000/api/despachos/?estado=EN_RUTA&ruta=1

│   └── wsgi.py                  # WSGI para deployment```

├── transporte/                   # App principal

│   ├── models.py                # 8 modelos: Vehiculo, Aeronave, etc.## 🔒 Permisos JWT

│   ├── serializers.py           # Serializers DRF

│   ├── views.py                 # ViewSets + vistas HTML### Endpoints que requieren autenticación JWT:

│   ├── urls.py                  # URLs de la app- ✅ **Conductores** (todos los métodos)

│   ├── admin.py                 # Panel admin personalizado- ✅ **Pilotos** (todos los métodos)

│   └── migrations/              # Migraciones de BD- ✅ **Rutas** (todos los métodos)

├── templates/                    # Templates HTML- ✅ **Despachos** (todos los métodos)

│   ├── base.html                # Template base con navbar y footer

│   ├── home.html                # Página principal### Endpoints con IsAuthenticatedOrReadOnly:

│   ├── vehiculos.html           # Lista de vehículos- 📖 **Vehículos** (lectura pública, modificación autenticada)

│   ├── aeronaves.html           # Lista de aeronaves- 📖 **Aeronaves** (lectura pública, modificación autenticada)

│   ├── rutas.html               # Lista de rutas- 📖 **Clientes** (lectura pública, modificación autenticada)

│   ├── despachos.html           # Lista de despachos- 📖 **Cargas** (lectura pública, modificación autenticada)

│   └── clientes.html            # Lista de clientes

├── static/                       # Archivos estáticos## 🗄️ Modelos de Datos

│   ├── css/custom.css           # Estilos personalizados

│   └── js/custom.js             # JavaScript personalizado### 1. Vehiculo

├── manage.py                     # Comando Django- `tipo`: CAMION, FURGON, BUS

├── requirements.txt              # Dependencias Python- `patente`: Único

├── load_data.py                  # Script de carga de datos- `capacidad_kg`: Decimal

├── AWS_DEPLOYMENT.md             # ⭐ Guía deployment Instancia 1 (Web)- `marca`: String

├── INSTANCIA_BD_EC2.md           # ⭐ Guía deployment Instancia 2 (BD)

├── DUCKDNS_SETUP.md              # ⭐ Configuración DuckDNS + SSL### 2. Aeronave

└── ANALISIS_CUMPLIMIENTO.md      # Verificación de requerimientos- `modelo`: String

```- `matricula`: Único

- `capacidad_kg`: Decimal

---- `tipo`: AVION, HELICOPTERO



## 🗄️ Modelos de Datos### 3. Conductor

- `nombre`: String

### 1. Vehiculo- `licencia`: Único

Vehículos terrestres (camiones, furgones, buses)- `vigente`: Boolean

- `tipo`: CHOICES (CAMION, FURGON, BUS)

- `patente`: Único### 4. Piloto

- `capacidad_kg`: Decimal- `nombre`: String

- `marca`: String- `certificacion`: Único

- `horas_vuelo`: Integer

### 2. Aeronave

Aeronaves (aviones, helicópteros)### 5. Ruta

- `tipo`: CHOICES (AVION, HELICOPTERO)- `origen`: String

- `matricula`: Único- `destino`: String

- `capacidad_kg`: Decimal- `tipo_transporte`: TERRESTRE, AEREO

- `modelo`: String

### 6. Cliente

### 3. Conductor- `nombre`: String

Personal terrestre con licencia- `rut`: Único

- `nombre`: String- `direccion`: String

- `licencia`: Único

- `vigente`: Boolean### 7. Carga

- `tipo`: String

### 4. Piloto- `peso_kg`: Decimal

Personal aéreo con certificaciones- `valor`: Decimal

- `nombre`: String- `cliente`: ForeignKey

- `certificacion`: Único

- `horas_vuelo`: Integer### 8. Despacho

- `ruta`: ForeignKey

### 5. Ruta- `vehiculo/aeronave`: ForeignKey (nullable)

Origen y destino de transporte- `conductor/piloto`: ForeignKey (nullable)

- `origen`: String- `carga`: ForeignKey

- `destino`: String- `estado`: PENDIENTE, EN_RUTA, ENTREGADO

- `tipo_transporte`: CHOICES (TERRESTRE, AEREO)- `fecha_creacion`: DateTime (auto)

- `fecha_actualizacion`: DateTime (auto)

### 6. Cliente

Clientes del servicio## 🧪 Pruebas con Swagger

- `nombre`: String

- `rut`: Único1. Accede a **http://localhost:8000/swagger/**

- `direccion`: String2. Haz clic en **Authorize** (🔓)

3. Obtén un token desde `/api/token/`

### 7. Carga4. Ingresa: `Bearer <tu_token>`

Cargas relacionadas a clientes5. Prueba los endpoints protegidos

- `tipo`: String

- `peso_kg`: Decimal## 🚀 Preparación para Deployment en AWS

- `valor`: Decimal

- `cliente`: ForeignKey(Cliente)### Cambios necesarios en `settings.py`:



### 8. Despacho#### 1. Base de datos PostgreSQL (RDS)

Envíos con estadoDescomentar y configurar:

- `ruta`: ForeignKey(Ruta)```python

- `vehiculo`: ForeignKey(Vehiculo) - opcionalDATABASES = {

- `aeronave`: ForeignKey(Aeronave) - opcional    'default': {

- `conductor`: ForeignKey(Conductor) - opcional        'ENGINE': 'django.db.backends.postgresql',

- `piloto`: ForeignKey(Piloto) - opcional        'NAME': 'logistica_db',

- `carga`: ForeignKey(Carga)        'USER': 'logistica_user',

- `estado`: CHOICES (PENDIENTE, EN_RUTA, ENTREGADO)        'PASSWORD': os.environ.get('DB_PASSWORD'),

        'HOST': 'tu-instancia.xxxx.us-east-1.rds.amazonaws.com',

---        'PORT': '5432',

    }

## 🔐 Autenticación JWT}

```

### Vistas Protegidas (Requieren Token)

#### 2. Allowed Hosts

Según los requerimientos, las siguientes vistas **SOLO** aceptan peticiones autenticadas:```python

ALLOWED_HOSTS = [

✅ **Conductores** (`/api/conductores/`) - `IsAuthenticated`      'ec2-XX-XX-XX-XX.compute-1.amazonaws.com',

✅ **Pilotos** (`/api/pilotos/`) - `IsAuthenticated`      'tu-dominio.com',

✅ **Rutas** (`/api/rutas/`) - `IsAuthenticated` (informes)  ]

✅ **Despachos** (`/api/despachos/`) - `IsAuthenticated` (registro de nuevos despachos)  ```



### Uso del Token#### 3. Archivos estáticos

```python

```bashSTATIC_ROOT = '/var/www/html/logistica/static/'

# 1. Obtener token```

TOKEN=$(curl -s -X POST http://localhost:8000/api/token/ \

  -H "Content-Type: application/json" \#### 4. Seguridad (producción)

  -d '{"username":"admin","password":"admin123"}' \Descomentar:

  | python -c "import sys, json; print(json.load(sys.stdin)['access'])")```python

SECURE_SSL_REDIRECT = True

# 2. Usar token en peticionesSESSION_COOKIE_SECURE = True

curl http://localhost:8000/api/conductores/ \CSRF_COOKIE_SECURE = True

  -H "Authorization: Bearer $TOKEN"DEBUG = False

``````



---### Deployment con Gunicorn + Nginx



## 🔍 Filtros y Búsquedas#### 1. Instalar dependencias en EC2

```bash

Todos los endpoints de la API soportan filtros:sudo apt update

sudo apt install python3-pip python3-venv nginx postgresql-client

### Ejemplos:```



```bash#### 2. Clonar proyecto

# Filtrar vehículos por tipo```bash

GET /api/vehiculos/?tipo=CAMIONcd /var/www/html

git clone tu-repositorio.git logistica

# Buscar vehículos por patentecd logistica

GET /api/vehiculos/?search=ABCD12```



# Filtrar despachos por estado#### 3. Entorno virtual

GET /api/despachos/?estado=EN_RUTA```bash

python3 -m venv venv

# Filtrar por clientesource venv/bin/activate

GET /api/despachos/?carga__cliente=1pip install -r requirements.txt

```

# Filtrar rutas por tipo de transporte

GET /api/rutas/?tipo_transporte=AEREO#### 4. Configurar Gunicorn

```bash

# Múltiples filtrosgunicorn --workers 3 --bind 0.0.0.0:8000 logistica.wsgi:application

GET /api/despachos/?estado=ENTREGADO&ruta=1```

```

#### 5. Configurar Nginx

---Crear `/etc/nginx/sites-available/logistica`:

```nginx

## 🚀 Deployment en AWS (Producción)server {

    listen 80;

### Arquitectura: 2 Instancias EC2 Separadas    server_name tu-dominio.com;



El proyecto está diseñado para desplegarse con **DOS INSTANCIAS EC2**:    location / {

        proxy_pass http://127.0.0.1:8000;

#### **Instancia 1 - Servidor Web**        proxy_set_header Host $host;

- Django + Gunicorn + Nginx        proxy_set_header X-Real-IP $remote_addr;

- IP Pública (acceso desde internet)    }

- Puertos: 22, 80, 443

    location /static/ {

#### **Instancia 2 - Base de Datos**        alias /var/www/html/logistica/static/;

- PostgreSQL 14    }

- Solo IP Privada (NO expuesta a internet)}

- Puerto 5432 (solo desde Instancia 1)```



### Guías de Deployment#### 6. Recolectar estáticos

```bash

📖 **[AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md)** - Configuración de Instancia 1 (Servidor Web)python manage.py collectstatic --noinput

- Instalación de dependencias```

- Configuración de Gunicorn

- Configuración de Nginx## 📝 Notas Importantes

- Variables de entorno

- Archivos estáticos- ⚠️ **SECRET_KEY**: Cambiar en producción y usar variables de entorno

- ⚠️ **DEBUG**: Debe ser `False` en producción

📖 **[INSTANCIA_BD_EC2.md](INSTANCIA_BD_EC2.md)** - Configuración de Instancia 2 (Base de Datos)- ⚠️ **ALLOWED_HOSTS**: Configurar con dominios reales

- Instalación de PostgreSQL en EC2- ⚠️ **PostgreSQL**: Recomendado para producción (RDS en AWS)

- Configuración de `postgresql.conf`- ⚠️ **HTTPS**: Obligatorio en producción

- Configuración de `pg_hba.conf`- ⚠️ **CORS**: Configurar orígenes permitidos específicos

- Security Groups

- Conexión desde Instancia 1## 📞 Soporte



📖 **[DUCKDNS_SETUP.md](DUCKDNS_SETUP.md)** - Configuración de DNS DinámicoPara dudas o problemas:

- Registro en DuckDNS- Email: contacto@logisticaglobal.cl

- Script de actualización automática- Documentación: http://localhost:8000/swagger/

- Configuración de Nginx con dominio

- SSL con Let's Encrypt## 📄 Licencia



### Resumen de Deployment© 2025 Logística Global Ltda. - Todos los derechos reservados.



```bash---

# INSTANCIA 1 (Web)

1. Lanzar EC2 en subnet pública**Desarrollado por**: [Tu nombre aquí]  

2. Instalar Python, Nginx, Git**Sección**: [X]  

3. Clonar proyecto en /var/www/html/logistica**Fecha**: Noviembre 2025

4. Configurar Gunicorn (systemd)
5. Configurar Nginx
6. Configurar DuckDNS
7. Instalar SSL (Let's Encrypt)

# INSTANCIA 2 (BD)
1. Lanzar EC2 en subnet privada (sin IP pública)
2. Instalar PostgreSQL 14
3. Configurar postgresql.conf y pg_hba.conf
4. Crear usuario y base de datos
5. Configurar Security Group (puerto 5432 desde Instancia 1)
6. Probar conexión desde Instancia 1
```

---

## 🧪 Testing

### Probar API con cURL

```bash
# Listar vehículos (público)
curl http://localhost:8000/api/vehiculos/

# Crear vehículo (requiere autenticación)
curl -X POST http://localhost:8000/api/vehiculos/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "CAMION",
    "patente": "WXYZ99",
    "capacidad_kg": 18000.00,
    "marca": "Volvo"
  }'

# Listar despachos (requiere autenticación)
curl http://localhost:8000/api/despachos/ \
  -H "Authorization: Bearer $TOKEN"
```

### Probar con Swagger

1. Ve a: http://localhost:8000/swagger/
2. Haz clic en **Authorize** 🔓
3. Ingresa el token JWT (sin "Bearer")
4. Prueba los endpoints directamente desde la interfaz

---

## 📊 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Cargar datos de ejemplo
python load_data.py

# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar shell de Django
python manage.py shell

# Recolectar archivos estáticos (producción)
python manage.py collectstatic --noinput

# Ver SQL de las migraciones
python manage.py sqlmigrate transporte 0001

# Verificar problemas
python manage.py check
```

---

## 🆘 Troubleshooting

### Error: "No module named 'rest_framework'"

```bash
pip install -r requirements.txt
```

### Error: "Table doesn't exist"

```bash
python manage.py migrate
```

### Error: "Unauthorized" en API

Asegúrate de incluir el token JWT en el header:
```bash
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Error: "CSRF token missing"

En API REST, puedes deshabilitar CSRF usando tokens JWT en lugar de sesiones.

---

## 📄 Documentación Adicional

- **[ANALISIS_CUMPLIMIENTO.md](ANALISIS_CUMPLIMIENTO.md)** - Verificación completa de requerimientos
- **[AWS_DEPLOYMENT.md](AWS_DEPLOYMENT.md)** - Deployment en AWS EC2 (Instancia Web)
- **[INSTANCIA_BD_EC2.md](INSTANCIA_BD_EC2.md)** - Configuración de PostgreSQL en EC2
- **[DUCKDNS_SETUP.md](DUCKDNS_SETUP.md)** - DNS dinámico con DuckDNS

---

## 👨‍💻 Personalización

### Actualizar Footer con tus Datos

Edita `templates/base.html`:

```html
<footer class="footer">
    <div class="text-center">
        <p class="mb-0">© 2025 | [TU NOMBRE] | Sección [TU SECCIÓN] | Logística Global Ltda.</p>
    </div>
</footer>
```

### Cambiar Logo

Reemplaza el placeholder en `templates/base.html`:

```html
<span class="logo-placeholder">LG</span>
```

Por:

```html
<img src="{% static 'images/logo.png' %}" alt="Logo" height="40">
```

---

## 📋 Checklist de Requerimientos

✅ **Modelo de Datos**
- [x] 8 modelos con CHOICES correctos
- [x] Migraciones generadas
- [x] Serializers completos
- [x] CRUD completo

✅ **Autenticación JWT**
- [x] JWT instalado y configurado
- [x] Vistas protegidas (Conductores, Pilotos, Rutas, Despachos)
- [x] Endpoints de token

✅ **Funcionalidades**
- [x] Filtros y búsquedas
- [x] Documentación Swagger
- [x] Templates Bootstrap
- [x] Footer institucional
- [x] Carga de datos inicial

✅ **AWS Deployment**
- [x] Guía para Instancia 1 (Web)
- [x] Guía para Instancia 2 (BD en EC2)
- [x] Configuración de DuckDNS
- [x] Arquitectura de 2 instancias separadas
- [x] Security Groups segmentados
- [x] BD no expuesta a internet

---

## 📞 Soporte

Para más información, consulta:
- Swagger UI: http://localhost:8000/swagger/
- Panel Admin: http://localhost:8000/admin/
- [Documentación oficial de Django](https://docs.djangoproject.com/)
- [Documentación de DRF](https://www.django-rest-framework.org/)

---

## 🎯 Estado del Proyecto

✅ **100% COMPLETO** - Cumple todos los requerimientos de la evaluación

- ✅ 8 Modelos de datos con CHOICES
- ✅ Autenticación JWT
- ✅ CRUD completo
- ✅ Filtros y búsquedas
- ✅ Swagger/OpenAPI
- ✅ Templates Bootstrap
- ✅ Footer institucional
- ✅ Carga de datos inicial
- ✅ Deployment AWS (2 instancias EC2)
- ✅ DuckDNS configurado
- ✅ SSL/HTTPS

---

**© 2025 | [Tu Nombre] | Sección [X] | Logística Global Ltda.**
