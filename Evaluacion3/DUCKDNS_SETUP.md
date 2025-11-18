# 🦆 Configuración de DuckDNS para Logística Global Ltda.

## 📋 ¿Qué es DuckDNS?

DuckDNS es un servicio **gratuito** de DNS dinámico que te permite:
- Tener un dominio personalizado (ejemplo: `logistica-global.duckdns.org`)
- Apuntar tu dominio a la IP pública de tu instancia EC2
- Actualizar automáticamente la IP cuando cambie
- No depender de IPs públicas difíciles de recordar

---

## 🚀 Paso 1: Registrar Dominio en DuckDNS

### 1.1. Crear cuenta

1. Ve a: **https://www.duckdns.org/**
2. Inicia sesión con una de estas opciones:
   - GitHub
   - Google
   - Reddit
   - Twitter

### 1.2. Crear tu dominio

1. En el campo "sub domain", escribe tu nombre deseado:
   ```
   logistica-global
   ```

2. Haz clic en **"add domain"**

3. Tu dominio será:
   ```
   logistica-global.duckdns.org
   ```

### 1.3. Obtener token

En la página principal de DuckDNS verás:
```
token: a7c4d0ad-114e-40ef-ba1d-d217904a50f2
```

**⚠️ IMPORTANTE:** Guarda este token de forma segura. Lo necesitarás para la configuración.

---

## 🔧 Paso 2: Configurar IP Inicial

### 2.1. Obtener IP pública de tu instancia EC2

```bash
# Opción 1: Desde AWS Console
# EC2 > Instancias > Tu instancia > Public IPv4 address

# Opción 2: Desde la instancia
curl http://checkip.amazonaws.com

# Ejemplo de salida: 54.123.45.67
```

### 2.2. Actualizar IP manualmente (primera vez)

En la página de DuckDNS:
1. Selecciona tu dominio (`logistica-global`)
2. En el campo "current ip", verás tu IP actual detectada
3. Haz clic en **"update ip"**

Tu dominio ahora apunta a tu instancia EC2. ✅

---

## 🤖 Paso 3: Configurar Actualización Automática en EC2

### 3.1. Conectar a tu instancia

```bash
ssh -i tu-llave.pem ubuntu@TU_IP_PUBLICA
```

### 3.2. Crear directorio para DuckDNS

```bash
mkdir -p ~/duckdns
cd ~/duckdns
```

### 3.3. Crear script de actualización

```bash
nano duck.sh
```

**Contenido del archivo:**

```bash
#!/bin/bash

# Configuración
DOMAIN="logistica-global"
TOKEN="a7c4d0ad-114e-40ef-ba1d-d217904a50f2"  # ⚠️ REEMPLAZAR con tu token

# Actualizar IP en DuckDNS
echo url="https://www.duckdns.org/update?domains=${DOMAIN}&token=${TOKEN}&ip=" | curl -k -o ~/duckdns/duck.log -K -

# Registrar timestamp
echo "$(date): IP actualizada" >> ~/duckdns/duck.log
```

**⚠️ REEMPLAZA:**
- `logistica-global` con tu dominio
- `a7c4d0ad-114e-40ef-ba1d-d217904a50f2` con tu token real

### 3.4. Dar permisos de ejecución

```bash
chmod 700 ~/duckdns/duck.sh
```

### 3.5. Probar el script

```bash
./duck.sh
```

Verificar resultado:

```bash
cat duck.log
```

Deberías ver: `OK` (significa que funcionó) ✅

---

## ⏰ Paso 4: Configurar Actualización Automática (Cron)

### 4.1. Editar crontab

```bash
crontab -e
```

Si es la primera vez, te preguntará qué editor usar. Elige `nano` (opción 1).

### 4.2. Agregar tarea programada

Al final del archivo, agrega:

```bash
# Actualizar DuckDNS cada 5 minutos
*/5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
```

**Explicación:**
- `*/5 * * * *` = Cada 5 minutos
- `~/duckdns/duck.sh` = Script a ejecutar
- `>/dev/null 2>&1` = Suprimir salida (ya tenemos duck.log)

### 4.3. Verificar cron

