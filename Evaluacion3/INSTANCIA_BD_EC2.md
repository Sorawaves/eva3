# 🗄️ Configuración de Instancia 2: Base de Datos PostgreSQL en EC2

## 📋 Descripción

Esta guía detalla la configuración de la **segunda instancia EC2** que funcionará como servidor de base de datos PostgreSQL. Esta instancia NO debe estar expuesta a internet y solo debe aceptar conexiones desde la instancia web.

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────┐
│                    VPC                          │
│                 10.0.0.0/16                     │
│                                                 │
│  ┌──────────────────┐    ┌──────────────────┐  │
│  │  SUBNET PÚBLICA  │    │  SUBNET PRIVADA  │  │
│  │   10.0.1.0/24    │    │   10.0.2.0/24    │  │
│  │                  │    │                  │  │
│  │  ┌────────────┐  │    │  ┌────────────┐  │  │
│  │  │ INSTANCIA 1│  │    │  │ INSTANCIA 2│  │  │
│  │  │    (Web)   │──────────│    (BD)    │  │  │
│  │  │            │  │    │  │            │  │  │
│  │  │ Nginx      │  │    │  │ PostgreSQL │  │  │
│  │  │ Gunicorn   │  │    │  │            │  │  │
│  │  │ Django     │  │    │  │            │  │  │
│  │  └────────────┘  │    │  └────────────┘  │  │
│  │  IP: 10.0.1.10   │    │  IP: 10.0.2.50   │  │
│  │  Pública: Sí     │    │  Pública: NO     │  │
│  └──────────────────┘    └──────────────────┘  │
│         ↓                                       │
│    Internet Gateway                             │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Paso 1: Lanzar Instancia EC2 para Base de Datos

### 1.1. Configuración de la instancia

```
AMI:              Ubuntu Server 20.04 LTS (HVM), SSD Volume Type
Instance Type:    t2.micro (Free Tier eligible)
VPC:              Misma VPC que la instancia web
Subnet:           Subnet privada (10.0.2.0/24)
Auto-assign IP:   DISABLE (No necesita IP pública)
Storage:          20 GB gp3
```

### 1.2. Configurar Security Group

**Nombre:** `logistica-db-sg`

**Inbound Rules:**

| Type       | Protocol | Port | Source               | Descripción                    |
|------------|----------|------|----------------------|--------------------------------|
| PostgreSQL | TCP      | 5432 | 10.0.1.10/32         | Solo instancia web             |
| SSH        | TCP      | 22   | Tu IP / Bastion Host | Administración (temporal)      |

**Outbound Rules:**

| Type       | Protocol | Port | Destination | Descripción        |
|------------|----------|------|-------------|--------------------|
| All        | All      | All  | 0.0.0.0/0   | Permitir salida    |

### 1.3. Key Pair

Usar la misma llave `.pem` que usas para la instancia web, o crear una nueva específica para BD.

---

## 🔧 Paso 2: Conectar a la Instancia

### Opción A: Conexión directa (si tiene IP pública temporal)

```bash
ssh -i tu-llave.pem ubuntu@IP_PUBLICA_TEMPORAL
```

### Opción B: Conexión a través de Bastion Host

```bash
# Desde tu máquina local
ssh -i tu-llave.pem -L 2222:10.0.2.50:22 ubuntu@IP_INSTANCIA_WEB

# En otra terminal
ssh -p 2222 ubuntu@localhost
```

### Opción C: Session Manager (recomendado)

```bash
# Instalar AWS CLI y Session Manager Plugin
aws ssm start-session --target i-INSTANCE_ID_DE_BD
```

---

## 📦 Paso 3: Instalar PostgreSQL

### 3.1. Actualizar sistema

```bash
sudo apt update
sudo apt upgrade -y
```

### 3.2. Instalar PostgreSQL 14

```bash
# Instalar PostgreSQL
sudo apt install -y postgresql-14 postgresql-contrib-14

# Verificar instalación
sudo systemctl status postgresql
```

### 3.3. Verificar versión

```bash
psql --version
# Debería mostrar: psql (PostgreSQL) 14.x
```

---

## 🔐 Paso 4: Configurar PostgreSQL

### 4.1. Editar postgresql.conf

```bash
sudo nano /etc/postgresql/14/main/postgresql.conf
```

**Cambios a realizar:**

```ini
# Escuchar en todas las interfaces de red
listen_addresses = '*'                  # Cambiar de 'localhost' a '*'

# Ajustar para mejor rendimiento (t2.micro tiene ~1GB RAM)
shared_buffers = 128MB
effective_cache_size = 512MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 4MB
default_statistics_target = 100
random_page_cost = 1.1
work_mem = 4MB
min_wal_size = 1GB
max_wal_size = 4GB

# Logging para producción
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'mod'                   # Log INSERT, UPDATE, DELETE
log_duration = on
log_line_prefix = '%m [%p] %u@%d '
```

