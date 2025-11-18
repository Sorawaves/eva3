#!/usr/bin/env pwsh
# Script de inicio rápido para Windows PowerShell
# Ejecutar: .\start.ps1

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Sistema de Gestión Logística - Inicio Rápido  " -ForegroundColor Cyan
Write-Host "  Logística Global Ltda.                         " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si existe el entorno virtual
if (-Not (Test-Path "venv")) {
    Write-Host "⚠️  No se encontró entorno virtual." -ForegroundColor Yellow
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Green
    python -m venv venv
    
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
    Write-Host ""
}

# Activar entorno virtual
Write-Host "🔄 Activando entorno virtual..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

# Verificar si hay dependencias instaladas
Write-Host "📦 Verificando dependencias..." -ForegroundColor Green
$pipList = pip list
if (-Not ($pipList -match "Django")) {
    Write-Host "📥 Instalando dependencias..." -ForegroundColor Green
    pip install -r requirements.txt
    Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
} else {
    Write-Host "✅ Dependencias ya instaladas" -ForegroundColor Green
}
Write-Host ""

# Verificar si existe la base de datos
if (-Not (Test-Path "db.sqlite3")) {
    Write-Host "⚠️  No se encontró base de datos." -ForegroundColor Yellow
    Write-Host "🔄 Ejecutando migraciones..." -ForegroundColor Green
    python manage.py makemigrations
    python manage.py migrate
    
    Write-Host ""
    Write-Host "📊 ¿Deseas cargar datos de ejemplo? (S/N)" -ForegroundColor Cyan
    $respuesta = Read-Host
    
    if ($respuesta -eq "S" -or $respuesta -eq "s") {
        Write-Host "📥 Cargando datos de ejemplo..." -ForegroundColor Green
        Get-Content load_data.py | python manage.py shell
        Write-Host "✅ Datos cargados correctamente" -ForegroundColor Green
    }
} else {
    Write-Host "✅ Base de datos encontrada" -ForegroundColor Green
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  🚀 INICIANDO SERVIDOR DE DESARROLLO            " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 URLs disponibles:" -ForegroundColor Green
Write-Host "  - Inicio:        http://localhost:8000/" -ForegroundColor White
Write-Host "  - Admin:         http://localhost:8000/admin/" -ForegroundColor White
Write-Host "  - API:           http://localhost:8000/api/" -ForegroundColor White
Write-Host "  - Swagger:       http://localhost:8000/swagger/" -ForegroundColor White
Write-Host ""
Write-Host "🔑 Credenciales:" -ForegroundColor Green
Write-Host "  Usuario:  admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
python manage.py runserver
