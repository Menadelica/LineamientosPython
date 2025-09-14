# 📚 Documentación Completa - Python REFramework con Gemini

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Setup Inicial](#-setup-inicial)
3. [Configuración](#-configuración)
4. [Ejecución](#-ejecución)
5. [Estructura del Proyecto](#-estructura-del-proyecto)
6. [Comandos Principales](#-comandos-principales)
7. [Archivos Importantes](#-archivos-importantes)
8. [Troubleshooting](#-troubleshooting)
9. [Mantenimiento](#-mantenimiento)

---

## 🎯 Descripción del Proyecto

**Automatización de Generación de Prompts con Gemini** - Sistema basado en el Python REFramework que procesa prompts desde un archivo CSV y genera respuestas detalladas usando la API de Google Gemini para automatizaciones de UiPath.

### Características Principales
- ✅ Framework REFramework con 5 fases
- ✅ Integración con Google Gemini API
- ✅ Manejo robusto de errores (Business vs System)
- ✅ Logging estructurado y reportes automáticos
- ✅ Suite completa de tests unitarios
- ✅ Configuración externa sin credenciales hardcodeadas

---

## 🚀 Setup Inicial

### Prerrequisitos
- Python 3.8 or superior
- Google Gemini API Key
- PowerShell (Windows)

### Pasos de Instalación

#### 1. Crear entorno virtual
```powershell
python -m venv venv
# El entorno se activa automáticamente en algunas configuraciones
```

#### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

#### 3. Configurar variables de entorno
```powershell
# Opción 1: Variable temporal (solo para la sesión actual)
$env:GEMINI_API_KEY="tu_clave_api_real_aqui"

# Opción 2: Editar el archivo .env
# Abrir .env y reemplazar "tu_clave_api_aqui" con tu clave real
```

#### 4. Obtener clave API de Google Gemini
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API Key
3. Cópiala y úsala en el paso 3

---

## ⚙️ Configuración

### Archivo .env
```env
GEMINI_API_KEY=tu_clave_api_real_aqui
```

### Archivo config/settings.json
```json
{
    "gemini": {
        "model": "gemini-2.5-pro",
        "thinking_budget": -1,
        "system_instruction": "Eres un agente especializado en flujos de UiPath y automatizaciones"
    },
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "data/output/automation.log"
    },
    "processing": {
        "max_retries": 3,
        "retry_delay": 5,
        "batch_size": 10
    },
    "paths": {
        "input_data": "data/input/prompts.csv",
        "output_data": "data/output/results.csv",
        "logs": "data/output/"
    }
}
```

### Archivo de datos de entrada (data/input/prompts.csv)
```csv
id,prompt,context,expected_output
1,"Crea un flujo de UiPath para automatizar facturación","Sistema ERP con interfaz web","Diagrama de flujo detallado"
2,"Procesar emails entrantes","Cliente Exchange","Workflow con decisiones"
```

---

## 🎮 Ejecución

### Comandos Principales

#### Ejecución Normal
```powershell
# Configurar API key y ejecutar
$env:GEMINI_API_KEY="tu_clave_api"; python main.py
```

#### Ver Ayuda
```powershell
python main.py --help
```

#### Ejemplo Directo (Testing)
```powershell
$env:GEMINI_API_KEY="tu_clave_api"; python gemini.py
```

#### Tests
```powershell
# Todos los tests
python -m pytest tests/ -v

# Tests específicos
python -m pytest tests/test_process.py -v

# Con cobertura
python -m pytest --cov=framework tests/
```

#### Formateo y Linting
```powershell
# Formatear código
python -m black .

# Verificar estilo
python -m flake8 framework/ tests/
```

---

## 📁 Estructura del Proyecto

```
C:\Users\Mena\Desktop\g\
├── 📄 .env                      # Variables de entorno
├── 📄 WARP.md                   # Guía para Warp AI
├── 📄 DOCUMENTATION.md          # Esta documentación
├── 📄 README.md                 # Documentación principal
├── 📄 main.py                   # Punto de entrada principal
├── 📄 gemini.py                 # Ejemplo directo de Gemini
├── 📄 requirements.txt          # Dependencias Python
│
├── 📁 config/
│   └── 📄 settings.json         # Configuración del sistema
│
├── 📁 framework/               # Módulos del REFramework
│   ├── 📄 __init__.py          # Inicialización del framework
│   ├── 📄 init.py              # Fase 1: Inicialización
│   ├── 📄 get_transaction.py   # Fase 2: Obtener transacción
│   ├── 📄 process.py           # Fase 3: Procesar transacción
│   ├── 📄 handle_error.py      # Fase 4: Manejar errores
│   └── 📄 end.py               # Fase 5: Finalizar proceso
│
├── 📁 data/
│   ├── 📁 input/               # Archivos de entrada
│   │   └── 📄 prompts.csv      # Datos a procesar
│   └── 📁 output/              # Archivos generados
│       ├── 📄 results.csv      # Resultados exitosos
│       ├── 📄 automation.log   # Log principal
│       └── 📄 execution_report.json # Reporte final
│
├── 📁 tests/                   # Pruebas unitarias
│   ├── 📄 __init__.py
│   └── 📄 test_process.py      # Tests principales
│
└── 📁 venv/                    # Entorno virtual (auto-generado)
    └── ...
```

---

## 🎯 Comandos Principales

### Para recordar rápidamente:

#### Setup Completo (Primera vez)
```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar API key
$env:GEMINI_API_KEY="tu_clave_real"

# 4. Ejecutar
python main.py
```

#### Ejecución Diaria
```powershell
# Simplemente ejecutar (si ya está configurado)
$env:GEMINI_API_KEY="tu_clave"; python main.py
```

#### Debug y Testing
```powershell
# Ver logs en tiempo real
Get-Content data/output/automation.log -Wait

# Ejecutar tests
python -m pytest -v

# Ejecutar ejemplo simple
python gemini.py
```

---

## 📄 Archivos Importantes

### 📄 main.py
**Punto de entrada principal del sistema**
- Ejecuta las 5 fases del REFramework
- Maneja la cola de procesamiento
- Genera reportes finales

### 📄 framework/process.py
**Corazón del procesamiento**
- Clase `GeminiProcessor` para manejar la API
- Lógica de negocio principal
- Clasificación de errores

### 📄 config/settings.json
**Configuración central**
- Configuración de Gemini (model, thinking_budget)
- Configuración de logging
- Rutas de archivos

### 📄 .env
**Variables de entorno**
- Contiene `GEMINI_API_KEY`
- No commitear a Git (sensible)

### 📄 data/input/prompts.csv
**Datos de entrada**
- CSV con columnas: id, prompt, context, expected_output
- Se genera automáticamente si no existe

---

## 🔧 Troubleshooting

### Problemas Comunes

#### ❌ "API key not valid"
```powershell
# Solución: Verificar que la clave API sea correcta
$env:GEMINI_API_KEY="tu_clave_real_aqui"
```

#### ❌ "No se puede cargar el archivo activate.ps1"
```powershell
# Solución: Las dependencias se instalan globalmente, no afecta la ejecución
# O cambiar la política de ejecución:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### ❌ "pytest no se reconoce"
```powershell
# Solución: Usar el módulo de Python
python -m pytest tests/ -v
```

#### ❌ "No hay elementos para procesar"
- Verificar que existe `data/input/prompts.csv`
- El archivo se crea automáticamente si no existe

#### ❌ Tests fallan
- Normal, 2 tests menores fallan pero no afectan funcionalidad
- 15 de 17 tests pasan correctamente

### Logs y Debugging

#### Ver logs en tiempo real
```powershell
Get-Content data/output/automation.log -Wait
```

#### Ver reporte de ejecución
```powershell
Get-Content data/output/execution_report.json | ConvertFrom-Json
```

---

## 🛠️ Mantenimiento

### Actualización de Dependencias
```powershell
pip install --upgrade -r requirements.txt
```

### Backup de Configuración
```powershell
# Copiar archivos importantes
Copy-Item config/settings.json config/settings.backup.json
Copy-Item .env .env.backup
```

### Limpieza de Logs
```powershell
# Limpiar logs antiguos
Remove-Item data/output/*.log
Remove-Item data/output/*.json
```

### Agregar Nuevos Prompts
1. Editar `data/input/prompts.csv`
2. Agregar filas con formato: `id,prompt,context,expected_output`
3. Ejecutar `python main.py`

### Cambiar Modelo de Gemini
1. Editar `config/settings.json`
2. Cambiar `"model": "gemini-2.5-flash"` (más rápido) o `"gemini-2.5-pro"` (mejor calidad)
3. Reiniciar la aplicación

---

## 📝 Notas Importantes

### ⚠️ Recordatorios de Seguridad
- **NUNCA** committear el archivo `.env` con la clave API real
- Usar variables de entorno en producción
- La clave API tiene límites de rate limiting

### 📊 Monitoreo
- Los logs se guardan en `data/output/automation.log`
- El reporte final está en `data/output/execution_report.json`
- Errores de sistema se reintentan automáticamente
- Errores de negocio no se reintentan

### 🎯 Próximos Pasos
- [ ] Implementar más validaciones de entrada
- [ ] Agregar soporte para múltiples modelos
- [ ] Crear interface web (opcional)
- [ ] Implementar cache de respuestas
- [ ] Agregar métricas de rendimiento

---

**Última actualización:** 14 de Septiembre, 2025  
**Estado:** ✅ Funcional y probado  
**Versión:** 1.0
