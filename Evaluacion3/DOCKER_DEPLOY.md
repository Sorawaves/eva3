# 🐳 Despliegue con Docker Compose (Alternativa Local)

## 📋 Descripción

Esta configuración con Docker Compose simula la arquitectura de **2 instancias EC2** en tu máquina local, perfecta para:
- ✅ Demostración sin AWS Academy
- ✅ Desarrollo local
- ✅ Testing rápido
- ✅ Backup si AWS falla

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────┐
│           Docker Network (Bridge)           │
│                                             │
│  ┌──────────────┐        ┌──────────────┐  │
│  │   Nginx      │        │              │  │
│  │   (Puerto 80)│───────▶│  Django Web  │  │
│  └──────────────┘        │  (Puerto 8000│  │
│                          │   Gunicorn)  │  │
│                          └──────┬───────┘  │
│                                 │          │
│                                 │ SQL      │
│                                 ▼          │
│                          ┌──────────────┐  │
│                          │  PostgreSQL  │  │
│                          │  (Puerto 5432│  │
│                          │   Database)  │  │
│                          └──────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
         │                    │
         │ HTTP               │ (No expuesto)
         ▼                    ▼
      localhost:80         localhost:5432
```

---

## 🚀 Inicio Rápido

### Prerrequisitos

```bash
# Instalar Docker y Docker Compose
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# Verificar instalación
docker --version
docker-compose --version
```

### Levantar Todo el Sistema

```bash
# Desde el directorio del proyecto
cd /home/fari/Evaluacion3

# Construir y levantar contenedores
docker-compose up -d

# Ver logs
docker-compose logs -f

# Esperar ~30 segundos...
```

### Acceder a la Aplicación

```bash
# Con Nginx (recomendado)
http://localhost

# Directamente a Django
http://localhost:8000

# Swagger
http://localhost/swagger/
# o
http://localhost:8000/swagger/

# Admin
http://localhost/admin/
Usuario: admin
Password: admin123
```

---

## 📊 Comandos Útiles

### Ver estado de los contenedores

```bash
docker-compose ps
```

### Ver logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo Django
docker-compose logs -f web

# Solo PostgreSQL
docker-compose logs -f db

# Solo Nginx
docker-compose logs -f nginx
```

### Ejecutar comandos en Django

```bash
# Shell de Django
docker-compose exec web python manage.py shell

# Crear migraciones
docker-compose exec web python manage.py makemigrations

# Aplicar migraciones
docker-compose exec web python manage.py migrate

# Crear superusuario
docker-compose exec web python manage.py createsuperuser

# Cargar datos (ya se hace automáticamente)
docker-compose exec web python load_data.py
```

### Acceder a PostgreSQL

```bash
# Shell de PostgreSQL
docker-compose exec db psql -U logistica_user -d logistica_db

# Comandos SQL útiles
\dt                           # Listar tablas
\d+ transporte_vehiculo       # Describir tabla
SELECT COUNT(*) FROM transporte_despacho;
```

### Reiniciar servicios

```bash
# Reiniciar todos
docker-compose restart

# Reiniciar solo web
docker-compose restart web

# Reiniciar solo base de datos
docker-compose restart db
```

### Detener y limpiar

```bash
# Detener contenedores (mantiene datos)
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Eliminar TODO (incluyendo volúmenes/datos)
docker-compose down -v

# Eliminar imágenes también
docker-compose down -v --rmi all
```

---

## 🔧 Configuración

### Variables de Entorno

Editar `docker-compose.yml` sección `web.environment`:

```yaml
environment:
  - DEBUG=False                    # Cambiar a True para desarrollo
  - ALLOWED_HOSTS=localhost,...    # Agregar más hosts
  - DB_PASSWORD=TuPasswordSeguro   # Cambiar password
  - SECRET_KEY=tu_clave_secreta    # Generar nueva clave
```

### Puertos

Por defecto:
- **80** → Nginx (acceso web principal)
- **8000** → Django/Gunicorn (acceso directo)
- **5432** → PostgreSQL (solo para debugging)

Para cambiar puertos, editar `docker-compose.yml`:

```yaml
ports:
  - "8080:80"    # Cambiar puerto 80 a 8080
```

---

## 🎓 Para la Evaluación

### Demostración Rápida (1 minuto)

```bash
# 1. Levantar sistema
docker-compose up -d

# 2. Ver logs en tiempo real
docker-compose logs -f

# 3. Abrir navegador
# http://localhost

# 4. Mostrar servicios corriendo
docker-compose ps
```

### Explicación para el Profesor

