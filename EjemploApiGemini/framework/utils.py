"""
Utilidades compartidas del framework
"""

import logging


def classify_error(error: Exception) -> str:
    """
    Clasifica el error como BusinessException o SystemException
    
    Args:
        error: Excepción ocurrida
        
    Returns:
        Tipo de error clasificado
    """
    system_errors = [
        'ConnectionError', 'TimeoutError', 'APIError', 
        'AuthenticationError', 'RateLimitError', 'NetworkError'
    ]
    
    error_type = type(error).__name__
    return 'SystemException' if any(sys_error in error_type for sys_error in system_errors) else 'BusinessException'


def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """
    Configura y retorna un logger simple
    
    Args:
        name: Nombre del logger
        level: Nivel de logging
        
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(getattr(logging, level))
    return logger
