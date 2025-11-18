# 🚀 Guía Completa de Deployment para AWS - Logística Global Ltda.# Configuración de Deployment para AWS EC2 + RDS + Nginx + Gunicorn



## 📋 Arquitectura: Dos Instancias EC2## 📋 Pre-requisitos



Esta guía implementa una arquitectura de **DOS INSTANCIAS EC2 SEPARADAS** según los requerimientos de la evaluación:- Instancia EC2 (Ubuntu 20.04 o superior)

- RDS PostgreSQL (opcional)

### **INSTANCIA 1 - Servidor Web**- Dominio configurado (opcional)

- **Sistema:** Amazon Linux 2 / Ubuntu 20.04- Certificado SSL (Let's Encrypt recomendado)

- **Servicios:** Django + Gunicorn + Nginx

- **IP Pública:** Sí (acceso desde internet)---

- **IP Privada:** 10.0.1.10 (ejemplo)

- **Puertos abiertos:** 22 (SSH), 80 (HTTP), 443 (HTTPS)## 🔧 Configuración de EC2

- **Ubicación proyecto:** `/var/www/html/logistica`

### 1. Conectar a la instancia

### **INSTANCIA 2 - Servidor de Base de Datos**

- **Sistema:** Ubuntu 20.04```bash

- **Servicios:** PostgreSQL 14ssh -i tu-llave.pem ubuntu@ec2-XX-XX-XX-XX.compute-1.amazonaws.com

- **IP Pública:** NO (solo IP privada)```

- **IP Privada:** 10.0.2.50 (ejemplo)

- **Puertos abiertos:** 5432 (solo desde Instancia 1)### 2. Actualizar sistema

- **Seguridad:** No expuesta a internet

```bash

### **DuckDNS**sudo apt update

- Dominio personalizado gratuito: `logistica-global.duckdns.org`sudo apt upgrade -y# Configuración de Deployment para AWS EC2 + RDS + Nginx + Gunicorn

- Actualización automática de IP

- SSL con Let's Encrypt## 📋 Pre-requisitos



---- Instancia EC2 (Ubuntu 20.04 o superior)

- RDS PostgreSQL (opcional)

## 📚 Documentación Complementaria- Dominio configurado (opcional)

- Certificado SSL (Let's Encrypt recomendado)

Esta guía cubre la **Instancia 1 (Web)**. Para configuraciones específicas, consulta:

---

- **[INSTANCIA_BD_EC2.md](INSTANCIA_BD_EC2.md)** ⭐ - Configuración completa de la Instancia 2 con PostgreSQL

- **[DUCKDNS_SETUP.md](DUCKDNS_SETUP.md)** ⭐ - Configuración de DNS dinámico con DuckDNS y SSL## 🔧 Configuración de EC2



---### 1. Conectar a la instancia



## 🏗️ Pre-requisitos```bash

ssh -i tu-llave.pem ubuntu@ec2-XX-XX-XX-XX.compute-1.amazonaws.com

- ✅ Cuenta de AWS activa```

- ✅ 2 Instancias EC2 lanzadas (t2.micro Free Tier)

- ✅ VPC configurada con subnets pública y privada### 2. Actualizar sistema

- ✅ Llave privada (.pem) para acceso SSH

- ✅ Dominio en DuckDNS registrado (ver [DUCKDNS_SETUP.md](DUCKDNS_SETUP.md))```bash

- ✅ Instancia 2 con PostgreSQL configurada (ver [INSTANCIA_BD_EC2.md](INSTANCIA_BD_EC2.md))sudo apt update

sudo apt upgrade -y

---```



## 🌐 Paso 1: Configurar VPC y Security Groups### 3. Instalar dependencias



### 1.1. Crear VPC (si no existe)```bash

sudo apt install -y python3-pip python3-venv nginx postgresql-client git

``````

VPC Name: logistica-vpc

CIDR: 10.0.0.0/16### 4. Configurar firewall

```

```bash

### 1.2. Crear Subnetssudo ufw allow 22

sudo ufw allow 80

**Subnet Pública:**sudo ufw allow 443

```sudo ufw enable

Name: logistica-public-subnet```

CIDR: 10.0.1.0/24

Availability Zone: us-east-1a---

Auto-assign public IP: Yes

```## 📦 Deployment de la aplicación



**Subnet Privada:**### 1. Clonar repositorio

```

Name: logistica-private-subnet```bash

CIDR: 10.0.2.0/24cd /var/www

Availability Zone: us-east-1asudo mkdir html

Auto-assign public IP: Nocd html

```sudo git clone https://github.com/tu-usuario/logistica.git

sudo chown -R ubuntu:ubuntu logistica

### 1.3. Crear Internet Gatewaycd logistica

```

```

Name: logistica-igw### 2. Crear entorno virtual

Attach to: logistica-vpc

``````bash

python3 -m venv venv

### 1.4. Configurar Route Tablessource venv/bin/activate

pip install -r requirements.txt

**Route Table Pública:**```

```

Name: logistica-public-rt### 3. Configurar variables de entorno

Routes:

  - Destination: 0.0.0.0/0 → Target: logistica-igw```bash

  - Destination: 10.0.0.0/16 → Target: localsudo nano .env

Associated with: logistica-public-subnet```

```

Agregar:

**Route Table Privada:**```env

```SECRET_KEY=tu_clave_secreta_super_segura_aqui

Name: logistica-private-rtDEBUG=False

Routes:ALLOWED_HOSTS=tu-dominio.com,ec2-XX-XX-XX-XX.compute-1.amazonaws.com

  - Destination: 10.0.0.0/16 → Target: local

Associated with: logistica-private-subnetDB_ENGINE=django.db.backends.postgresql

```DB_NAME=logistica_db

DB_USER=logistica_user

### 1.5. Security GroupsDB_PASSWORD=tu_password_seguro

DB_HOST=logistica-db.xxxx.us-east-1.rds.amazonaws.com

**Security Group Web (Instancia 1):**DB_PORT=5432

``````

Name: logistica-web-sg

VPC: logistica-vpc### 4. Actualizar settings.py para usar .env



Inbound Rules:Instalar python-decouple:

  - Type: SSH, Port: 22, Source: Tu IP / 0.0.0.0/0```bash

  - Type: HTTP, Port: 80, Source: 0.0.0.0/0pip install python-decouple

  - Type: HTTPS, Port: 443, Source: 0.0.0.0/0```



Outbound Rules:En `settings.py`:

  - Type: All, Port: All, Destination: 0.0.0.0/0```python

```from decouple import config



**Security Group DB (Instancia 2):**SECRET_KEY = config('SECRET_KEY')

```DEBUG = config('DEBUG', default=False, cast=bool)

Name: logistica-db-sgALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

VPC: logistica-vpc

DATABASES = {

Inbound Rules:    'default': {

  - Type: PostgreSQL, Port: 5432, Source: logistica-web-sg (o 10.0.1.10/32)        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),

  - Type: SSH, Port: 22, Source: Tu IP (para administración)        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),

        'USER': config('DB_USER', default=''),

Outbound Rules:        'PASSWORD': config('DB_PASSWORD', default=''),

  - Type: All, Port: All, Destination: 0.0.0.0/0        'HOST': config('DB_HOST', default=''),

```        'PORT': config('DB_PORT', default=''),

    }

