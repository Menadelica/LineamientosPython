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
    logger = logging.getLogger('gemini_automation.get_transaction')
    
    try:
        # Validar campos requeridos
        required_fields = ['id', 'prompt']
        for field in required_fields:
            if field not in item or not item[field]:
                raise ValueError(f"Campo requerido '{field}' está vacío o ausente")
        
        # Preparar transacción
        transaction = {
            'id': item['id'],
            'prompt': item['prompt'],
            'context': item.get('context', ''),
            'expected_output': item.get('expected_output', ''),
            'status': 'pending'
        }
        
        logger.info(f"Transacción {transaction['id']} preparada correctamente")
        return transaction
        
    except Exception as e:
        logger.error(f"Error al preparar transacción {item.get('id', 'unknown')}: {e}")
        raise


def validate_prompt(prompt: str) -> bool:
    """
    Valida que el prompt tenga el formato correcto
    
    Args:
        prompt: Texto del prompt a validar
        
    Returns:
        True si el prompt es válido
    """
    if not prompt or len(prompt.strip()) < 10:
        return False
    
    # Validaciones adicionales pueden agregarse aquí
    return True


def enrich_transaction(transaction: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enriquece la transacción con información adicional
    
    Args:
        transaction: Transacción base
        
    Returns:
        Transacción enriquecida
    """
    # Agregar timestamp
    from datetime import datetime
    transaction['created_at'] = datetime.now().isoformat()
    
    # Agregar metadata
    transaction['metadata'] = {
        'source': 'csv_input',
        'version': '1.0',
        'processed_by': 'gemini_automation'
    }
    
    return transaction
