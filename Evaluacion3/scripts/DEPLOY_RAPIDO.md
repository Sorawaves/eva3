# 🚀 Despliegue Rápido en AWS Academy (No Persistente)

## 📋 Guía de Uso para Evaluación

Esta guía te permite **levantar todo el sistema en 5-10 minutos** cada vez que inicies una sesión de AWS Academy, perfecto para demostraciones y evaluaciones.

---

## ⚡ Resumen Rápido (TL;DR)

```bash
# INSTANCIA 1 (Base de Datos) - EJECUTAR PRIMERO
sudo bash scripts/install_db.sh

# INSTANCIA 2 (Web Server) - EJECUTAR DESPUÉS
# Actualizar IP de BD en el script
sudo bash scripts/install_web.sh
```

---

## 🎯 Flujo de Trabajo para AWS Academy

### Preparación (Una sola vez)

1. **Comprimir el proyecto**
   ```bash
   cd /home/fari
   tar -czf logistica.tar.gz Evaluacion3/
   ```

2. **Tener listos:**
   - ✅ Archivo `logistica.tar.gz`
   - ✅ Llave `.pem` de AWS Academy
   - ✅ Scripts `install_db.sh` y `install_web.sh`

---

## 🚀 Cada Vez que Inicies AWS Academy (10 minutos)

### PASO 1: Lanzar Instancias EC2 (2 minutos)

#### Instancia 1: Base de Datos

```
Nombre:          logistica-db-server
AMI:             Ubuntu Server 20.04 LTS
Tipo:            t2.micro
VPC:             Default VPC
Subnet:          Privada (o pública temporal)
IP Pública:      Deshabilitada (o habilitada solo para instalación)
Security Group:  logistica-db-sg
  - Puerto 5432 desde Instancia Web
  - Puerto 22 desde Mi IP (temporal)
Key Pair:        Seleccionar tu keypair
```

#### Instancia 2: Web Server

```
Nombre:          logistica-web-server
AMI:             Ubuntu Server 20.04 LTS
Tipo:            t2.micro
VPC:             Default VPC
Subnet:          Pública
IP Pública:      Habilitada
Security Group:  logistica-web-sg
  - Puerto 22 desde Mi IP
  - Puerto 80 desde 0.0.0.0/0
  - Puerto 443 desde 0.0.0.0/0
Key Pair:        Seleccionar tu keypair
```

### PASO 2: Subir Archivos Necesarios (1 minuto)

```bash
# Obtener IPs
IP_DB="XX.XX.XX.XX"      # IP pública temporal de instancia BD
IP_WEB="YY.YY.YY.YY"     # IP pública de instancia Web

# IMPORTANTE: Cada instancia solo necesita ciertos archivos:

# OPCIÓN 1 - Subir todo a ambas (más simple, recomendado para principiantes)
scp -i keypair.pem logistica.tar.gz ubuntu@$IP_DB:/tmp/
scp -i keypair.pem logistica.tar.gz ubuntu@$IP_WEB:/tmp/

# OPCIÓN 2 - Optimizado (solo lo necesario, avanzado)
# BD solo necesita el script:
scp -i keypair.pem scripts/install_db.sh ubuntu@$IP_DB:/tmp/
# Web necesita el proyecto completo:
scp -i keypair.pem logistica.tar.gz ubuntu@$IP_WEB:/tmp/
```

**💡 Explicación:** La instancia de BD solo ejecuta PostgreSQL (no necesita tu código Django), pero subir todo es más simple y el archivo pesa poco.
```

### PASO 3: Instalar Base de Datos PRIMERO (3 minutos)

```bash
# Conectar a instancia BD
ssh -i keypair.pem ubuntu@$IP_DB

# Si usaste OPCIÓN 1 (subir todo):
cd /tmp && tar -xzf logistica.tar.gz && cd Evaluacion3
sudo bash scripts/install_db.sh

# Si usaste OPCIÓN 2 (solo script):
cd /tmp
sudo bash install_db.sh

# ⚠️ IMPORTANTE: Anotar la IP PRIVADA que muestra al final
# Ejemplo: DB_HOST=10.0.1.234
```

Al terminar verás algo como:

```
╔════════════════════════════════════════════════════════════════╗
║                  ✅ INSTALACIÓN COMPLETADA                      ║
╚════════════════════════════════════════════════════════════════╝