---}

```

## 🖥️ Paso 2: Lanzar Instancia 1 (Servidor Web)

### 5. Migraciones

### 2.1. Configuración de la instancia

```bash

```python manage.py makemigrations

AMI: Ubuntu Server 20.04 LTS (HVM), SSD Volume Typepython manage.py migrate

Instance Type: t2.micro (1 vCPU, 1 GB RAM)python manage.py collectstatic --noinput

VPC: logistica-vpcpython manage.py createsuperuser

Subnet: logistica-public-subnet (10.0.1.0/24)```

Auto-assign Public IP: Enable

Storage: 20 GB gp3---

Security Group: logistica-web-sg

Key Pair: Seleccionar o crear nueva## 🗄️ Configuración de RDS PostgreSQL

Tags:

  - Name: logistica-web-server### 1. Crear instancia RDS

  - Environment: Production

```- Engine: PostgreSQL 14.x

- Instance class: db.t3.micro (Free Tier)

### 2.2. Conectar a la instancia- Storage: 20 GB

- Username: logistica_user

```bash- Password: [tu password seguro]

# Dar permisos a la llave- VPC: Same as EC2

chmod 400 tu-llave.pem- Security Group: Allow port 5432 from EC2



# Conectar### 2. Configurar Security Group

ssh -i tu-llave.pem ubuntu@TU_IP_PUBLICA