```bash
# Ver tareas programadas
crontab -l

# Ver logs de ejecución
tail -f ~/duckdns/duck.log
```

Deberías ver actualizaciones cada 5 minutos. ✅

---

## 🌐 Paso 5: Configurar Nginx con DuckDNS

### 5.1. Editar configuración de Nginx

```bash
sudo nano /etc/nginx/sites-available/logistica
```

### 5.2. Actualizar server_name

**ANTES:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com ec2-XX-XX-XX-XX.compute-1.amazonaws.com;
    ...
}
```

**DESPUÉS:**
```nginx
server {
    listen 80;
    server_name logistica-global.duckdns.org;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/html/logistica/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/html/logistica/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/html/logistica/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### 5.3. Probar configuración

```bash
sudo nginx -t
```

Deberías ver:
```
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 5.4. Reiniciar Nginx

```bash
sudo systemctl restart nginx
sudo systemctl status nginx
```

---

## 🔒 Paso 6: Configurar SSL con Let's Encrypt

### 6.1. Instalar Certbot

```bash
sudo apt update
sudo apt install -y certbot python3-certbot-nginx
```

### 6.2. Obtener certificado SSL

```bash
sudo certbot --nginx -d logistica-global.duckdns.org
```

Te preguntará:
- **Email:** Tu correo (para notificaciones de renovación)
- **Términos de servicio:** A (Agree)
- **Compartir email:** N (No)
- **Redirect HTTP to HTTPS:** 2 (Yes, redirect)

### 6.3. Verificar certificado

```bash
sudo certbot certificates
```

### 6.4. Probar renovación automática

```bash
sudo certbot renew --dry-run
```

Si no hay errores, ¡el certificado se renovará automáticamente! ✅

---

## 🔧 Paso 7: Actualizar Django Settings

### 7.1. Editar .env

```bash
nano /var/www/html/logistica/.env
```

Actualizar:

```env
DEBUG=False
ALLOWED_HOSTS=logistica-global.duckdns.org,localhost,127.0.0.1

# Configuración de seguridad para HTTPS
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 7.2. Editar settings.py

```python
# logistica/settings.py
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Configuración de seguridad (solo si DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

### 7.3. Reiniciar Gunicorn

```bash
sudo systemctl restart gunicorn
sudo systemctl status gunicorn
```

---

## ✅ Paso 8: Verificar Funcionamiento

### 8.1. Probar desde navegador

Abre tu navegador y visita:

```
https://logistica-global.duckdns.org
```

Deberías ver tu aplicación Django funcionando con HTTPS. 🎉

### 8.2. Probar endpoints de API

```bash
# Obtener token JWT
curl -X POST https://logistica-global.duckdns.org/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Listar vehículos
curl https://logistica-global.duckdns.org/api/vehiculos/

# Ver documentación Swagger
# https://logistica-global.duckdns.org/swagger/
```

### 8.3. Verificar actualización de IP

```bash
# Ver logs de DuckDNS
cat ~/duckdns/duck.log

# Deberías ver algo como:
# OK
# Sun Nov 17 10:00:01 UTC 2025: IP actualizada
# OK
# Sun Nov 17 10:05:01 UTC 2025: IP actualizada
```

---

## 🔄 Paso 9: Configuración Nginx Completa (Actualizada)

Después de configurar SSL, tu archivo de Nginx se verá así:

```bash
sudo cat /etc/nginx/sites-available/logistica
```

```nginx
server {
    server_name logistica-global.duckdns.org;
    
    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/html/logistica/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/html/logistica/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/html/logistica/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/logistica-global.duckdns.org/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/logistica-global.duckdns.org/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = logistica-global.duckdns.org) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name logistica-global.duckdns.org;
    return 404; # managed by Certbot
}
```

---

## 📊 Monitoreo y Mantenimiento

### Ver estado de DuckDNS

```bash
# Ver IP actual registrada
curl "https://www.duckdns.org/update?domains=logistica-global&token=TU_TOKEN&ip="

