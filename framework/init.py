"""
Módulo de inicialización del framework
Carga configuraciones, credenciales y prepara logging
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, List


def load_config(config_path: str = "config/settings.json") -> Dict[str, Any]:
    """
    Carga la configuración desde el archivo JSON
    
    Args:
        config_path: Ruta al archivo de configuración
        
    Returns:
        Dict con la configuración cargada
        
    Raises:
        FileNotFoundError: Si no se encuentra el archivo de configuración
        json.JSONDecodeError: Si el archivo JSON está mal formateado
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Crear directorios de salida si no existen
        output_dir = Path(config['paths']['logs']).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error al parsear el archivo de configuración: {e}")


def load_credentials() -> Dict[str, str]:
    """
    Carga las credenciales desde variables de entorno
    
    Returns:
        Dict con las credenciales
        
    Raises:
        ValueError: Si faltan credenciales requeridas
    """
    credentials = {}
    
    # Cargar API key de Gemini desde variable de entorno
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
    
    credentials['gemini_api_key'] = gemini_api_key
    return credentials


def setup_logging(config: Dict[str, Any]) -> logging.Logger:
    """
    Configura el sistema de logging
    
    Args:
        config: Configuración del framework
        
    Returns:
        Logger configurado
    """
    log_config = config['logging']
    
    # Configurar formato
    formatter = logging.Formatter(log_config['format'])
    
    # Configurar logger principal
    logger = logging.getLogger('gemini_automation')
    logger.setLevel(getattr(logging, log_config['level']))
    
    # Evitar duplicar handlers
    if not logger.handlers:
        # Handler para archivo
        file_handler = logging.FileHandler(log_config['file'], encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def load_queue(input_path: str) -> List[Dict[str, Any]]:
    """
    Carga los elementos de la cola de procesamiento
    
    Args:
        input_path: Ruta al archivo de entrada
        
    Returns:
        Lista de elementos a procesar
    """
    import csv
    
    if not os.path.exists(input_path):
        # Crear archivo de ejemplo si no existe
        create_sample_input(input_path)
    
    queue = []
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            queue.append(row)
    
    return queue


def create_sample_input(input_path: str) -> None:
    """
    Crea un archivo de entrada de ejemplo
    
    Args:
        input_path: Ruta donde crear el archivo
    """
    import csv
    
    # Crear directorio si no existe
    os.makedirs(os.path.dirname(input_path), exist_ok=True)
    
    sample_data = [
        {
            'id': '1',
            'prompt': 'Crea un flujo de UiPath para automatizar el proceso de facturación',
            'context': 'Sistema ERP con interfaz web',
            'expected_output': 'Diagrama de flujo detallado'
        },
        {
            'id': '2', 
            'prompt': 'Diseña una automatización para procesar emails entrantes',
            'context': 'Cliente de email corporativo',
            'expected_output': 'Workflow con decisiones y excepciones'
        }
    ]
    
    with open(input_path, 'w', newline='', encoding='utf-8') as f:
        if sample_data:
            fieldnames = sample_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_data)


def verify_dependencies() -> bool:
    """
    Verifica que todas las dependencias estén disponibles
    
    Returns:
        True si todas las dependencias están disponibles
    """
    required_modules = ['google.genai', 'json', 'logging', 'csv']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Módulos faltantes: {', '.join(missing_modules)}")
        print("Instala las dependencias con: pip install -r requirements.txt")
        return False
    
    return True