```Inbound Rules:

```

---Type: PostgreSQL

Protocol: TCP

## 📦 Paso 3: Instalar Dependencias en Instancia 1Port: 5432

Source: [EC2 Security Group ID]

### 3.1. Actualizar sistema```



```bash### 3. Crear base de datos

sudo apt update

sudo apt upgrade -y```bash

```psql -h logistica-db.xxxx.us-east-1.rds.amazonaws.com \

     -U logistica_user \

### 3.2. Instalar Python y dependencias     -d postgres



```bashCREATE DATABASE logistica_db;

sudo apt install -y python3-pip python3-venv python3-dev\q

sudo apt install -y nginx git postgresql-client```

sudo apt install -y build-essential libpq-dev

```---



### 3.3. Configurar firewall (UFW)## 🚀 Configuración de Gunicorn



```bash### 1. Crear archivo de servicio systemd

# Habilitar UFW

sudo ufw allow 22/tcp```bash

sudo ufw allow 80/tcpsudo nano /etc/systemd/system/gunicorn.service

sudo ufw allow 443/tcp```

sudo ufw enable

Contenido:

# Verificar```ini

sudo ufw status[Unit]

```Description=Gunicorn daemon for Logistica Django app

After=network.target

---

[Service]

## 🚀 Paso 4: Clonar y Configurar ProyectoUser=ubuntu

Group=www-data

### 4.1. Crear directorio del proyectoWorkingDirectory=/var/www/html/logistica

Environment="PATH=/var/www/html/logistica/venv/bin"

```bashExecStart=/var/www/html/logistica/venv/bin/gunicorn \

sudo mkdir -p /var/www/html          --workers 3 \

cd /var/www/html          --bind unix:/var/www/html/logistica/gunicorn.sock \

```          logistica.wsgi:application



### 4.2. Clonar repositorio[Install]

WantedBy=multi-user.target

```bash```

# Opción A: Desde GitHub

sudo git clone https://github.com/tu-usuario/logistica.git### 2. Iniciar y habilitar servicio

sudo chown -R ubuntu:ubuntu logistica

```bash

# Opción B: Subir archivos con SCPsudo systemctl start gunicorn

# Desde tu máquina local:sudo systemctl enable gunicorn

# scp -i tu-llave.pem -r /ruta/local/logistica ubuntu@TU_IP_PUBLICA:/tmp/sudo systemctl status gunicorn

# sudo mv /tmp/logistica /var/www/html/```

# sudo chown -R ubuntu:ubuntu /var/www/html/logistica

```### 3. Verificar socket



### 4.3. Crear entorno virtual```bash

ls -l /var/www/html/logistica/gunicorn.sock

```bash```

cd /var/www/html/logistica

python3 -m venv venv---

source venv/bin/activate

```## 🌐 Configuración de Nginx



### 4.4. Instalar dependencias### 1. Crear configuración del sitio



```bash```bash

pip install --upgrade pipsudo nano /etc/nginx/sites-available/logistica

pip install -r requirements.txt```

```

Contenido:

---```nginx

server {

## 🔧 Paso 5: Configurar Variables de Entorno    listen 80;

    server_name tu-dominio.com www.tu-dominio.com ec2-XX-XX-XX-XX.compute-1.amazonaws.com;

### 5.1. Crear archivo .env

    location = /favicon.ico { access_log off; log_not_found off; }

```bash    

nano /var/www/html/logistica/.env    location /static/ {

```        alias /var/www/html/logistica/staticfiles/;

    }

