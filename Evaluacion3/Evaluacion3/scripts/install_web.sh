#!/bin/bash
#=============================================================================
# Script de Instalación Automática - INSTANCIA 1 (Web Server)
# Logística Global Ltda.
# 
# USO: Ejecutar con sudo después de conectar a la instancia EC2
#      curl -sL https://raw.githubusercontent.com/TU_USUARIO/logistica/main/scripts/install_web.sh | sudo bash
#      O subir el archivo y ejecutar: sudo bash install_web.sh
#=============================================================================

set -e  # Salir si hay algún error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  Instalación Automática - Instancia Web (Logística Global)    ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Detectar IP privada automáticamente
IP_PRIVADA=$(hostname -I | awk '{print $1}')
IP_PUBLICA=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo "NO_DETECTADA")

echo "📍 IPs detectadas:"
echo "   IP Privada: $IP_PRIVADA"
echo "   IP Pública: $IP_PUBLICA"
echo ""

# Solicitar datos al usuario
read -p "🔹 IP PRIVADA de la Instancia BD (ejemplo: 172.31.XX.XX): " DB_HOST
read -p "🔹 Dominio DuckDNS (sin .duckdns.org, ej: logistica-global): " DUCKDNS_DOMAIN
read -sp "🔹 Password para PostgreSQL: " DB_PASSWORD
echo ""
read -p "🔹 Token DuckDNS (opcional, Enter para omitir): " DUCKDNS_TOKEN
echo ""

# Variables fijas
PROJECT_DIR="/var/www/html/logistica"
GITHUB_REPO="https://github.com/TU_USUARIO/logistica.git"  # Opcional si copias manualmente

echo "📋 Configuración:"
echo "   - Proyecto: $PROJECT_DIR"
echo "   - Base de datos: $DB_HOST"
echo "   - Dominio DuckDNS: ${DUCKDNS_DOMAIN}.duckdns.org"
echo ""
read -p "¿Continuar? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Instalación cancelada"
    exit 1
fi

#=============================================================================
# DETECTAR SISTEMA OPERATIVO
#=============================================================================
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "❌ No se pudo detectar el sistema operativo"
    exit 1
fi

echo "🖥️  Sistema detectado: $OS"

#=============================================================================
# PASO 1: Actualizar sistema
#=============================================================================
echo ""
echo "📦 [1/10] Actualizando sistema..."
if [ "$OS" = "amzn" ] || [ "$OS" = "rhel" ] || [ "$OS" = "centos" ]; then
    # Amazon Linux / RHEL / CentOS
    yum update -y