```
"Profesor, este Docker Compose simula exactamente la arquitectura 
de 2 instancias EC2:

1. Contenedor 'db' = Instancia 2 (PostgreSQL)
   - Base de datos aislada
   - No expuesta a internet (en producción)

2. Contenedor 'web' = Instancia 1 (Django + Gunicorn)
   - Aplicación Django
   - Conecta a 'db' por red interna

3. Contenedor 'nginx' = Reverse proxy
   - Proxy a Django
   - Sirve archivos estáticos

[Mostrar docker-compose ps]
Aquí puede ver los 3 servicios corriendo de forma aislada.

[Mostrar navegador]
La aplicación funciona exactamente igual que en AWS.

El código es el mismo, solo cambia la infraestructura:
AWS = EC2 instances
Local = Docker containers
"
```

---

## 🐛 Troubleshooting

### Puerto 80 ya en uso

```bash
# Ver qué usa el puerto 80
sudo lsof -i :80

# Cambiar puerto en docker-compose.yml
ports:
  - "8080:80"

# Acceder en: http://localhost:8080
```

### Error de conexión a base de datos

```bash
# Ver logs de PostgreSQL
docker-compose logs db

# Reiniciar servicio de BD
docker-compose restart db

# Verificar que web espera a db
docker-compose logs web | grep "PostgreSQL"
```

### Los datos no persisten

```bash
# Ver volúmenes
docker volume ls

# Los datos están en:
# - postgres_data (base de datos)
# - static_volume (archivos estáticos)
# - media_volume (uploads)

# Para eliminar datos:
docker-compose down -v
```

### Permisos de archivos

```bash
# Si hay problemas de permisos
sudo chown -R $USER:$USER .
docker-compose down
docker-compose up -d --build
```

---

## 📊 Comparación: AWS vs Docker

| Aspecto | AWS EC2 | Docker Compose |
|---------|---------|----------------|
| **Setup** | ~10 min | ~2 min |
| **Costo** | Créditos AWS | Gratis |
| **Persistencia** | No (AWS Academy) | Sí |
| **Velocidad** | Depende de red | Local (rápido) |
| **Arquitectura** | 2 instancias reales | 3 contenedores |
| **Producción** | ✅ Real | ❌ Solo desarrollo |
| **Demostración** | ✅ Impresiona | ✅ Confiable |

---

## 🎯 Cuándo Usar Cada Opción

### Usar Docker Compose si:
- ✅ Tienes problemas con AWS Academy
- ✅ Necesitas demostrar rápido (evaluación)
- ✅ Desarrollo local
- ✅ Quieres algo 100% confiable

### Usar AWS EC2 si:
- ✅ El profesor requiere deployment real
- ✅ Quieres demostrar conocimientos de AWS
- ✅ Tienes tiempo para el setup
- ✅ AWS Academy está funcionando bien

### Plan Recomendado:
1. **Tener Docker Compose listo** como backup
2. **Intentar AWS Academy** primero
3. **Si AWS falla → Docker Compose** inmediatamente

---

## 🚀 Script de Inicio Rápido

Crear archivo `start.sh`:

```bash
#!/bin/bash

echo "🚀 Iniciando Logística Global Ltda..."
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

# Verificar Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado"
    exit 1
fi

# Limpiar contenedores anteriores
echo "🧹 Limpiando contenedores anteriores..."
docker-compose down -v

# Construir y levantar
echo "📦 Construyendo imágenes..."
docker-compose build

echo "🚀 Levantando servicios..."
docker-compose up -d

# Esperar a que esté listo
echo "⏳ Esperando a que los servicios estén listos..."
sleep 10

# Verificar estado
echo ""
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "✅ ¡Listo!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - Web:    http://localhost"
echo "   - API:    http://localhost/api/"
echo "   - Swagger: http://localhost/swagger/"
echo "   - Admin:  http://localhost/admin/"
echo ""
echo "🔑 Credenciales:"
echo "   Usuario:  admin"
echo "   Password: admin123"
echo ""
echo "📝 Ver logs:"
echo "   docker-compose logs -f"
echo ""
```

Uso:

```bash
chmod +x start.sh
./start.sh
```

---

## 📚 Archivos Necesarios

Asegúrate de tener:

- ✅ `docker-compose.yml` (ya creado)
- ✅ `Dockerfile` (ya creado)
- ✅ `nginx/nginx.conf` (ya creado)
- ✅ `requirements.txt` (ya existe)
- ✅ `.dockerignore` (crear si falta)

### Crear `.dockerignore`:

```bash
cat > .dockerignore << 'EOF'
*.pyc
__pycache__
*.sqlite3
*.db
venv/
.env
.git/
.gitignore
*.md
staticfiles/
media/
logs/
*.log
.DS_Store
EOF
```

---

¡Listo! Ahora tienes **Docker Compose como alternativa** confiable para demostrar tu proyecto. 🎉