### 5.2. Contenido del .env    

    location /media/ {

```env        alias /var/www/html/logistica/media/;

# Django Settings    }

SECRET_KEY=tu_clave_secreta_super_segura_generada_aleatoriamente

DEBUG=False    location / {

ALLOWED_HOSTS=logistica-global.duckdns.org,localhost,127.0.0.1        include proxy_params;

        proxy_pass http://unix:/var/www/html/logistica/gunicorn.sock;

# Base de datos en INSTANCIA 2 (EC2 con PostgreSQL)        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

DB_ENGINE=django.db.backends.postgresql        proxy_set_header Host $host;

DB_NAME=logistica_db        proxy_redirect off;

DB_USER=logistica_user    }

DB_PASSWORD=TuPasswordSeguro2025!}

DB_HOST=10.0.2.50```

DB_PORT=5432

### 2. Habilitar sitio

# Seguridad HTTPS

SECURE_SSL_REDIRECT=True```bash

SESSION_COOKIE_SECURE=Truesudo ln -s /etc/nginx/sites-available/logistica /etc/nginx/sites-enabled/

CSRF_COOKIE_SECURE=Truesudo nginx -t

```sudo systemctl restart nginx

```

**⚠️ IMPORTANTE:**

- Reemplazar `10.0.2.50` con la IP privada real de tu Instancia 2---

- Generar SECRET_KEY único: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`

## 🔒 Configuración SSL con Let's Encrypt

### 5.3. Instalar python-decouple

### 1. Instalar Certbot

```bash

pip install python-decouple```bash

```sudo apt install -y certbot python3-certbot-nginx

```

### 5.4. Actualizar settings.py

### 2. Obtener certificado

```bash

nano logistica/settings.py```bash

```sudo certbot --nginx -d tu-dominio.com -d www.tu-dominio.com

```

Asegurarse de tener:

### 3. Verificar renovación automática

```python

from decouple import config```bash

import ossudo certbot renew --dry-run

```

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)La configuración de Nginx se actualizará automáticamente para usar HTTPS.

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

---

DATABASES = {

    'default': {## 📊 Monitoreo y Logs

        'ENGINE': config('DB_ENGINE', default='django.db.backends.sqlite3'),

        'NAME': config('DB_NAME', default=BASE_DIR / 'db.sqlite3'),### Ver logs de Gunicorn

        'USER': config('DB_USER', default=''),

        'PASSWORD': config('DB_PASSWORD', default=''),```bash

        'HOST': config('DB_HOST', default=''),sudo journalctl -u gunicorn -f

        'PORT': config('DB_PORT', default=''),```

    }

}### Ver logs de Nginx



# Configuración para archivos estáticos en producción```bash

STATIC_ROOT = '/var/www/html/logistica/staticfiles/'sudo tail -f /var/log/nginx/error.log

STATIC_URL = '/static/'sudo tail -f /var/log/nginx/access.log

```

# Seguridad en producción

if not DEBUG:### Ver logs de Django

    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)

    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)```bash

    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)tail -f /var/www/html/logistica/logs/django.log

    SECURE_BROWSER_XSS_FILTER = True```

    SECURE_CONTENT_TYPE_NOSNIFF = True

    X_FRAME_OPTIONS = 'DENY'Crear directorio de logs:

``````bash

mkdir -p /var/www/html/logistica/logs

---```



## 🗄️ Paso 6: Configurar Base de Datos---



### 6.1. Verificar conexión a Instancia 2## 🔄 Comandos útiles de mantenimiento



```bash### Reiniciar Gunicorn

# Probar conexión a PostgreSQL en Instancia 2

psql -h 10.0.2.50 -U logistica_user -d logistica_db```bash

sudo systemctl restart gunicorn

# Si conecta correctamente, ¡perfecto! (Ctrl+D para salir)```

```

### Reiniciar Nginx

Si falla, revisar [INSTANCIA_BD_EC2.md](INSTANCIA_BD_EC2.md) para configurar la Instancia 2.

```bash

### 6.2. Ejecutar migracionessudo systemctl restart nginx

```

```bash

cd /var/www/html/logistica### Actualizar código desde Git

source venv/bin/activate

```bash

python manage.py makemigrationscd /var/www/html/logistica

python manage.py migrategit pull origin main

```source venv/bin/activate

pip install -r requirements.txt

### 6.3. Recolectar archivos estáticospython manage.py migrate

python manage.py collectstatic --noinput

```bashsudo systemctl restart gunicorn

python manage.py collectstatic --noinput```

```

### Backup de base de datos

### 6.4. Crear superusuario

```bash

```bashpython manage.py dumpdata > backup_$(date +%Y%m%d).json

python manage.py createsuperuser```

# Usuario: admin

# Email: admin@logisticaglobal.cl### Restore de base de datos

