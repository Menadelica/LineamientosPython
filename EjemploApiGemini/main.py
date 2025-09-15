"""
Punto de entrada principal para la automatización de generación de prompts con Gemini
Basado en el REFramework de UiPath

Uso:
    python main.py

Variables de entorno requeridas:
    GEMINI_API_KEY: Clave API de Google Gemini
"""

import sys
import logging
from datetime import datetime
from typing import List, Dict, Any

# Importar módulos del framework
from framework import init, get_transaction, process, handle_error, end


def main():
    """Función principal de la automatización"""
    try:
        print("🚀 Iniciando automatización de generación de prompts con Gemini...")
        
        if not init.verify_dependencies():
            sys.exit("❌ Faltan dependencias requeridas. Instala con: pip install -r requirements.txt")
        
        config = init.load_config()
        logger = init.setup_logging(config)
        queue = init.load_queue(config['paths']['input_data'])
        
        if not queue:
            return print("⚠️  No hay elementos para procesar en la cola")

        start_time = datetime.now()
        successful_results, failed_items = [], []
        print(f"📋 Procesando {len(queue)} elementos...")
        
        for i, item in enumerate(queue, 1):
            try:
                print(f"🔄 Procesando elemento {i}/{len(queue)}: {item.get('id', 'unknown')}")
                transaction = get_transaction.run(item)
                status, result = process.run(transaction, config)
                
                if status == 'Success':
                    successful_results.append(result)
                    print(f"✅ Elemento {transaction['id']} procesado exitosamente")
                else:
                    failed_items.append(item)
                    print(f"❌ Elemento {transaction['id']} falló: {status}")
                    
            except Exception as e:
                failed_items.append(item)
                print(f"💥 Error en elemento {item.get('id', 'unknown')}: {e}")
                handle_error.run(item, e)

        print("🏁 Finalizando proceso...")
        end.run(results=successful_results, failed_items=failed_items, start_time=start_time)
        
        # Resumen final
        total, success, failed = len(queue), len(successful_results), len(failed_items)
        rate = (success / total * 100) if total > 0 else 0
        
        print(f"\n📊 RESUMEN: {success}/{total} exitosos ({rate:.1f}%)")
        print(f"🎉 ¡Completado!" if success > 0 else "⚠️ Sin resultados exitosos")
            
    except KeyboardInterrupt:
        print("\n⏹️  Proceso interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Error crítico: {e}")
        logging.error(f"Error crítico: {e}")
        sys.exit(1)


def show_usage():
    """Muestra información de uso del programa"""
    print("""
🤖 Automatización de Generación de Prompts con Gemini

Uso:
    python main.py

Configuración requerida:
    1. Establecer variable de entorno GEMINI_API_KEY
    2. Configurar archivo config/settings.json
    3. Colocar datos de entrada en data/input/prompts.csv

Estructura de datos de entrada (CSV):
    id,prompt,context,expected_output
    1,"Crea un flujo de UiPath para...","Sistema ERP","Diagrama detallado"

Archivos generados:
    - data/output/results.csv: Resultados exitosos
    - data/output/automation.log: Log de ejecución
    - data/output/execution_report.json: Reporte final
    """)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_usage()
    else:
        main()
