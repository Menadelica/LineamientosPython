# 🚀 Referencia Rápida - Python REFramework con Gemini

## ⚡ Comandos Más Usados

### 🔧 Setup Inicial (Solo primera vez)
```powershell
python -m venv venv
pip install -r requirements.txt
```

### 🎮 Ejecución Principal
```powershell
# Configurar API key y ejecutar
$env:GEMINI_API_KEY="tu_clave_aqui"; python main.py
```

### 🔍 Ver Resultados
```powershell
# Ver reporte final
Get-Content data/output/execution_report.json | ConvertFrom-Json

# Ver logs en tiempo real
Get-Content data/output/automation.log -Wait

# Listar archivos generados
dir data/output/
```

### 🧪 Testing y Debug
```powershell
# Ejecutar tests
python -m pytest -v

# Ejemplo directo de Gemini
$env:GEMINI_API_KEY="tu_clave"; python gemini.py

# Ver ayuda
python main.py --help
```

### 📝 Editar Datos
```powershell
# Editar prompts de entrada
notepad data/input/prompts.csv

# Editar configuración
notepad config/settings.json

# Editar variables de entorno
notepad .env
```

---

## 📋 Formato de Datos de Entrada (CSV)

```csv
id,prompt,context,expected_output
1,"Tu prompt aquí","Contexto opcional","Salida esperada"
2,"Otro prompt","Más contexto","Otra salida"
```

---

## 🔑 Variables de Entorno

### Archivo .env
```env
GEMINI_API_KEY=tu_clave_api_real_aqui
```

### PowerShell (Temporal)
```powershell
$env:GEMINI_API_KEY="tu_clave_aqui"
```

---

## 📁 Archivos Importantes

| Archivo | Propósito |
|---------|-----------|
| `main.py` | Ejecutar el sistema completo |
| `gemini.py` | Ejemplo directo de API |
| `.env` | Variable de API key |
| `config/settings.json` | Configuración principal |
| `data/input/prompts.csv` | Datos a procesar |
| `data/output/automation.log` | Logs de ejecución |
| `data/output/execution_report.json` | Reporte final |

---

## 🆘 Soluciones Rápidas

### ❌ "API key not valid"
```powershell
$env:GEMINI_API_KEY="clave_correcta_aqui"
```

### ❌ "pytest no encontrado"
```powershell
python -m pytest -v
```

### ❌ "No hay elementos para procesar"
- Verificar que existe `data/input/prompts.csv`
- Se crea automáticamente con datos de ejemplo

### ❌ Error de PowerShell activate
```powershell
# No es crítico, las dependencias se instalan globalmente
pip install -r requirements.txt
```

---

## 🎯 Flujo de Trabajo Típico

1. **Configurar clave API**: `$env:GEMINI_API_KEY="tu_clave"`
2. **Editar prompts**: Modificar `data/input/prompts.csv`
3. **Ejecutar**: `python main.py`
4. **Ver resultados**: `Get-Content data/output/execution_report.json`

---

## 📊 Estados del Sistema

### ✅ Ejecución Exitosa
```
✅ Configuración cargada
📋 Procesando X elementos
✅ Elemento Y procesado exitosamente
🎉 ¡Automatización completada exitosamente!
```

### ❌ Error de API Key
```
❌ API key not valid. Please pass a valid API key.
```

### ⚠️ Sin resultados exitosos
```
⚠️ La automatización se completó pero sin resultados exitosos
```

---

**Última actualización:** 14 de Septiembre, 2025
