# 🤖 Automatización de Generación de Prompts con Gemini

Sistema de automatización para generar prompts especializados en flujos de UiPath utilizando la API de Google Gemini, implementado siguiendo el **Python REFramework** basado en las mejores prácticas de UiPath.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Ejemplos](#-ejemplos)
- [Testing](#-testing)
- [Arquitectura](#-arquitectura)
- [Contribución](#-contribución)

## ✨ Características

- 🏗️ **Framework REFramework**: Estructura modular basada en las mejores prácticas de UiPath
- 🤖 **Integración con Gemini**: Utiliza la API de Google Gemini para generación de contenido
- 📊 **Logging estructurado**: Sistema completo de logs para trazabilidad y auditoría
- 🔄 **Manejo robusto de errores**: Diferenciación entre errores de sistema y de negocio
- 📈 **Reportes detallados**: Generación automática de reportes de ejecución
- 🧪 **Pruebas unitarias**: Suite completa de tests con pytest
- ⚙️ **Configuración externa**: Sin credenciales hardcodeadas en el código

## 📁 Estructura del Proyecto

```
automation_project/
│
├── config/
│   └── settings.json        # Configuración general del sistema
│
├── data/
│   ├── input/               # Archivos de entrada
│   │   └── prompts.csv      # Datos de prompts a procesar
│   └── output/              # Resultados generados
│       ├── results.csv      # Resultados exitosos
│       ├── automation.log   # Log de ejecución
│       └── execution_report.json # Reporte final
│
├── framework/               # Módulos del REFramework
│   ├── __init__.py         # Inicialización del framework
│   ├── init.py             # Carga de configs, logs, colas
│   ├── get_transaction.py  # Obtención de ítems a procesar
│   ├── process.py          # Lógica principal de negocio
│   ├── handle_error.py     # Manejo de excepciones
│   └── end.py              # Limpieza y cierre
│
├── tests/                   # Pruebas unitarias
│   ├── __init__.py
│   └── test_process.py     # Tests del módulo de procesamiento
│
├── main.py                  # Punto de entrada principal
├── gemini.py               # Ejemplo de uso directo de Gemini
├── requirements.txt         # Dependencias del proyecto
└── README.md               # Este archivo
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Clave API de Google Gemini

### Pasos de instalación

1. **Clonar o descargar el repositorio**
   ```bash
   git clone <repository-url>
   cd automation_project
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   
   # En Windows
   venv\Scripts\activate
   
   # En Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variable de entorno**
   ```bash
   # En Windows
   set GEMINI_API_KEY=tu_clave_api_aqui
   
   # En Linux/Mac
   export GEMINI_API_KEY=tu_clave_api_aqui
   ```

## ⚙️ Configuración

### Archivo de configuración (`config/settings.json`)

El archivo de configuración contiene todas las configuraciones del sistema:

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

### Archivo de datos de entrada (`data/input/prompts.csv`)

El archivo CSV debe contener las siguientes columnas:

```csv
id,prompt,context,expected_output
1,"Crea un flujo de UiPath para automatizar el proceso de facturación","Sistema ERP con interfaz web","Diagrama de flujo detallado"
2,"Diseña una automatización para procesar emails entrantes","Cliente de email corporativo","Workflow con decisiones y excepciones"
```

## 🎯 Uso

### Ejecución principal

```bash
python main.py
```

### Ejecución con ayuda

```bash
python main.py --help
```

### Ejemplo de uso directo de Gemini

```bash
python gemini.py
```

## 📝 Ejemplos

### Ejemplo básico de ejecución

```bash
# 1. Configurar la API key
export GEMINI_API_KEY=tu_clave_api

# 2. Ejecutar la automatización
python main.py

# 3. Verificar resultados
cat data/output/results.csv
cat data/output/execution_report.json
```

### Ejemplo de datos de entrada

Crear el archivo `data/input/prompts.csv`:

```csv
id,prompt,context,expected_output
1,"Automatizar proceso de facturación en SAP","Sistema SAP con interfaz web","Flujo detallado con pasos específicos"
2,"Crear automatización para procesar PDFs","Documentos PDF con datos estructurados","Workflow con OCR y extracción de datos"
3,"Diseñar flujo para integración con APIs REST","API REST con autenticación OAuth","Secuencia de llamadas y manejo de errores"
```

## 🧪 Testing

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar pruebas con cobertura

```bash
pytest --cov=framework tests/
```

### Ejecutar pruebas específicas

```bash
pytest tests/test_process.py::TestGeminiProcessor::test_processor_initialization
```

## 🏗️ Arquitectura

### Flujo del REFramework

1. **Initialization** (`framework/init.py`)
   - Carga configuraciones y credenciales
   - Configura sistema de logging
   - Verifica dependencias

2. **Get Transaction Data** (`framework/get_transaction.py`)
   - Obtiene ítems de entrada desde CSV
   - Valida datos antes de procesar

3. **Process Transaction** (`framework/process.py`)
   - Ejecuta lógica de negocio con Gemini API
   - Retorna estado: `Success`, `BusinessException`, `SystemException`

4. **Handle Errors** (`framework/handle_error.py`)
   - Maneja errores de negocio y sistema
   - Implementa reintentos para errores de sistema
   - Registra fallos controlados

5. **End Process** (`framework/end.py`)
   - Genera reporte final de ejecución
   - Guarda resultados en CSV
   - Limpia recursos

### Clasificación de Errores

- **BusinessException**: Datos inválidos, lógica de negocio incorrecta
- **SystemException**: Errores de infraestructura, red, APIs

## 📊 Logs y Monitoreo

### Archivos de log generados

- `data/output/automation.log`: Log principal de ejecución
- `data/output/business_errors.log`: Errores de negocio
- `data/output/system_errors.log`: Errores de sistema
- `data/output/execution_report.json`: Reporte final con estadísticas

### Niveles de log

- **DEBUG**: Información detallada para debugging
- **INFO**: Información general del proceso
- **WARNING**: Advertencias y errores de negocio
- **ERROR**: Errores de sistema y excepciones críticas

## 🔧 Personalización

### Modificar el modelo de Gemini

Editar `config/settings.json`:

```json
{
    "gemini": {
        "model": "gemini-2.5-flash",  // Cambiar modelo
        "thinking_budget": 1000,      // Ajustar presupuesto
        "system_instruction": "Tu instrucción personalizada"
    }
}
```

### Agregar validaciones personalizadas

Modificar `framework/get_transaction.py`:

```python
def validate_prompt(prompt: str) -> bool:
    # Agregar validaciones personalizadas
    if len(prompt.split()) < 5:
        return False
    # ... más validaciones
    return True
```

## 🤝 Contribución

### Estándares de código

- Seguir **PEP8** para estilo de código
- Usar nombres descriptivos en variables y funciones
- Agregar docstrings en todas las funciones públicas
- Escribir pruebas unitarias para nueva funcionalidad

### Proceso de contribución

1. Fork del repositorio
2. Crear rama para nueva funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Para reportar problemas o solicitar funcionalidades:

1. Crear un issue en el repositorio
2. Incluir logs relevantes
3. Describir pasos para reproducir el problema
4. Especificar versión de Python y dependencias

## 📚 Referencias

- [Documentación de Google Gemini API](https://ai.google.dev/docs)
- [PEP 8 - Style Guide for Python Code](https://pep8.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [UiPath REFramework](https://docs.uipath.com/reframework/)

---

**Desarrollado siguiendo los lineamientos del Python REFramework para automatizaciones robustas y mantenibles.** 🚀
