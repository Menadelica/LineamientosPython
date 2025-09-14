"""
Módulo para manejo de errores y excepciones
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime


class ErrorHandler:
    """Manejador de errores para el framework"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el manejador de errores
        
        Args:
            config: Configuración del framework
        """
        self.logger = logging.getLogger('gemini_automation.handle_error')
        self.config = config
        self.max_retries = config['processing']['max_retries']
        self.retry_delay = config['processing']['retry_delay']
    
    def handle_business_exception(self, item: Dict[str, Any], error: Exception) -> None:
        """
        Maneja errores de negocio (datos inválidos, lógica de negocio)
        
        Args:
            item: Elemento que falló
            error: Excepción ocurrida
        """
        self.logger.warning(f"Business Exception en item {item.get('id', 'unknown')}: {error}")
        
        # Registrar en archivo de errores de negocio
        self._log_business_error(item, error)
        
        # Marcar como fallo controlado
        self._mark_as_failed(item, 'BusinessException', str(error))
    
    def handle_system_exception(self, item: Dict[str, Any], error: Exception, retry_count: int = 0) -> bool:
        """
        Maneja errores de sistema (infraestructura, red, APIs)
        
        Args:
            item: Elemento que falló
            error: Excepción ocurrida
            retry_count: Número de reintentos actual
            
        Returns:
            True si se debe reintentar, False si no
        """
        self.logger.error(f"System Exception en item {item.get('id', 'unknown')}: {error}")
        
        if retry_count < self.max_retries:
            self.logger.info(f"Reintentando en {self.retry_delay} segundos... (intento {retry_count + 1}/{self.max_retries})")
            time.sleep(self.retry_delay)
            return True
        else:
            self.logger.error(f"Agotados los reintentos para item {item.get('id', 'unknown')}")
            self._log_system_error(item, error)
            self._mark_as_failed(item, 'SystemException', str(error))
            return False
    
    def _log_business_error(self, item: Dict[str, Any], error: Exception) -> None:
        """
        Registra errores de negocio en archivo específico
        
        Args:
            item: Elemento que falló
            error: Excepción ocurrida
        """
        error_log_path = self.config['paths']['logs'] + 'business_errors.log'
        
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'item_id': item.get('id', 'unknown'),
            'error_type': 'BusinessException',
            'error_message': str(error),
            'item_data': item
        }
        
        with open(error_log_path, 'a', encoding='utf-8') as f:
            f.write(f"{error_entry}\n")
    
    def _log_system_error(self, item: Dict[str, Any], error: Exception) -> None:
        """
        Registra errores de sistema en archivo específico
        
        Args:
            item: Elemento que falló
            error: Excepción ocurrida
        """
        error_log_path = self.config['paths']['logs'] + 'system_errors.log'
        
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'item_id': item.get('id', 'unknown'),
            'error_type': 'SystemException',
            'error_message': str(error),
            'item_data': item
        }
        
        with open(error_log_path, 'a', encoding='utf-8') as f:
            f.write(f"{error_entry}\n")
    
    def _mark_as_failed(self, item: Dict[str, Any], error_type: str, error_message: str) -> None:
        """
        Marca un elemento como fallido en el archivo de resultados
        
        Args:
            item: Elemento que falló
            error_type: Tipo de error
            error_message: Mensaje de error
        """
        failed_items_path = self.config['paths']['output_data'].replace('.csv', '_failed.csv')
        
        failed_entry = {
            'id': item.get('id', 'unknown'),
            'prompt': item.get('prompt', ''),
            'context': item.get('context', ''),
            'expected_output': item.get('expected_output', ''),
            'status': 'failed',
            'error_type': error_type,
            'error_message': error_message,
            'failed_at': datetime.now().isoformat()
        }
        
        # Verificar si el archivo existe para agregar headers
        file_exists = False
        try:
            with open(failed_items_path, 'r', encoding='utf-8') as f:
                file_exists = True
        except FileNotFoundError:
            file_exists = False
        
        import csv
        with open(failed_items_path, 'a', newline='', encoding='utf-8') as f:
            fieldnames = failed_entry.keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(failed_entry)


def run(item: Dict[str, Any], error: Exception, error_type: Optional[str] = None) -> None:
    """
    Función principal de manejo de errores
    
    Args:
        item: Elemento que falló
        error: Excepción ocurrida
        error_type: Tipo de error (BusinessException/SystemException)
    """
    # Cargar configuración
    from .init import load_config
    config = load_config()
    
    # Crear manejador de errores
    handler = ErrorHandler(config)
    
    # Clasificar error si no se proporcionó el tipo
    if not error_type:
        error_type = _classify_error(error)
    
    # Manejar según el tipo
    if error_type == 'BusinessException':
        handler.handle_business_exception(item, error)
    else:  # SystemException
        handler.handle_system_exception(item, error)


def _classify_error(error: Exception) -> str:
    """
    Clasifica el error como BusinessException o SystemException
    
    Args:
        error: Excepción ocurrida
        
    Returns:
        Tipo de error clasificado
    """
    # Errores de sistema (infraestructura, API, red)
    system_errors = [
        'ConnectionError',
        'TimeoutError',
        'APIError', 
        'AuthenticationError',
        'RateLimitError',
        'NetworkError'
    ]
    
    error_type = type(error).__name__
    if any(sys_error in error_type for sys_error in system_errors):
        return 'SystemException'
    
    # Errores de negocio (datos inválidos, lógica de negocio)
    return 'BusinessException'