🗄️  Información de conexión:
   Host:     10.0.1.234    <-- ⚠️ COPIAR ESTA IP
   Port:     5432
   Database: logistica_db
   User:     logistica_user
   Password: LogisticaSecure2025!
```

### PASO 4: Instalar Web Server (3 minutos)

```bash
# Conectar a instancia Web (en OTRA terminal)
ssh -i keypair.pem ubuntu@$IP_WEB

# Descomprimir proyecto
cd /tmp
tar -xzf logistica.tar.gz
cd Evaluacion3

# ⚠️ EDITAR el script con la IP PRIVADA de la BD
nano scripts/install_web.sh

# Buscar y cambiar:
DB_HOST="10.0.2.50"    # Cambiar por la IP privada real
                        # Ejemplo: DB_HOST="10.0.1.234"

# Guardar (Ctrl+O, Enter, Ctrl+X)

# Ejecutar instalación
sudo bash scripts/install_web.sh
```

### PASO 5: Verificar (1 minuto)

```bash
# Ver si todo está corriendo
sudo systemctl status gunicorn
sudo systemctl status nginx

# Obtener IP pública
curl http://checkip.amazonaws.com
```

Abre en tu navegador:
```
http://IP_PUBLICA_WEB
```

---

## 📝 Versión Simplificada (Sin Scripts - Manual)

Si prefieres hacerlo paso a paso manualmente, usa las guías originales:
- [INSTANCIA_BD_EC2.md](../INSTANCIA_BD_EC2.md)
- [AWS_DEPLOYMENT.md](../AWS_DEPLOYMENT.md)

---

## 🎬 Para la Evaluación en Vivo

### Antes de la Evaluación:

1. **Practica el proceso** 2-3 veces para dominarlo
2. **Cronometra** - Debería tomar ~10 minutos
3. **Ten listos los archivos** en tu máquina local
4. **Anota las contraseñas** que usarás

### Durante la Evaluación:

1. **Iniciar sesión AWS Academy** (30 segundos)
2. **Lanzar 2 instancias EC2** (2 minutos)
3. **Subir proyecto** (1 minuto)
4. **Instalar BD** (3 minutos)
5. **Instalar Web** (3 minutos)
6. **Verificar funcionamiento** (1 minuto)

**Total: ~10 minutos** ⏱️

### Qué Mostrar:

```bash
# 1. Arquitectura
echo "Tengo 2 instancias EC2 separadas:"
echo "- Instancia BD: $IP_PRIVADA_BD (sin IP pública)"
echo "- Instancia Web: $IP_PUBLICA_WEB"

# 2. Servicios corriendo
sudo systemctl status postgresql   # En instancia BD
sudo systemctl status gunicorn     # En instancia Web
sudo systemctl status nginx        # En instancia Web

# 3. Aplicación funcionando
curl http://$IP_PUBLICA_WEB
curl http://$IP_PUBLICA_WEB/api/vehiculos/

# 4. Swagger
echo "Abrir: http://$IP_PUBLICA_WEB/swagger/"
```

---

## 🔧 Personalización de Scripts

### Variables a Cambiar en `install_web.sh`:

```bash
# Línea 15-20
DB_HOST="10.0.2.50"              # ⚠️ IP privada de instancia BD
DB_PASSWORD="TuPasswordSeguro!"   # ⚠️ Tu password
DUCKDNS_DOMAIN="tu-dominio"      # ⚠️ Tu dominio DuckDNS (opcional)
DUCKDNS_TOKEN="tu-token"         # ⚠️ Tu token DuckDNS (opcional)

# Si no usas GitHub
GITHUB_REPO="https://github.com/TU_USUARIO/logistica.git"
# Cambiar a: Manual (subir por SCP)
```

### Variables a Cambiar en `install_db.sh`:

```bash
# Línea 15-18
DB_PASSWORD="TuPasswordSeguro!"   # ⚠️ Debe coincidir con install_web.sh
WEB_SERVER_IP="10.0.1.10"        # ⚠️ IP privada de instancia web
```

---

## 🐛 Troubleshooting Rápido

### Script falla en install_web.sh

```bash
# Ver logs
sudo journalctl -u gunicorn -n 50
sudo tail -f /var/log/nginx/error.log

