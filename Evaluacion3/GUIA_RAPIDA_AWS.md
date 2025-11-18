# 🚀 GUÍA RÁPIDA DE DEPLOYMENT EN AWS - DOS INSTANCIAS EC2

## ✅ **PROYECTO 100% LISTO PARA AWS**

Este proyecto ahora está **completamente preparado** para correr en dos instancias EC2 de AWS según los requerimientos.

---

## 📋 **ARCHIVOS CLAVE CREADOS:**

### 1. **`.env.aws`** - Template de variables de entorno
- Plantilla con placeholders para configuración
- Incluye todas las variables necesarias
- Instrucciones claras de qué reemplazar

### 2. **`nginx/nginx-ec2.conf`** - Configuración de Nginx para EC2
- Usa socket Unix de Gunicorn (más eficiente)
- Listo para producción
- Compatible con DuckDNS y SSL

### 3. **`scripts/install_web.sh`** - Script automático INSTANCIA WEB
- ✅ Detecta IPs automáticamente
- ✅ Solicita solo datos necesarios (IP BD, dominio, password)
- ✅ Configura todo: Python, Nginx, Gunicorn, Django
- ✅ Genera SECRET_KEY automáticamente
- ✅ Crea archivo .env con configuración real

### 4. **`scripts/install_db.sh`** - Script automático INSTANCIA BD
- ✅ Detecta IP privada automáticamente
- ✅ Solicita IP de instancia Web
- ✅ Instala y configura PostgreSQL 14
- ✅ Crea usuario y base de datos
- ✅ Configura firewall y acceso remoto
- ✅ Configura backups automáticos

### 5. **`settings.py`** - Actualizado para producción
- ✅ Seguridad HTTPS configurable desde .env
- ✅ CORS correcto para producción
- ✅ Sin configuraciones hardcodeadas

---

## 🎯 **CÓMO USAR (PASO A PASO):**

### **PASO 1: En tu máquina local**

```powershell
# 1. Subir proyecto a ambas instancias
scp -i tu-llave.pem -r c:\Users\matia\OneDrive\Escritorio\Evaluacion3\Evaluacion3 ubuntu@IP_INSTANCIA_WEB:/home/ubuntu/logistica
scp -i tu-llave.pem -r c:\Users\matia\OneDrive\Escritorio\Evaluacion3\Evaluacion3 ubuntu@IP_INSTANCIA_BD:/home/ubuntu/logistica
```

### **PASO 2: En la INSTANCIA BD (primero)**

```bash
# Conectar
ssh -i tu-llave.pem ubuntu@IP_INSTANCIA_BD

# Copiar proyecto y ejecutar script
sudo cp -r /home/ubuntu/logistica /var/www/html/
cd /var/www/html/logistica
sudo bash scripts/install_db.sh

# El script te preguntará:
# - IP de instancia Web: 172.31.13.25 (la que viste)
# - Usuario: logistica_user (default, presiona Enter)
# - Password: [el que quieras]
# - Base de datos: logistica_db (default, presiona Enter)

# ⚠️ IMPORTANTE: Anota la IP privada que muestra al final
```

### **PASO 3: En la INSTANCIA WEB (segundo)**

```bash
# Conectar
ssh -i tu-llave.pem ubuntu@IP_INSTANCIA_WEB

# Copiar proyecto y ejecutar script
sudo cp -r /home/ubuntu/logistica /var/www/html/
cd /var/www/html/logistica
sudo bash scripts/install_web.sh

# El script te preguntará:
# - IP de BD: [la que anotaste del paso anterior]
# - Dominio DuckDNS: logistica-global
# - Password PostgreSQL: [el mismo del paso anterior]
# - Token DuckDNS: [tu token de duckdns.org, o Enter para omitir]

# ✅ ¡LISTO! La aplicación estará corriendo
```

### **PASO 4: Acceder a tu aplicación**

