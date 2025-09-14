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
    
    # Inicialización
    try:
        print("🚀 Iniciando automatización de generación de prompts con Gemini...")
        
        # Verificar dependencias
        if not init.verify_dependencies():
            print("❌ Faltan dependencias requeridas. Instala con: pip install -r requirements.txt")
            sys.exit(1)
        
        # Cargar configuración
        config = init.load_config()
        print(f"✅ Configuración cargada desde: config/settings.json")
        
        # Configurar logging
        logger = init.setup_logging(config)
        logger.info("Automatización iniciada")
        
        # Cargar cola de procesamiento
        input_path = config['paths']['input_data']
        queue = init.load_queue(input_path)
        logger.info(f"Cargados {len(queue)} elementos para procesar desde: {input_path}")
        
        if not queue:
            print("⚠️  No hay elementos para procesar en la cola")
            return
        
        # Procesar elementos
        start_time = datetime.now()
        successful_results = []
        failed_items = []
        
        print(f"📋 Procesando {len(queue)} elementos...")
        
        for i, item in enumerate(queue, 1):
            try:
                print(f"🔄 Procesando elemento {i}/{len(queue)}: {item.get('id', 'unknown')}")
                
                # Obtener y validar transacción
                transaction = get_transaction.run(item)
                
                # Procesar transacción
                status, result = process.run(transaction, config)
                
                if status == 'Success':
                    successful_results.append(result)
                    print(f"✅ Elemento {transaction['id']} procesado exitosamente")
                    logger.info(f"Elemento {transaction['id']} procesado exitosamente")
                else:
                    failed_items.append(item)
                    print(f"❌ Elemento {transaction['id']} falló con status: {status}")
                    logger.error(f"Elemento {transaction['id']} falló con status: {status}")
                    
            except Exception as e:
                failed_items.append(item)
                print(f"💥 Error inesperado en elemento {item.get('id', 'unknown')}: {e}")
                logger.error(f"Error inesperado en elemento {item.get('id', 'unknown')}: {e}")
                
                # Manejar error según su tipo
                try:
                    handle_error.run(item, e)
                except Exception as error_handling_error:
                    logger.error(f"Error al manejar el error: {error_handling_error}")
        
        # Finalización
        print("🏁 Finalizando proceso...")
        end.run(
            results=successful_results,
            failed_items=failed_items,
            start_time=start_time
        )
        
        # Resumen final
        total_items = len(queue)
        success_count = len(successful_results)
        failed_count = len(failed_items)
        success_rate = (success_count / total_items * 100) if total_items > 0 else 0
        
        print("=" * 60)
        print("📊 RESUMEN DE EJECUCIÓN")
        print("=" * 60)
        print(f"Total de elementos: {total_items}")
        print(f"Exitosos: {success_count}")
        print(f"Fallidos: {failed_count}")
        print(f"Tasa de éxito: {success_rate:.1f}%")
        print(f"Resultados guardados en: {config['paths']['output_data']}")
        print(f"Logs disponibles en: {config['logging']['file']}")
        print("=" * 60)
        
        if success_count > 0:
            print("🎉 ¡Automatización completada exitosamente!")
        else:
            print("⚠️  La automatización se completó pero sin resultados exitosos")
            
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