### 4.2. Editar pg_hba.conf

```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

**Agregar al final del archivo:**

```conf
# Configuración de acceso para la instancia web
# TYPE  DATABASE        USER              ADDRESS           METHOD

# Permitir conexión desde la instancia web (IP privada)
host    logistica_db    logistica_user    10.0.1.10/32      md5

# Permitir conexión desde toda la subnet privada (opcional)
host    logistica_db    logistica_user    10.0.1.0/24       md5

# Conexión local
local   all             all                                 peer
host    all             all               127.0.0.1/32      md5
host    all             all               ::1/128           md5
```

### 4.3. Reiniciar PostgreSQL

```bash
sudo systemctl restart postgresql
sudo systemctl enable postgresql
sudo systemctl status postgresql
```

---

## 👤 Paso 5: Crear Usuario y Base de Datos

### 5.1. Acceder a PostgreSQL

```bash
sudo -u postgres psql
```

### 5.2. Crear usuario

```sql
-- Crear usuario con contraseña segura
CREATE USER logistica_user WITH PASSWORD 'TuPasswordSeguro2025!';

-- Otorgar permisos para crear bases de datos (útil para migraciones)
ALTER USER logistica_user CREATEDB;
```

### 5.3. Crear base de datos

```sql
-- Crear base de datos
CREATE DATABASE logistica_db OWNER logistica_user;

-- Otorgar todos los privilegios
GRANT ALL PRIVILEGES ON DATABASE logistica_db TO logistica_user;

-- Salir
\q
```

### 5.4. Verificar conexión

```bash
# Conectar como el usuario creado
psql -U logistica_user -d logistica_db -h localhost

# Si funciona, verás:
# logistica_db=>
```

---

## 🔒 Paso 6: Configurar Firewall (UFW)

```bash
# Habilitar UFW
sudo ufw enable

# Permitir SSH (importante: hacerlo ANTES de habilitar)
sudo ufw allow 22/tcp

# Permitir PostgreSQL solo desde la instancia web
sudo ufw allow from 10.0.1.10 to any port 5432

# Verificar reglas
sudo ufw status numbered

# Debería mostrar:
# Status: active
#
#      To                         Action      From
#      --                         ------      ----
# [ 1] 22/tcp                     ALLOW IN    Anywhere
# [ 2] 5432                       ALLOW IN    10.0.1.10
```

---

## 🔌 Paso 7: Configurar Conexión desde Instancia Web

### 7.1. Obtener IP privada de la instancia BD

```bash
# Desde la instancia BD
ip addr show eth0 | grep "inet " | awk '{print $2}' | cut -d/ -f1

# O desde AWS Console: EC2 > Instancia BD > Detalles > Private IPv4 address
# Ejemplo: 10.0.2.50
```

### 7.2. Probar conexión desde instancia web

```bash
# Conectar a la instancia WEB
ssh -i tu-llave.pem ubuntu@IP_PUBLICA_WEB

# Instalar cliente PostgreSQL
sudo apt install -y postgresql-client

# Probar conexión a la BD
psql -h 10.0.2.50 -U logistica_user -d logistica_db

# Si pide contraseña y conecta, ¡perfecto!
```

### 7.3. Actualizar .env en instancia web

```bash
# En la instancia WEB: /var/www/html/logistica/.env
nano /var/www/html/logistica/.env
```

Actualizar con:

```env
# Base de datos en INSTANCIA 2 (EC2 con PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=logistica_db
DB_USER=logistica_user
DB_PASSWORD=TuPasswordSeguro2025!
DB_HOST=10.0.2.50          # IP PRIVADA de la instancia BD
DB_PORT=5432
```

### 7.4. Actualizar settings.py

```python
# logistica/settings.py
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': config('DB_USER', default=''),
        'PASSWORD': config('DB_PASSWORD', default=''),
        'HOST': config('DB_HOST', default=''),
        'PORT': config('DB_PORT', default=''),
    }
}
```

---

## 🚀 Paso 8: Migrar Base de Datos

```bash
# En la instancia WEB
cd /var/www/html/logistica
source venv/bin/activate

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Cargar datos iniciales
python load_data.py

# Verificar
python manage.py dbshell
```

En psql:

```sql
-- Ver tablas creadas
\dt

-- Ver datos
SELECT COUNT(*) FROM transporte_vehiculo;
SELECT COUNT(*) FROM transporte_despacho;