# Password: [tu password seguro]

``````bash

python manage.py loaddata backup_20251111.json

### 6.5. Cargar datos iniciales```



```bash---

python load_data.py

```## 🔐 Seguridad adicional



---### 1. Configurar HTTPS redirect en settings.py



## 🦄 Paso 7: Configurar Gunicorn```python

SECURE_SSL_REDIRECT = True

### 7.1. Crear archivo de servicio systemdSESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

```bashSECURE_BROWSER_XSS_FILTER = True

sudo nano /etc/systemd/system/gunicorn.serviceSECURE_CONTENT_TYPE_NOSNIFF = True

```X_FRAME_OPTIONS = 'DENY'

SECURE_HSTS_SECONDS = 31536000

### 7.2. Contenido del archivoSECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_HSTS_PRELOAD = True

```ini```

[Unit]

Description=Gunicorn daemon for Logistica Django app### 2. Configurar CORS para producción

After=network.target

```python

[Service]CORS_ALLOWED_ORIGINS = [

User=ubuntu    "https://tu-dominio.com",

Group=www-data    "https://www.tu-dominio.com",

WorkingDirectory=/var/www/html/logistica]

Environment="PATH=/var/www/html/logistica/venv/bin"CORS_ALLOW_ALL_ORIGINS = False

ExecStart=/var/www/html/logistica/venv/bin/gunicorn \```

          --workers 3 \

          --bind unix:/var/www/html/logistica/gunicorn.sock \### 3. Limitar acceso a admin

          logistica.wsgi:application

En Nginx:

[Install]```nginx

WantedBy=multi-user.targetlocation /admin {

```    allow TU_IP;

    deny all;

### 7.3. Crear directorio para socket    include proxy_params;

    proxy_pass http://unix:/var/www/html/logistica/gunicorn.sock;

```bash}

sudo mkdir -p /var/www/html/logistica```

sudo chown -R ubuntu:www-data /var/www/html/logistica

```---



### 7.4. Iniciar y habilitar servicio## 📈 Optimizaciones



```bash### 1. Cache con Redis (opcional)

sudo systemctl start gunicorn

sudo systemctl enable gunicorn```bash

sudo systemctl status gunicornsudo apt install redis-server

```pip install django-redis

```

Deberías ver: `Active: active (running)`

En settings.py:

### 7.5. Verificar socket```python

CACHES = {

```bash    'default': {

ls -l /var/www/html/logistica/gunicorn.sock        'BACKEND': 'django_redis.cache.RedisCache',

# Debería existir: srwxrwxrwx ... gunicorn.sock        'LOCATION': 'redis://127.0.0.1:6379/1',

```        'OPTIONS': {

            'CLIENT_CLASS': 'django_redis.client.DefaultClient',

---        }

    }

## 🌐 Paso 8: Configurar Nginx}

```

### 8.1. Eliminar configuración por defecto

### 2. Aumentar workers de Gunicorn

```bash

sudo rm /etc/nginx/sites-enabled/defaultFórmula: (2 x CPU cores) + 1

```

Para t2.micro (1 CPU):

### 8.2. Crear configuración para el proyecto```ini

ExecStart=/var/www/html/logistica/venv/bin/gunicorn \

```bash          --workers 3 \

sudo nano /etc/nginx/sites-available/logistica          --threads 2 \

```          --bind unix:/var/www/html/logistica/gunicorn.sock \

          logistica.wsgi:application

### 8.3. Contenido del archivo (SIN SSL - configuraremos después)```