```
http://IP_PUBLICA_WEB
http://tu-dominio.duckdns.org (si configuraste DuckDNS)
```

---

## 🔐 **CONFIGURAR SSL (OPCIONAL pero RECOMENDADO):**

```bash
# En la instancia WEB, después de configurar DuckDNS:
sudo certbot --nginx -d tu-dominio.duckdns.org

# Luego actualizar .env:
sudo nano /var/www/html/logistica/.env

# Cambiar:
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Reiniciar:
sudo systemctl restart gunicorn nginx
```

---

## 🗄️ **ARQUITECTURA FINAL:**

```
┌─────────────────────────────────────────────────────┐
│                    INTERNET                         │
│                        ↓                            │
│              [DuckDNS DNS Dinámico]                 │
│                        ↓                            │
└────────────────────────┼────────────────────────────┘
                         │
                    HTTPS (443)
                         │
┌────────────────────────▼────────────────────────────┐
│              INSTANCIA 1 (WEB)                      │
│              IP: 172.31.13.25 (privada)             │
│              IP: XX.XX.XX.XX (pública)              │
│                                                     │
│  ┌────────────┐   ┌─────────────┐                  │
│  │   Nginx    │──▶│  Gunicorn   │                  │
│  │  (80/443)  │   │   (socket)  │                  │
│  └────────────┘   └──────┬──────┘                  │
│                          │                          │
│                    ┌─────▼──────┐                   │
│                    │   Django   │                   │
│                    └────────────┘                   │
└─────────────────────────┼───────────────────────────┘
                          │
                    PostgreSQL
                    IP Privada
                          │
┌─────────────────────────▼───────────────────────────┐
│              INSTANCIA 2 (BD)                       │
│              IP: 172.31.XX.XX (privada)             │
│              SIN IP PÚBLICA                         │
│                                                     │
│            ┌──────────────────┐                     │
│            │  PostgreSQL 14   │                     │
│            │  logistica_db    │                     │
│            │   (puerto 5432)  │                     │
│            └──────────────────┘                     │
└─────────────────────────────────────────────────────┘
```

---

## 📝 **CHECKLIST DE VERIFICACIÓN:**

- [ ] Instancia 1 lanzada (t2.micro, subnet pública, Security Group: 22, 80, 443)
- [ ] Instancia 2 lanzada (t2.micro, subnet privada, Security Group: 5432 desde IP instancia 1)
- [ ] Proyecto copiado en ambas instancias
- [ ] Script `install_db.sh` ejecutado en Instancia 2
- [ ] IP privada de BD anotada
- [ ] Script `install_web.sh` ejecutado en Instancia 1
- [ ] Aplicación accesible desde navegador
- [ ] DuckDNS configurado (opcional)
- [ ] SSL instalado con Let's Encrypt (opcional)
- [ ] Superusuario creado: `sudo -u ubuntu venv/bin/python manage.py createsuperuser`

---

## 🆘 **COMANDOS ÚTILES:**

### En Instancia WEB:
```bash
# Ver logs
sudo journalctl -u gunicorn -f
sudo tail -f /var/log/nginx/error.log

# Reiniciar servicios
sudo systemctl restart gunicorn nginx

# Ver estado
sudo systemctl status gunicorn nginx
```

### En Instancia BD:
```bash
# Ver logs
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Conectar a PostgreSQL
sudo -u postgres psql

# Backup manual
/usr/local/bin/backup-logistica.sh
```

---

## 🎉 **¡TU PROYECTO ESTÁ LISTO!**

Todos los archivos necesarios están creados y configurados. Solo necesitas:
1. Lanzar las 2 instancias EC2
2. Ejecutar los scripts
3. ¡Disfrutar!

**Documentación adicional:**
- `AWS_DEPLOYMENT.md` - Guía detallada paso a paso
- `INSTANCIA_BD_EC2.md` - Detalles de configuración de PostgreSQL
- `DUCKDNS_SETUP.md` - Configuración de DNS dinámico
