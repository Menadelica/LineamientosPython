#  Lineamientos - Desarrollo - Python 

## 🎯 Objetivo

Establecer y aplicar prácticas estandarizadas para el desarrollo en Python, promoviendo la colaboración entre equipos de desarrollo, QA y soporte. Esto garantizará la calidad, mantenibilidad y facilidad de soporte del código, mediante la implementación de un framework inspirado en el REFramework de UiPath.

------------------------------------------------------------------------

## 🔑 Principios Generales

### 🧼 Código limpio y legible

Seguir el estándar [PEP 8](https://peps.python.org/pep-0008/?utm_source=chatgpt.com), la guía oficial de estilo para Python que define convenciones para la indentación, nombres de variables, longitud de líneas, organización de funciones y comentarios. 

### 🧩 Estructura modular

Organiza el código en módulos reutilizables y funciones con única responsabilidad, mejorando legibilidad, mantenimiento, pruebas y escalabilidad.

### 🛠️ Manejo de errores

Usa try/except con logging estructurado y diferencia:

- 🖧 Errores de sistema → 🔁 reintentar o escalar.
- 📊 Errores de negocio → 📝 registrar y continuar.

### ⚙️ Configuración externa

- No incluyas credenciales ni rutas sensibles en el código.
- Usa archivos .env, JSON, YAML o variables de entorno.
- Mantén estos archivos fuera del control de versiones y ofrecer un .env.example.

### 📜 Logs y monitoreo

-   Implementar logging con niveles (**DEBUG**, **INFO**, **ERROR**).
-   Generar logs fáciles de rastrear para soporte y auditoría.

### 🧪 Pruebas y calidad

- Escribe pruebas unitarias con [pytest](https://docs.pytest.org/en/stable/contents.html?utm_source=chatgpt.com).

- Valida los cambios en un entorno de prueba staging antes de desplegar.

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

1. **Initialization** – Configuraciones, credenciales, logging y verificación de dependencias.  
2. **Get Transaction Data** – Obtener y validar ítems de entrada.  
3. **Process Transaction** – Ejecutar lógica de negocio, devolver `Success`, `BusinessException` o `SystemException`.  
4. **Handle Errors** – Registrar excepciones. Reintentar o escalar según tipo.  
5. **End Process** – Generar reporte final y liberar recursos.  


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