```nginx---

server {

    listen 80;## ✅ Checklist de Deployment

    server_name logistica-global.duckdns.org;

- [ ] Instancia EC2 configurada

    client_max_body_size 10M;- [ ] RDS PostgreSQL creado (opcional)

- [ ] Código clonado en `/var/www/html/logistica`

    location = /favicon.ico { - [ ] Entorno virtual creado

        access_log off; - [ ] Dependencias instaladas

        log_not_found off; - [ ] Variables de entorno configuradas (.env)

    }- [ ] Migraciones ejecutadas

    - [ ] Archivos estáticos recolectados

    location /static/ {- [ ] Gunicorn configurado y funcionando

        alias /var/www/html/logistica/staticfiles/;- [ ] Nginx configurado y funcionando

        expires 30d;- [ ] SSL instalado (Let's Encrypt)

        add_header Cache-Control "public, immutable";- [ ] Firewall configurado (UFW)

    }- [ ] Security Groups configurados

    - [ ] Backup programado

    location /media/ {- [ ] Monitoring configurado

        alias /var/www/html/logistica/media/;

        expires 30d;---

        add_header Cache-Control "public";

    }## 🆘 Troubleshooting



    location / {### Error: Bad Gateway 502

        include proxy_params;

        proxy_pass http://unix:/var/www/html/logistica/gunicorn.sock;```bash

        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;sudo systemctl status gunicorn

        proxy_set_header Host $host;sudo journalctl -u gunicorn -n 50

        proxy_set_header X-Forwarded-Proto $scheme;```

        proxy_redirect off;

        Verificar socket:

        # Timeouts```bash

        proxy_connect_timeout 60s;ls -l /var/www/html/logistica/gunicorn.sock

        proxy_send_timeout 60s;```

        proxy_read_timeout 60s;

    }### Error: Static files not found

}

``````bash

python manage.py collectstatic --noinput

**⚠️ IMPORTANTE:** Reemplaza `logistica-global.duckdns.org` con tu dominio real de DuckDNS.sudo systemctl restart nginx

```

### 8.4. Habilitar sitio

### Error: Database connection

```bash

sudo ln -s /etc/nginx/sites-available/logistica /etc/nginx/sites-enabled/Verificar credenciales en .env y security group de RDS.

```

```bash

### 8.5. Probar configuraciónpsql -h [RDS_ENDPOINT] -U logistica_user -d logistica_db

```

```bash

sudo nginx -t---

```

## 📞 Recursos adicionales

Deberías ver: `nginx: configuration file /etc/nginx/nginx.conf test is successful`

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)

### 8.6. Reiniciar Nginx- [AWS EC2 Docs](https://docs.aws.amazon.com/ec2/)

