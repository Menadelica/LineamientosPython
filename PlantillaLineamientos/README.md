# 🚀 Plantilla REFramework Python

Plantilla base para automatizaciones en Python siguiendo el **REFramework** adaptado de UiPath.

## 📋 Descripción

Esta plantilla proporciona una estructura estandarizada para el desarrollo de automatizaciones, garantizando código limpio, mantenible y fácil de soportar.

## 🏗️ Estructura del Proyecto

```
plantilla/
├── config/
│   └── settings.json        # Configuración general
├── data/
│   ├── input/              # Archivos de entrada
│   │   └── data.csv
│   └── output/             # Resultados generados
├── framework/
│   ├── init.py             # Inicialización del framework
│   ├── get_transaction.py  # Obtención de transacciones
│   ├── process.py          # Lógica de procesamiento
│   ├── handle_error.py     # Manejo de errores
│   └── end.py              # Finalización y limpieza
├── tests/
│   └── test_process.py     # Pruebas unitarias
├── main.py                 # Punto de entrada principal
└── requirements.txt        # Dependencias del proyecto
```

## 🚀 Instalación

1. **Clonar la plantilla:**
   ```bash
   git clone <repositorio>
   cd plantilla
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Ejecución

```bash
python main.py
```

## 🧪 Pruebas

```bash
pytest tests/
```

## 📝 Uso

1. **Configuración:** Modifica `config/settings.json` según tus necesidades
2. **Datos de entrada:** Coloca tus archivos en `data/input/`
3. **Lógica de negocio:** Implementa tu automatización en `framework/process.py`
4. **Resultados:** Los outputs se generarán en `data/output/`

## 🔧 Personalización

- **Variables de entorno:** Usa archivos `.env` para credenciales
- **Logging:** Configura niveles en `settings.json`
- **Manejo de errores:** Personaliza `framework/handle_error.py`

## 📚 Lineamientos

Este proyecto sigue las [mejores prácticas definidas](../../Lineamientos_Python_REFramework.md) para automatizaciones en Python.

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.