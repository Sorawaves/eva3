FROM python:3.10-slim

# Metadatos
LABEL maintainer="Logística Global Ltda."
LABEL description="Django REST API - Sistema de Gestión Logística"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    netcat-traditional \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero (mejor cache de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Crear directorios necesarios
RUN mkdir -p staticfiles media logs

# Dar permisos
RUN chmod +x scripts/*.sh || true

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/api/', timeout=5)" || exit 1

# Comando por defecto (puede ser sobreescrito por docker-compose)
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "logistica.wsgi:application"]