- [AWS RDS Docs](https://docs.aws.amazon.com/rds/)

```bash- [Gunicorn Docs](https://docs.gunicorn.org/)

sudo systemctl restart nginx- [Nginx Docs](https://nginx.org/en/docs/)

sudo systemctl enable nginx
sudo systemctl status nginx
```

---

## 🦆 Paso 9: Configurar DuckDNS

**⚠️ Este paso es CRÍTICO para cumplir con los requerimientos.**

Consulta la guía completa: **[DUCKDNS_SETUP.md](DUCKDNS_SETUP.md)**

Resumen rápido:

```bash
# 1. Registrar dominio en https://www.duckdns.org/
# 2. Crear script de actualización
mkdir ~/duckdns
nano ~/duckdns/duck.sh

# Contenido:
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=logistica-global&token=TU_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -

# 3. Dar permisos
chmod 700 ~/duckdns/duck.sh

# 4. Configurar cron
crontab -e
# Agregar: */5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1

# 5. Probar
./duck.sh
cat duck.log  # Debería mostrar "OK"
```

---

## 🔒 Paso 10: Configurar SSL con Let's Encrypt

### 10.1. Instalar Certbot

```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 10.2. Obtener certificado

```bash
sudo certbot --nginx -d logistica-global.duckdns.org
```

Responder:
- Email: Tu correo
- Términos: A (Agree)
- Compartir email: N (No)
- Redirect HTTP to HTTPS: 2 (Yes)

### 10.3. Verificar certificado

```bash
sudo certbot certificates
```

### 10.4. Probar renovación automática

```bash
sudo certbot renew --dry-run
```

---

## ✅ Paso 11: Verificar Funcionamiento

### 11.1. Acceder al sitio

Abre tu navegador:

```
https://logistica-global.duckdns.org
```

Deberías ver la página principal de Logística Global Ltda. 🎉

### 11.2. Probar endpoints

```bash
# Admin
https://logistica-global.duckdns.org/admin/

# API
https://logistica-global.duckdns.org/api/

# Swagger
https://logistica-global.duckdns.org/swagger/

# Obtener token JWT
curl -X POST https://logistica-global.duckdns.org/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"tu_password"}'
```

---

## 🔄 Comandos de Mantenimiento

### Actualizar código desde Git

```bash
cd /var/www/html/logistica
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Ver logs

```bash
# Logs de Gunicorn
sudo journalctl -u gunicorn -f

# Logs de Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Logs de Django
tail -f /var/www/html/logistica/logs/django.log  # Si está configurado
```

### Reiniciar servicios

```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
sudo systemctl status gunicorn
sudo systemctl status nginx
```

### Backup de base de datos

```bash
# Crear backup
pg_dump -h 10.0.2.50 -U logistica_user logistica_db > backup_$(date +%Y%m%d).sql

# Comprimir
gzip backup_$(date +%Y%m%d).sql

# Descargar a tu máquina local
# scp -i tu-llave.pem ubuntu@TU_IP:/ruta/backup.sql.gz ./
```

---

## 📊 Arquitectura Final

```
┌────────────────────────────────────────────────────────────┐
│                    INTERNET                                │
│                        │                                   │
│              ┌─────────▼──────────┐                        │
│              │   DuckDNS          │                        │
│              │   *.duckdns.org    │                        │
│              └─────────┬──────────┘                        │
│                        │                                   │
└────────────────────────┼────────────────────────────────────┘
                         │
                         │ HTTPS (443)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    AWS VPC (10.0.0.0/16)                    │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         SUBNET PÚBLICA (10.0.1.0/24)                 │  │
│  │                                                      │  │
│  │  ┌────────────────────────────────────────────┐     │  │
│  │  │      INSTANCIA 1 (Web Server)             │     │  │
│  │  │      IP Pública: XX.XX.XX.XX              │     │  │
│  │  │      IP Privada: 10.0.1.10                │     │  │
│  │  │                                           │     │  │
│  │  │  ┌──────────┐   ┌──────────┐            │     │  │
│  │  │  │  Nginx   │──▶│ Gunicorn │            │     │  │
│  │  │  │  (80/443)│   │  (sock)  │            │     │  │
│  │  │  └──────────┘   └─────┬────┘            │     │  │
│  │  │                       │                  │     │  │
│  │  │                 ┌─────▼────────┐         │     │  │
│  │  │                 │    Django    │         │     │  │
│  │  │                 │  (Logística) │         │     │  │
│  │  │                 └──────────────┘         │     │  │
│  │  └───────────────────────┬───────────────────┘     │  │
│  └────────────────────────│──────────────────────────┘  │
│                           │                             │
│                           │ PostgreSQL (5432)           │
│                           │ IP Privada                  │
│  ┌────────────────────────▼──────────────────────────┐  │
│  │         SUBNET PRIVADA (10.0.2.0/24)             │  │
│  │                                                  │  │
│  │  ┌────────────────────────────────────────┐     │  │
│  │  │   INSTANCIA 2 (Database Server)       │     │  │
│  │  │   IP Privada: 10.0.2.50               │     │  │
│  │  │   SIN IP Pública                      │     │  │
│  │  │                                       │     │  │
│  │  │  ┌──────────────────────────┐         │     │  │
│  │  │  │     PostgreSQL 14        │         │     │  │
│  │  │  │   logistica_db           │         │     │  │
│  │  │  │   (puerto 5432)          │         │     │  │
│  │  │  └──────────────────────────┘         │     │  │
│  │  └────────────────────────────────────────┘     │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘

Seguridad:
✅ Instancia 1: Puertos 22, 80, 443 abiertos al mundo
✅ Instancia 2: Puerto 5432 solo desde 10.0.1.10
✅ Base de datos NO expuesta a internet
✅ Comunicación interna por IP privada
✅ HTTPS con Let's Encrypt
✅ DNS dinámico con DuckDNS
```

---

## 🆘 Troubleshooting

### Gunicorn no inicia

```bash
# Ver logs detallados
sudo journalctl -u gunicorn -n 50 --no-pager

# Verificar socket
ls -l /var/www/html/logistica/gunicorn.sock

# Verificar permisos
sudo chown -R ubuntu:www-data /var/www/html/logistica

# Reintentar
sudo systemctl restart gunicorn
```

### Nginx muestra 502 Bad Gateway

```bash
# Verificar que Gunicorn está corriendo
sudo systemctl status gunicorn

# Verificar socket existe
ls -l /var/www/html/logistica/gunicorn.sock

# Ver logs
sudo tail -f /var/log/nginx/error.log
```

### No se puede conectar a la base de datos

```bash
# Probar conexión manualmente
psql -h 10.0.2.50 -U logistica_user -d logistica_db

# Verificar Security Group de Instancia 2
# Debe permitir puerto 5432 desde 10.0.1.10

# Verificar .env
cat /var/www/html/logistica/.env | grep DB_
```

### SSL no funciona

```bash
# Verificar que DuckDNS está configurado
curl "https://www.duckdns.org/update?domains=logistica-global&token=TU_TOKEN&ip="

# Verificar que dominio resuelve
ping logistica-global.duckdns.org

# Reinstalar certificado
sudo certbot --nginx -d logistica-global.duckdns.org --force-renewal
```

---

## ✅ Checklist de Deployment Completo

### VPC y Red
- [ ] VPC creada (10.0.0.0/16)
- [ ] Subnet pública creada (10.0.1.0/24)
- [ ] Subnet privada creada (10.0.2.0/24)
- [ ] Internet Gateway configurado
- [ ] Route Tables configuradas
- [ ] Security Groups creados

### Instancia 1 (Web)
- [ ] EC2 lanzada en subnet pública
- [ ] IP pública asignada
- [ ] Security Group: 22, 80, 443
- [ ] Python 3, pip, venv instalados
- [ ] Nginx instalado
- [ ] Git instalado
- [ ] Proyecto clonado en `/var/www/html/logistica`
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] .env configurado
- [ ] Migraciones ejecutadas
- [ ] Archivos estáticos recolectados
- [ ] Superusuario creado
- [ ] Datos iniciales cargados
- [ ] Gunicorn configurado y corriendo
- [ ] Nginx configurado y corriendo