# Reiniciar servicios
sudo systemctl restart gunicorn nginx
```

### No conecta a la base de datos

```bash
# Desde instancia Web, probar conexión
psql -h IP_PRIVADA_BD -U logistica_user -d logistica_db

# Verificar Security Group de instancia BD
# Debe permitir puerto 5432 desde IP de instancia Web
```

### Gunicorn no inicia

```bash
# Ver error específico
sudo journalctl -u gunicorn -n 100 --no-pager

# Verificar permisos
sudo chown -R ubuntu:www-data /var/www/html/logistica
sudo systemctl restart gunicorn
```

---

## 📊 Tiempos Estimados

| Tarea | Tiempo |
|-------|--------|
| Lanzar instancias EC2 | 2 min |
| Subir proyecto (SCP) | 1 min |
| Instalar BD (script) | 3 min |
| Instalar Web (script) | 3 min |
| Verificar y probar | 1 min |
| **TOTAL** | **~10 min** |

---

## 🎯 Alternativa: Docker Compose (Local)

Si AWS Academy no funciona, puedes demostrar localmente con Docker:

```bash
# En tu máquina local
docker-compose up -d

# Listo en 30 segundos
# http://localhost:8000
```

Ver archivo: [docker-compose.yml](docker-compose.yml) (si lo creamos)

---

## ✅ Checklist Pre-Evaluación

- [ ] He practicado el despliegue 2-3 veces
- [ ] Los scripts funcionan correctamente
- [ ] He actualizado las IPs y passwords en los scripts
- [ ] Tengo el archivo `logistica.tar.gz` listo
- [ ] Tengo la llave `.pem` lista
- [ ] Conozco mis credenciales de AWS Academy
- [ ] He cronometrado el proceso (~10 minutos)
- [ ] Sé qué mostrar durante la evaluación
- [ ] Tengo backup: demostración local funciona

---

## 💡 Consejos para la Evaluación

1. **Practica antes** - Hazlo 2-3 veces para que te salga natural
2. **Ten un plan B** - Si AWS Academy falla, muestra localmente
3. **Explica mientras haces** - "Ahora estoy instalando PostgreSQL en la segunda instancia..."
4. **Muestra la arquitectura** - Explica por qué son 2 instancias separadas
5. **Destaca la seguridad** - "La base de datos no está expuesta a internet"

---

## 🎓 Script de Explicación para el Profesor

```
"Profesor, este proyecto está diseñado para AWS con 2 instancias EC2 separadas.

Debido a que AWS Academy no mantiene instancias persistentes, he creado 
scripts de instalación automática que levantan todo el sistema en ~10 minutos.

[Mostrar terminal]
- Instancia 1: Base de Datos PostgreSQL (sin IP pública)
- Instancia 2: Servidor Web Django + Nginx (con IP pública)

Los scripts instalan y configuran todo automáticamente. 
La base de datos NO está expuesta a internet, solo acepta conexiones 
desde la instancia web usando IP privada.

[Mostrar navegador]
Aquí está la aplicación funcionando con los 8 modelos, JWT, y Swagger.

Si desea, puedo ejecutar los scripts desde cero para mostrar el proceso 
completo, toma aproximadamente 10 minutos."
```

---

## 📞 ¿Necesitas Ayuda?

Si algo no funciona:

1. **Revisa los logs:**
   ```bash
   sudo journalctl -u gunicorn -f
   sudo tail -f /var/log/nginx/error.log
   ```

2. **Verifica conexiones:**
   ```bash
   # Desde instancia Web
   ping IP_PRIVADA_BD
   psql -h IP_PRIVADA_BD -U logistica_user -d logistica_db
   ```

3. **Reinicia servicios:**
   ```bash
   sudo systemctl restart gunicorn nginx postgresql
   ```

---

¡Listo! Con estos scripts puedes levantar todo el sistema en **~10 minutos** cada vez que inicies AWS Academy. Perfecto para tu evaluación. 🚀
