"""
Framework de automatización para generación de prompts con Gemini
Basado en el REFramework de UiPath
"""

from . import init, get_transaction, process, handle_error, end, utils

__version__ = "1.0.0"
__author__ = "Equipo de Automatización"

__all__ = ['init', 'get_transaction', 'process', 'handle_error', 'end', 'utils']
