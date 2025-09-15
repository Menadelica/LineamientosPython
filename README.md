# 📌 Lineamientos de Desarrollo en Python para Automatizaciones Comfama

## 🎯 Objetivo

Definir prácticas claras y estandarizadas para el desarrollo de
automatizaciones en Python, asegurando calidad, mantenibilidad y
facilidad de soporte, mediante un framework inspirado en el
**REFramework** de UiPath.

------------------------------------------------------------------------

## 🔑 Principios Generales

### 🧼 Código limpio y legible

-   Cumplir el estándar **PEP8**.
-   Usar nombres descriptivos en variables, clases y funciones.
-   Agregar comentarios solo cuando sean necesarios: el código debe ser
    autoexplicativo.

### 🧩 Estructura modular

-   Dividir la lógica en módulos reutilizables.
-   Funciones cortas y con una sola responsabilidad.

### 🛠️ Manejo de errores

-   Usar `try/except` con logging estructurado.
-   Diferenciar errores de sistema (infraestructura, red, librerías) de
    errores de negocio (datos inválidos, flujo esperado).

### ⚙️ Configuración externa

-   No incluir credenciales ni rutas en el código.
-   Usar archivos `.env`, JSON, YAML o variables de entorno.

### 📜 Logs y monitoreo

-   Implementar logging con niveles (**DEBUG**, **INFO**, **ERROR**).
-   Generar logs fáciles de rastrear para soporte y auditoría.

### 🧪 Pruebas y calidad

-   Escribir pruebas unitarias con **pytest**.
-   Validar en staging antes de pasar a producción.

------------------------------------------------------------------------

## 🏗️ Python REFramework (Adaptación)

Estructura base del framework, inspirada en UiPath REFramework:

    automation_project/
    │
    ├── config/
    │   ├── settings.json        # Configuración general
    │   ├── credentials.json     # Credenciales (encriptadas o mock)
    │
    ├── data/
    │   ├── input/               # Archivos de entrada
    │   └── output/              # Resultados
    │
    ├── framework/
    │   ├── init.py              # Inicialización: logs, configs, colas
    │   ├── get_transaction.py   # Obtención de ítems a procesar
    │   ├── process.py           # Lógica principal de negocio
    │   ├── handle_error.py      # Manejo de excepciones
    │   └── end.py               # Limpieza y cierre
    │
    ├── tests/
    │   └── test_process.py      # Pruebas unitarias
    │
    ├── main.py                  # Punto de entrada
    └── requirements.txt         # Dependencias

------------------------------------------------------------------------

## 🔄 Fases del Flujo

1.  **Initialization**\
    Cargar configuraciones y credenciales. Preparar logging. Verificar
    dependencias (APIs, DB, rutas de archivos).

2.  **Get Transaction Data**\
    Obtener ítems de entrada (archivos, registros, requests). Validar
    datos antes de procesar.

3.  **Process Transaction**\
    Ejecutar la lógica de negocio para cada ítem.\
    Devolver estado: `Success`, `BusinessException`, `SystemException`.

4.  **Handle Errors**

    -   **BusinessException:** registrar y marcar ítem como fallo
        controlado.\
    -   **SystemException:** reintentar o escalar.\
        Siempre dejar trazabilidad clara en los logs.

5.  **End Process**\
    Generar reporte final de ejecución.\
    Cerrar conexiones, liberar recursos.

------------------------------------------------------------------------

## 📝 Ejemplo simplificado (`main.py`)

``` python
from framework import init, get_transaction, process, handle_error, end

if __name__ == "__main__":
    config = init.load_config()
    queue = init.load_queue("data/input/data.csv")

    for item in queue:
        try:
            tx = get_transaction.run(item)
            result = process.run(tx, config)
            print(f"[OK] {item} -> {result}")
        except Exception as e:
            handle_error.run(item, e)

    end.run()
```

------------------------------------------------------------------------

## 🚦 Buenas Prácticas Adicionales

-   **Versionamiento:** usar Git con ramas claras (`feature/`, `fix/`,
    `release/`).
-   **Entornos virtuales:** crear con `venv` o `poetry`.
-   **Documentación mínima:** incluir `README` con dependencias, pasos
    de ejecución y diagrama de flujo.
-   **Estandarización:** todos los proyectos deben seguir esta misma
    estructura.

------------------------------------------------------------------------

## ✅ Conclusión

Este marco asegura que todas las automatizaciones en Python tengan
**orden**, **trazabilidad**, sean **fáciles de mantener** y permitan
**escalar de manera segura** dentro del equipo.