-- Salir
\q
```

---

## 🔐 Paso 9: Seguridad Adicional

### 9.1. Cambiar contraseña de postgres

```bash
sudo -u postgres psql

ALTER USER postgres PASSWORD 'OtraPasswordSegura2025!';
\q
```

### 9.2. Deshabilitar acceso remoto a postgres

```bash
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

Asegurarse que postgres solo puede conectar localmente:

```conf
# postgres solo puede conectar localmente
local   all             postgres                                peer
```

### 9.3. Backup automático

Crear script de backup:

```bash
sudo nano /usr/local/bin/backup-logistica.sh
```

Contenido:

```bash
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/logistica_backup_$DATE.sql"

mkdir -p $BACKUP_DIR

# Crear backup
pg_dump -U logistica_user -h localhost logistica_db > $BACKUP_FILE

# Comprimir
gzip $BACKUP_FILE

# Eliminar backups antiguos (mantener últimos 7 días)
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete

echo "Backup completado: ${BACKUP_FILE}.gz"
```

Dar permisos:

```bash
sudo chmod +x /usr/local/bin/backup-logistica.sh
```

Configurar cron:

```bash
crontab -e

# Agregar (backup diario a las 3 AM)
0 3 * * * /usr/local/bin/backup-logistica.sh >> /home/ubuntu/backups/backup.log 2>&1
```

---

## 📊 Paso 10: Monitoreo

### Ver logs de PostgreSQL

```bash
sudo tail -f /var/log/postgresql/postgresql-14-main.log
```

### Ver conexiones activas

```bash
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

### Ver tamaño de la base de datos

```bash
sudo -u postgres psql -c "SELECT pg_size_pretty(pg_database_size('logistica_db'));"
```

---

## 🆘 Troubleshooting

### Error: No se puede conectar desde instancia web

**1. Verificar Security Group:**

```bash
# Desde AWS Console
EC2 > Security Groups > logistica-db-sg
# Asegurarse que puerto 5432 está abierto para 10.0.1.10
```

**2. Verificar UFW:**

```bash
sudo ufw status
# Debe mostrar: 5432 ALLOW IN 10.0.1.10
```

**3. Verificar postgresql.conf:**

```bash
sudo grep listen_addresses /etc/postgresql/14/main/postgresql.conf
# Debe mostrar: listen_addresses = '*'
```

**4. Verificar pg_hba.conf:**

```bash
sudo grep 10.0.1.10 /etc/postgresql/14/main/pg_hba.conf
# Debe tener línea con: host logistica_db logistica_user 10.0.1.10/32 md5
```

### Error: Autenticación fallida

```bash
# Resetear contraseña
sudo -u postgres psql
ALTER USER logistica_user PASSWORD 'NuevaPasswordSegura2025!';
\q

# Actualizar .env en instancia web
```

### Error: Base de datos no existe

```bash
sudo -u postgres psql
CREATE DATABASE logistica_db OWNER logistica_user;
GRANT ALL PRIVILEGES ON DATABASE logistica_db TO logistica_user;
\q
```

---

## ✅ Checklist de Verificación

- [ ] Instancia EC2 lanzada en subnet privada
- [ ] PostgreSQL 14 instalado
- [ ] postgresql.conf configurado (listen_addresses = '*')
- [ ] pg_hba.conf configurado con IP de instancia web
- [ ] Usuario logistica_user creado
- [ ] Base de datos logistica_db creada
- [ ] Security Group permite puerto 5432 desde instancia web
- [ ] UFW configurado
- [ ] Conexión probada desde instancia web
- [ ] Migraciones ejecutadas exitosamente
- [ ] Datos iniciales cargados
- [ ] Backup automático configurado
- [ ] Sin IP pública asignada (seguridad)

---

## 🎯 Resultado Final

Ahora tienes:

✅ **Instancia 1 (Web):**
- IP Pública: Para acceso desde internet
- IP Privada: 10.0.1.10
- Servicios: Nginx, Gunicorn, Django
- Puertos abiertos: 22, 80, 443

✅ **Instancia 2 (Base de Datos):**
- IP Pública: **NO** (seguridad)
- IP Privada: 10.0.2.50
- Servicios: PostgreSQL 14
- Puertos abiertos: Solo 5432 desde 10.0.1.10

✅ **Arquitectura segura:**
- Base de datos NO expuesta a internet
- Comunicación interna por IP privada
- Security Groups segmentados
- Backups automáticos

---

## 📞 Connection String Final

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=logistica_db
DB_USER=logistica_user
DB_PASSWORD=TuPasswordSeguro2025!
DB_HOST=10.0.2.50
DB_PORT=5432
```

¡Tu arquitectura de dos instancias EC2 está completa! 🎉