### Instancia 2 (Base de Datos)
- [ ] EC2 lanzada en subnet privada
- [ ] SIN IP pública
- [ ] Security Group: 5432 desde Instancia 1
- [ ] PostgreSQL 14 instalado
- [ ] postgresql.conf configurado
- [ ] pg_hba.conf configurado
- [ ] Usuario logistica_user creado
- [ ] Base de datos logistica_db creada
- [ ] Conexión probada desde Instancia 1
- [ ] Backup automático configurado

### DuckDNS y SSL
- [ ] Dominio registrado en DuckDNS
- [ ] Script duck.sh configurado
- [ ] Cron configurado (actualización cada 5 min)
- [ ] Nginx con server_name correcto
- [ ] Certbot instalado
- [ ] Certificado SSL obtenido
- [ ] HTTPS funcionando
- [ ] Redirect HTTP → HTTPS activo

### Aplicación
- [ ] Sitio accesible vía HTTPS
- [ ] Admin Django funcional
- [ ] API REST funcional
- [ ] Swagger UI accesible
- [ ] JWT autenticación funcional
- [ ] Templates HTML funcionando
- [ ] Archivos estáticos sirviendo correctamente

---

## 🎉 ¡Deployment Completado!

Tu aplicación ahora está:

✅ **Corriendo en producción con 2 instancias EC2**
✅ **Base de datos segura (no expuesta a internet)**
✅ **Dominio personalizado con DuckDNS**
✅ **HTTPS con certificado válido**
✅ **Arquitectura escalable y segura**

### URLs finales:

- 🌐 **Sitio Web:** https://logistica-global.duckdns.org
- 🔐 **Admin:** https://logistica-global.duckdns.org/admin/
- 🔌 **API:** https://logistica-global.duckdns.org/api/
- 📖 **Swagger:** https://logistica-global.duckdns.org/swagger/
- 🔑 **JWT Token:** https://logistica-global.duckdns.org/api/token/

---

## 📚 Documentación Adicional

- [INSTANCIA_BD_EC2.md](INSTANCIA_BD_EC2.md) - Configuración detallada de PostgreSQL en EC2
- [DUCKDNS_SETUP.md](DUCKDNS_SETUP.md) - Configuración completa de DuckDNS y SSL
- [README.md](README.md) - Documentación general del proyecto
- [ANALISIS_CUMPLIMIENTO.md](ANALISIS_CUMPLIMIENTO.md) - Verificación de requerimientos

¡Tu proyecto cumple 100% con los requerimientos de la evaluación! 🚀
