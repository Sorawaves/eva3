#!/bin/bash
#=============================================================================
# Script de Instalación Automática - INSTANCIA 2 (Database Server)
# Logística Global Ltda.
# 
# USO: Ejecutar con sudo después de conectar a la instancia EC2
#      curl -sL https://raw.githubusercontent.com/TU_USUARIO/logistica/main/scripts/install_db.sh | sudo bash
#      O subir el archivo y ejecutar: sudo bash install_db.sh
#=============================================================================

set -e  # Salir si hay algún error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Instalación Automática - Instancia BD (Logística Global)     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Detectar IP privada automáticamente
IP_PRIVADA=$(hostname -I | awk '{print $1}')

echo "📍 IP Privada de esta instancia BD: $IP_PRIVADA"
echo ""

# Solicitar datos al usuario
read -p "🔹 IP PRIVADA de la Instancia WEB (ejemplo: 172.31.13.25): " WEB_SERVER_IP
read -p "🔹 Usuario PostgreSQL a crear (default: logistica_user): " DB_USER
DB_USER=${DB_USER:-logistica_user}
read -sp "🔹 Password para el usuario: " DB_PASSWORD
echo ""
read -p "🔹 Nombre de la base de datos (default: logistica_db): " DB_NAME
DB_NAME=${DB_NAME:-logistica_db}
echo ""

# Variables fijas
POSTGRES_VERSION="14"

echo "📋 Configuración:"
echo "   - Base de datos: $DB_NAME"
echo "   - Usuario: $DB_USER"
echo "   - IP Instancia Web: $WEB_SERVER_IP"
echo "   - PostgreSQL: $POSTGRES_VERSION"
echo ""
read -p "¿Continuar? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Instalación cancelada"
    exit 1
fi

#=============================================================================
# PASO 1: Actualizar sistema
#=============================================================================
echo ""
echo "📦 [1/7] Actualizando sistema..."
apt update -qq
apt upgrade -y -qq

#=============================================================================
# PASO 2: Instalar PostgreSQL
#=============================================================================
echo "🗄️  [2/7] Instalando PostgreSQL ${POSTGRES_VERSION}..."
apt install -y -qq postgresql-${POSTGRES_VERSION} postgresql-contrib-${POSTGRES_VERSION}

# Verificar instalación
systemctl start postgresql
systemctl enable postgresql

#=============================================================================
# PASO 3: Configurar postgresql.conf
#=============================================================================
echo "⚙️  [3/7] Configurando PostgreSQL..."
PG_CONF="/etc/postgresql/${POSTGRES_VERSION}/main/postgresql.conf"

# Backup original
cp "$PG_CONF" "${PG_CONF}.backup"

# Configurar para escuchar en todas las interfaces
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Optimizaciones para t2.micro (1GB RAM)
cat >> "$PG_CONF" << EOF

# Optimizaciones para producción (t2.micro)
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

# Logging
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_statement = 'mod'
log_duration = on
log_line_prefix = '%m [%p] %u@%d '
EOF

#=============================================================================
# PASO 4: Configurar pg_hba.conf
#=============================================================================
echo "🔐 [4/7] Configurando acceso..."
PG_HBA="/etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf"

# Backup original
cp "$PG_HBA" "${PG_HBA}.backup"

# Agregar regla para instancia web
cat >> "$PG_HBA" << EOF

# Acceso desde Instancia Web (Logística Global)
host    $DB_NAME    $DB_USER    ${WEB_SERVER_IP}/32    md5
host    $DB_NAME    $DB_USER    10.0.1.0/24            md5
EOF

#=============================================================================
# PASO 5: Crear usuario y base de datos
#=============================================================================
echo "👤 [5/7] Creando usuario y base de datos..."

# Crear usuario
sudo -u postgres psql << EOF
-- Crear usuario
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER USER $DB_USER CREATEDB;

-- Crear base de datos
CREATE DATABASE $DB_NAME OWNER $DB_USER;

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;

-- Mostrar información
\l $DB_NAME
\du $DB_USER
EOF

#=============================================================================
# PASO 6: Configurar firewall
#=============================================================================
echo "🔒 [6/7] Configurando firewall..."
ufw --force enable
ufw allow 22/tcp
ufw allow from $WEB_SERVER_IP to any port 5432
ufw allow from 10.0.1.0/24 to any port 5432
ufw reload

#=============================================================================
# PASO 7: Reiniciar PostgreSQL y verificar
#=============================================================================
echo "🔄 [7/7] Reiniciando PostgreSQL..."
systemctl restart postgresql

# Verificar que está corriendo
if systemctl is-active --quiet postgresql; then
    echo "   ✅ PostgreSQL está corriendo"
else
    echo "   ❌ Error: PostgreSQL no está corriendo"
    systemctl status postgresql
    exit 1
fi

#=============================================================================
# CONFIGURAR BACKUP AUTOMÁTICO
#=============================================================================
echo ""
echo "💾 Configurando backup automático..."
mkdir -p /home/ubuntu/backups

cat > /usr/local/bin/backup-logistica.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/logistica_backup_$DATE.sql"

mkdir -p $BACKUP_DIR
pg_dump -U logistica_user -h localhost logistica_db > $BACKUP_FILE
gzip $BACKUP_FILE
find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
echo "$(date): Backup completado - ${BACKUP_FILE}.gz" >> $BACKUP_DIR/backup.log
EOF

chmod +x /usr/local/bin/backup-logistica.sh
chown ubuntu:ubuntu /usr/local/bin/backup-logistica.sh

# Agregar a crontab (backup diario a las 3 AM)
(crontab -u ubuntu -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/backup-logistica.sh >> /home/ubuntu/backups/backup.log 2>&1") | crontab -u ubuntu -

#=============================================================================
# OBTENER IP PRIVADA (ya la tenemos de antes)
#=============================================================================
PRIVATE_IP=$IP_PRIVADA

#=============================================================================
# FINALIZACIÓN
#=============================================================================
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ INSTALACIÓN COMPLETADA                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🗄️  Información de conexión:"
echo "   Host:     $PRIVATE_IP"
echo "   Port:     5432"
echo "   Database: $DB_NAME"
echo "   User:     $DB_USER"
echo "   Password: $DB_PASSWORD"
echo ""
echo "🔗 Connection String para Instancia Web (.env):"
echo "   DB_HOST=$PRIVATE_IP"
echo "   DB_NAME=$DB_NAME"
echo "   DB_USER=$DB_USER"
echo "   DB_PASSWORD=$DB_PASSWORD"
echo "   DB_PORT=5432"
echo ""
echo "✅ Probar conexión desde Instancia Web:"
echo "   psql -h $PRIVATE_IP -U $DB_USER -d $DB_NAME"
echo ""
echo "📊 Verificar estado:"
echo "   sudo systemctl status postgresql"
echo ""
echo "📝 Ver logs:"
echo "   sudo tail -f /var/log/postgresql/postgresql-${POSTGRES_VERSION}-main.log"
echo ""
echo "💾 Backups:"
echo "   Automático: Diario a las 3 AM"
echo "   Ubicación: /home/ubuntu/backups/"
echo "   Manual: /usr/local/bin/backup-logistica.sh"
echo ""
echo "⏱️  Tiempo de instalación: $SECONDS segundos"
echo ""
echo "⚠️  IMPORTANTE: Actualiza el archivo .env en la Instancia Web con:"
echo "   DB_HOST=$PRIVATE_IP"
echo ""
