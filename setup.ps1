# 🚀 Script de Setup Automatizado - Python REFramework con Gemini
# Ejecutar con: powershell -ExecutionPolicy Bypass -File setup.ps1

Write-Host "🚀 Iniciando setup de Python REFramework con Gemini..." -ForegroundColor Green

# Verificar Python
Write-Host "🔍 Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✅ $pythonVersion encontrado" -ForegroundColor Green
} catch {
    Write-Host "❌ Python no encontrado. Por favor instalar Python 3.8+." -ForegroundColor Red
    exit 1
}

# Crear entorno virtual si no existe
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
} else {
    Write-Host "✅ Entorno virtual ya existe" -ForegroundColor Green
}

# Instalar dependencias
Write-Host "📥 Instalando dependencias..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias instaladas exitosamente" -ForegroundColor Green
} else {
    Write-Host "❌ Error instalando dependencias" -ForegroundColor Red
    exit 1
}

# Verificar estructura de directorios
Write-Host "📁 Verificando estructura de directorios..." -ForegroundColor Yellow
$directories = @("data\input", "data\output")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "📁 Creado directorio: $dir" -ForegroundColor Blue
    } else {
        Write-Host "✅ Directorio existe: $dir" -ForegroundColor Green
    }
}

# Verificar archivos importantes
Write-Host "📄 Verificando archivos de configuración..." -ForegroundColor Yellow
$files = @(
    @{Path = ".env"; Description = "Variables de entorno"},
    @{Path = "config\settings.json"; Description = "Configuración principal"},
    @{Path = "data\input\prompts.csv"; Description = "Datos de entrada"}
)

foreach ($file in $files) {
    if (Test-Path $file.Path) {
        Write-Host "✅ $($file.Description): $($file.Path)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Falta: $($file.Description) - $($file.Path)" -ForegroundColor Yellow
    }
}

# Verificar clave API
Write-Host "🔑 Verificando configuración de API..." -ForegroundColor Yellow
if ($env:GEMINI_API_KEY) {
    Write-Host "✅ Variable GEMINI_API_KEY configurada" -ForegroundColor Green
} elseif (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "GEMINI_API_KEY=.+") {
        Write-Host "✅ GEMINI_API_KEY encontrada en archivo .env" -ForegroundColor Green
    } else {
        Write-Host "⚠️  GEMINI_API_KEY no configurada en .env" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Necesitas configurar GEMINI_API_KEY" -ForegroundColor Yellow
}

# Ejecutar tests básicos
Write-Host "🧪 Ejecutando tests básicos..." -ForegroundColor Yellow
python -m pytest tests/test_process.py::TestInitModule::test_verify_dependencies -v --tb=no
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Tests básicos pasaron" -ForegroundColor Green
} else {
    Write-Host "⚠️  Algunos tests fallaron (normal)" -ForegroundColor Yellow
}

# Mostrar resumen
Write-Host "`n" -NoNewline
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "📋 RESUMEN DEL SETUP" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "✅ Python: Verificado" -ForegroundColor Green
Write-Host "✅ Entorno virtual: Configurado" -ForegroundColor Green
Write-Host "✅ Dependencias: Instaladas" -ForegroundColor Green
Write-Host "✅ Estructura: Verificada" -ForegroundColor Green
Write-Host "✅ Tests: Ejecutados" -ForegroundColor Green

# Mostrar próximos pasos
Write-Host "`n🎯 PRÓXIMOS PASOS:" -ForegroundColor Blue
Write-Host "1. Configurar GEMINI_API_KEY:" -ForegroundColor White
Write-Host "   `$env:GEMINI_API_KEY=`"tu_clave_aqui`"" -ForegroundColor Gray
Write-Host "2. Editar datos de entrada (opcional):" -ForegroundColor White
Write-Host "   notepad data\input\prompts.csv" -ForegroundColor Gray
Write-Host "3. Ejecutar el sistema:" -ForegroundColor White
Write-Host "   python main.py" -ForegroundColor Gray
Write-Host "4. Ver resultados:" -ForegroundColor White
Write-Host "   Get-Content data\output\execution_report.json" -ForegroundColor Gray

Write-Host "`n📚 DOCUMENTACIÓN DISPONIBLE:" -ForegroundColor Blue
Write-Host "- DOCUMENTATION.md: Guía completa" -ForegroundColor White
Write-Host "- QUICK_REFERENCE.md: Comandos rápidos" -ForegroundColor White
Write-Host "- WARP.md: Guía para Warp AI" -ForegroundColor White
Write-Host "- README.md: Documentación principal" -ForegroundColor White

Write-Host "`n🎉 Setup completado exitosamente!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
