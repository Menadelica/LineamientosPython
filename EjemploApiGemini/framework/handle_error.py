"""
Módulo para manejo de errores y excepciones
"""

import csv
import logging
import os
from datetime import datetime
from typing import Dict, Any
from .utils import classify_error


def log_error(item: Dict[str, Any], error: Exception, config: Dict[str, Any]) -> None:
    """Registra el error en los archivos correspondientes"""
    failed_items_path = config['paths']['output_data'].replace('.csv', '_failed.csv')
    
    failed_entry = {
        'id': item.get('id', 'unknown'),
        'prompt': item.get('prompt', ''),
        'context': item.get('context', ''),
        'expected_output': item.get('expected_output', ''),
        'status': 'failed',
        'error_type': classify_error(error),
        'error_message': str(error),
        'failed_at': datetime.now().isoformat()
    }
    
    # Escribir al archivo de errores
    file_exists = os.path.exists(failed_items_path)
    with open(failed_items_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=failed_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(failed_entry)


def run(item: Dict[str, Any], error: Exception) -> None:
    """
    Función principal de manejo de errores
    
    Args:
        item: Elemento que falló
        error: Excepción ocurrida
    """
    from .init import load_config
    config = load_config()
    log_error(item, error, config)