# Ver historial de actualizaciones
tail -20 ~/duckdns/duck.log
```

### Ver certificados SSL

```bash
sudo certbot certificates
```

### Renovar certificado manualmente

```bash
sudo certbot renew
sudo systemctl restart nginx
```

---

## 🆘 Troubleshooting

### Problema: DuckDNS devuelve "KO" en lugar de "OK"

**Solución:**
1. Verificar que el token es correcto
2. Verificar que el dominio está escrito correctamente
3. Revisar el script `duck.sh`

```bash
# Probar manualmente
curl "https://www.duckdns.org/update?domains=logistica-global&token=TU_TOKEN&ip="
```

### Problema: Nginx no acepta conexiones con DuckDNS

**Solución:**
1. Verificar que `server_name` en Nginx coincide con tu dominio
2. Reiniciar Nginx: `sudo systemctl restart nginx`
3. Verificar logs: `sudo tail -f /var/log/nginx/error.log`

### Problema: SSL no funciona

**Solución:**
1. Verificar que el dominio está accesible: `ping logistica-global.duckdns.org`
2. Ejecutar Certbot nuevamente: `sudo certbot --nginx -d logistica-global.duckdns.org`
3. Verificar firewall: `sudo ufw status` (debe permitir 80 y 443)

### Problema: IP no se actualiza automáticamente

**Solución:**
1. Verificar cron: `crontab -l`
2. Verificar permisos del script: `ls -la ~/duckdns/duck.sh` (debe ser ejecutable)
3. Probar script manualmente: `~/duckdns/duck.sh`
4. Ver logs de cron: `grep CRON /var/log/syslog`

---

## 📋 Checklist de Configuración

- [ ] Cuenta creada en DuckDNS.org
- [ ] Dominio registrado (ej: logistica-global.duckdns.org)
- [ ] Token obtenido y guardado
- [ ] Script duck.sh creado con token correcto
- [ ] Script tiene permisos de ejecución (chmod 700)
- [ ] Script probado manualmente (muestra "OK")
- [ ] Crontab configurado (*/5 * * * *)
- [ ] Nginx actualizado con server_name correcto
- [ ] Nginx testeado (nginx -t)
- [ ] Nginx reiniciado
- [ ] Certbot instalado
- [ ] Certificado SSL obtenido
- [ ] HTTPS funcionando
- [ ] ALLOWED_HOSTS actualizado en Django
- [ ] Gunicorn reiniciado
- [ ] Aplicación accesible desde https://TU-DOMINIO.duckdns.org

---

## 🎯 Resultado Final

Ahora tienes:

✅ **Dominio personalizado:**
```
https://logistica-global.duckdns.org
```

✅ **Actualización automática de IP:**
- Cada 5 minutos el script verifica la IP
- Si cambia, actualiza DuckDNS automáticamente

✅ **HTTPS con certificado válido:**
- Certificado Let's Encrypt gratuito
- Renovación automática cada 90 días

✅ **URLs accesibles:**
- `https://logistica-global.duckdns.org/` → Página principal
- `https://logistica-global.duckdns.org/admin/` → Panel admin
- `https://logistica-global.duckdns.org/api/` → API REST
- `https://logistica-global.duckdns.org/swagger/` → Documentación

---

## 📞 URLs de Servicio

| Servicio | URL |
|----------|-----|
| **Sitio Web** | https://logistica-global.duckdns.org |
| **Admin Django** | https://logistica-global.duckdns.org/admin/ |
| **API REST** | https://logistica-global.duckdns.org/api/ |
| **Swagger UI** | https://logistica-global.duckdns.org/swagger/ |
| **ReDoc** | https://logistica-global.duckdns.org/redoc/ |
| **JWT Token** | https://logistica-global.duckdns.org/api/token/ |

---

## 🚀 Comandos Rápidos de Referencia

```bash
# Actualizar IP manualmente
~/duckdns/duck.sh

# Ver logs de actualización
cat ~/duckdns/duck.log

# Ver tareas cron
crontab -l

# Probar Nginx
sudo nginx -t

# Reiniciar servicios
sudo systemctl restart nginx
sudo systemctl restart gunicorn

# Renovar SSL
sudo certbot renew

# Ver certificados
sudo certbot certificates
```

¡Tu configuración de DuckDNS está completa! 🦆✨