elif [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    # Ubuntu / Debian
    apt update -qq
    apt upgrade -y -qq
else
    echo "⚠️  Sistema no reconocido, continuando..."
fi

#=============================================================================
# PASO 2: Instalar dependencias
#=============================================================================
echo "📦 [2/10] Instalando dependencias..."
if [ "$OS" = "amzn" ] || [ "$OS" = "rhel" ] || [ "$OS" = "centos" ]; then
    # Amazon Linux 2023 / RHEL
    # Detectar gestor de paquetes
    if command -v dnf &> /dev/null; then
        PKG_MGR="dnf"
    else
        PKG_MGR="yum"
    fi
    
    $PKG_MGR install -y \
        python3 \
        python3-pip \
        python3-devel \
        nginx \
        git \
        postgresql15 \
        gcc \
        gcc-c++ \
        make \
        libpq-devel
    
elif [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    # Ubuntu / Debian
    apt install -y -qq \
        python3-pip \
        python3-venv \
        python3-dev \
        nginx \
        git \
        postgresql-client \
        build-essential \
        libpq-dev \
        curl
fi

#=============================================================================
# PASO 3: Configurar firewall
#=============================================================================
echo "🔒 [3/10] Configurando firewall..."
if [ "$OS" = "amzn" ] || [ "$OS" = "rhel" ] || [ "$OS" = "centos" ]; then
    # Amazon Linux usa firewalld o iptables (generalmente configurado por Security Groups)
    echo "   ⚠️  En Amazon Linux, usa Security Groups de AWS para el firewall"
    echo "   Asegúrate de tener abiertos los puertos: 22, 80, 443"
elif [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
    # Ubuntu / Debian usa UFW
    ufw --force enable
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw reload
fi

#=============================================================================
# PASO 4: Clonar o actualizar proyecto
#=============================================================================
echo "📥 [4/10] Obteniendo código del proyecto..."

# Si existe, hacer backup y actualizar
if [ -d "$PROJECT_DIR" ]; then
    echo "   ⚠️  Proyecto existe, creando backup..."
    mv "$PROJECT_DIR" "${PROJECT_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Clonar repositorio
mkdir -p /var/www/html
cd /var/www/html

# Si no tienes GitHub, copiar archivos manualmente
if [[ $GITHUB_REPO == *"TU_USUARIO"* ]]; then
    echo "   ⚠️  El proyecto debe estar en /home/$WEB_USER/logistica o /tmp/logistica"
    
    if [ -d "/home/$WEB_USER/logistica" ]; then
        echo "   ✅ Copiando desde /home/$WEB_USER/logistica..."
        cp -r "/home/$WEB_USER/logistica" "$PROJECT_DIR"
    elif [ -d "/tmp/logistica" ]; then
        echo "   ✅ Copiando desde /tmp/logistica..."
        cp -r "/tmp/logistica" "$PROJECT_DIR"
    else
        echo "   ❌ No se encontró el proyecto"
        echo "   Ejecuta desde tu máquina local:"
        echo "   scp -i keypair.pem -r C:\\Users\\matia\\OneDrive\\Escritorio\\Evaluacion3\\Evaluacion3 $WEB_USER@${IP_PUBLICA}:/tmp/logistica"
        exit 1
    fi
else
    git clone "$GITHUB_REPO" logistica
fi

# Detectar usuario correcto
if [ "$OS" = "amzn" ]; then
    WEB_USER="ec2-user"
    WEB_GROUP="nginx"
else
    WEB_USER="ubuntu"
    WEB_GROUP="www-data"
fi

chown -R $WEB_USER:$WEB_GROUP "$PROJECT_DIR"

#=============================================================================
# PASO 5: Crear entorno virtual e instalar dependencias
#=============================================================================
echo "🐍 [5/10] Configurando entorno Python..."
cd "$PROJECT_DIR"

# Detectar usuario correcto (ec2-user en Amazon Linux, ubuntu en Ubuntu)
if [ "$OS" = "amzn" ]; then
    WEB_USER="ec2-user"
    WEB_GROUP="nginx"
else
    WEB_USER="ubuntu"
    WEB_GROUP="www-data"
fi

chown -R $WEB_USER:$WEB_GROUP "$PROJECT_DIR"

# Crear venv como usuario correcto
su - $WEB_USER -c "cd $PROJECT_DIR && python3 -m venv venv"
su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && pip install --upgrade pip -q"
su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && pip install -r requirements.txt -q"

#=============================================================================
# PASO 6: Configurar variables de entorno
#=============================================================================
echo "⚙️  [6/10] Configurando variables de entorno..."

# Generar SECRET_KEY segura
cd "$PROJECT_DIR"
SECRET_KEY=$(su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'")

cat > "$PROJECT_DIR/.env" << EOF
# Django Settings
SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=${DUCKDNS_DOMAIN}.duckdns.org,localhost,127.0.0.1,${IP_PUBLICA},${IP_PRIVADA}

# Base de datos en INSTANCIA 2
DB_ENGINE=django.db.backends.postgresql
DB_NAME=logistica_db
DB_USER=logistica_user
DB_PASSWORD=${DB_PASSWORD}
DB_HOST=${DB_HOST}
DB_PORT=5432

# Seguridad HTTPS (cambiar a True si usas SSL)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
EOF

chown $WEB_USER:$WEB_GROUP "$PROJECT_DIR/.env"
echo "   ✅ Variables de entorno configuradas"

#=============================================================================
# PASO 7: Probar conexión a base de datos
#=============================================================================
echo "🗄️  [7/10] Probando conexión a base de datos..."
if PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U logistica_user -d logistica_db -c "SELECT 1" &> /dev/null; then
    echo "   ✅ Conexión exitosa a la base de datos"
else
    echo "   ⚠️  No se pudo conectar a la base de datos"
    echo "   Asegúrate de que la Instancia 2 (BD) esté corriendo"
    echo "   Continuando de todas formas..."
fi

#=============================================================================
# PASO 8: Ejecutar migraciones y cargar datos
#=============================================================================
echo "🔄 [8/10] Ejecutando migraciones..."
cd "$PROJECT_DIR"

# Crear migraciones para la app transporte
echo "   📝 Creando migraciones..."
su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && python manage.py makemigrations transporte --noinput" || true
su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && python manage.py makemigrations --noinput" || true

# Aplicar migraciones
echo "   ⬆️  Aplicando migraciones..."
su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && python manage.py migrate --noinput"

# Recolectar archivos estáticos
echo "   📦 Recolectando archivos estáticos..."
su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && python manage.py collectstatic --noinput"

# Cargar datos iniciales
echo "   📊 Cargando datos iniciales..."
su - $WEB_USER -c "cd $PROJECT_DIR && source venv/bin/activate && python load_data.py" || echo "   ℹ️  Datos ya cargados o error menor (continuando...)"

#=============================================================================
# PASO 9: Configurar Gunicorn
#=============================================================================
echo "🦄 [9/10] Configurando Gunicorn..."
cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=Gunicorn daemon for Logistica Django app
After=network.target

[Service]
User=$WEB_USER
Group=$WEB_GROUP
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
          --workers 3 \\
          --bind unix:$PROJECT_DIR/gunicorn.sock \\
          logistica.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl start gunicorn
systemctl enable gunicorn
echo "   ✅ Gunicorn configurado y corriendo"

#=============================================================================
# PASO 10: Configurar Nginx
#=============================================================================
echo "🌐 [10/10] Configurando Nginx..."

if [ "$OS" = "amzn" ]; then
    # Amazon Linux usa /etc/nginx/conf.d/
    cat > /etc/nginx/conf.d/logistica.conf << EOF
server {
    listen 80 default_server;
    server_name ${DUCKDNS_DOMAIN}.duckdns.org ${IP_PUBLICA} ${IP_PRIVADA};

    client_max_body_size 10M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 30d;
    }

    location / {
        proxy_pass http://unix:$PROJECT_DIR/gunicorn.sock;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
}
EOF
    
    # Limpiar configuración por defecto si existe
    if [ -f /etc/nginx/nginx.conf.default ]; then
        mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak 2>/dev/null || true
        cat > /etc/nginx/nginx.conf << 'EOFNGINX'
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                      '\$status \$body_bytes_sent "\$http_referer" '
                      '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    include /etc/nginx/conf.d/*.conf;
}
EOFNGINX
    fi
    
else
    # Ubuntu / Debian usa sites-available/enabled
    cat > /etc/nginx/sites-available/logistica << EOF
server {
    listen 80 default_server;
    server_name ${DUCKDNS_DOMAIN}.duckdns.org ${IP_PUBLICA} ${IP_PRIVADA};

    client_max_body_size 10M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 30d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/gunicorn.sock;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_redirect off;
    }
}
EOF
    
    # Habilitar sitio
    rm -f /etc/nginx/sites-enabled/default
    ln -sf /etc/nginx/sites-available/logistica /etc/nginx/sites-enabled/
fi

# Probar configuración
if nginx -t; then
    echo "   ✅ Configuración de Nginx correcta"
else
    echo "   ❌ Error en configuración de Nginx"
    exit 1
fi

# Reiniciar Nginx
systemctl restart nginx
systemctl enable nginx
echo "   ✅ Nginx configurado y corriendo"

#=============================================================================
# CONFIGURAR DUCKDNS (Opcional)
#=============================================================================
if [[ ! $DUCKDNS_TOKEN == *"a7c4d0ad"* ]]; then
    echo ""
    echo "🦆 Configurando DuckDNS..."
    mkdir -p /home/ubuntu/duckdns
    cat > /home/ubuntu/duckdns/duck.sh << EOF
#!/bin/bash
echo url="https://www.duckdns.org/update?domains=${DUCKDNS_DOMAIN}&token=${DUCKDNS_TOKEN}&ip=" | curl -k -o /home/ubuntu/duckdns/duck.log -K -
EOF
    
    chmod 700 /home/ubuntu/duckdns/duck.sh
    chown -R ubuntu:ubuntu /home/ubuntu/duckdns
    
    # Ejecutar una vez
    su - ubuntu -c "/home/ubuntu/duckdns/duck.sh"
    
    # Agregar a crontab
    (crontab -u ubuntu -l 2>/dev/null; echo "*/5 * * * * /home/ubuntu/duckdns/duck.sh >/dev/null 2>&1") | crontab -u ubuntu -
    
    echo "   ✅ DuckDNS configurado (actualización cada 5 min)"
fi

#=============================================================================
# FINALIZACIÓN
#=============================================================================
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ✅ INSTALACIÓN COMPLETADA                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 URLs disponibles:"
echo "   - HTTP:    http://$(curl -s http://checkip.amazonaws.com)"
if [[ ! $DUCKDNS_TOKEN == *"a7c4d0ad"* ]]; then
    echo "   - DuckDNS: http://${DUCKDNS_DOMAIN}.duckdns.org"
fi
echo ""
echo "🔐 Credenciales por defecto:"
echo "   Usuario:   admin"
echo "   Password:  admin123"
echo ""
echo "📊 Verificar estado:"
echo "   sudo systemctl status gunicorn"
echo "   sudo systemctl status nginx"
echo ""
echo "📝 Ver logs:"
echo "   sudo journalctl -u gunicorn -f"
echo "   sudo tail -f /var/log/nginx/error.log"
echo ""
echo "🔄 Reiniciar servicios:"
echo "   sudo systemctl restart gunicorn nginx"
echo ""
echo "⏱️  Tiempo de instalación: $SECONDS segundos"
echo ""
