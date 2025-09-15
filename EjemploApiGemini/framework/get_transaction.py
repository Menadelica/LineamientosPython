"""
Módulo para obtener y validar datos de transacciones
"""

import logging
from typing import Dict, Any, Optional


def run(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Obtiene y valida los datos de una transacción
    
    Args:
        item: Elemento de la cola de procesamiento
        
    Returns:
        Transacción validada y preparada
        
    Raises:
        ValueError: Si los datos no son válidos
    """
    for field in ['id', 'prompt']:
        if field not in item or not item[field]:
            raise ValueError(f"Campo requerido '{field}' está vacío o ausente")
    
    return {
        'id': item['id'],
        'prompt': item['prompt'],
        'context': item.get('context', ''),
        'expected_output': item.get('expected_output', ''),
        'status': 'pending'
    }


def validate_prompt(prompt: str) -> bool:
    """Valida que el prompt tenga el formato correcto"""
    return bool(prompt and len(prompt.strip()) >= 10)
