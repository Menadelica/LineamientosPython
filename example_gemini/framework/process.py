"""
Módulo principal de procesamiento de transacciones
Contiene la lógica de negocio para generar prompts con Gemini
"""

import logging
import os
from typing import Dict, Any, Tuple
from google import genai
from google.genai import types


class GeminiProcessor:
    """Clase para procesar prompts con Gemini API"""
    
    def __init__(self, config: Dict[str, Any], credentials: Dict[str, str]):
        """
        Inicializa el procesador de Gemini
        
        Args:
            config: Configuración del framework
            credentials: Credenciales de API
        """
        self.logger = logging.getLogger('gemini_automation.process')
        self.config = config
        self.credentials = credentials
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Inicializa el cliente de Gemini"""
        try:
            self.client = genai.Client(
                api_key=self.credentials['gemini_api_key']
            )
            self.logger.info("Cliente de Gemini inicializado correctamente")
        except Exception as e:
            self.logger.error(f"Error al inicializar cliente de Gemini: {e}")
            raise
    
    def process_transaction(self, transaction: Dict[str, Any]) -> Tuple[str, str]:
        """
        Procesa una transacción y genera el prompt con Gemini
        
        Args:
            transaction: Transacción a procesar
            
        Returns:
            Tupla con (status, resultado)
            Status puede ser: 'Success', 'BusinessException', 'SystemException'
        """
        try:
            self.logger.info(f"Iniciando procesamiento de transacción {transaction['id']}")
            
            # Preparar contenido para Gemini
            prompt_text = self._prepare_prompt(transaction)
            
            # Generar respuesta con Gemini
            response = self._generate_with_gemini(prompt_text)
            
            # Procesar respuesta
            result = self._process_response(response, transaction)
            
            self.logger.info(f"Transacción {transaction['id']} procesada exitosamente")
            return 'Success', result
            
        except Exception as e:
            error_type = self._classify_error(e)
            self.logger.error(f"Error en transacción {transaction['id']}: {e}")
            return error_type, str(e)
    
    def _prepare_prompt(self, transaction: Dict[str, Any]) -> str:
        """
        Prepara el prompt completo para enviar a Gemini
        
        Args:
            transaction: Transacción con los datos
            
        Returns:
            Prompt formateado
        """
        base_prompt = transaction['prompt']
        context = transaction.get('context', '')
        expected_output = transaction.get('expected_output', '')
        
        # Construir prompt estructurado
        full_prompt = f"""
        Como especialista en automatizaciones de UiPath, por favor ayuda con lo siguiente:
        
        Solicitud: {base_prompt}
        
        Contexto: {context if context else 'No se proporcionó contexto específico'}
        
        Resultado esperado: {expected_output if expected_output else 'Respuesta detallada y estructurada'}
        
        Por favor proporciona:
        1. Un análisis detallado del proceso
        2. Un diagrama de flujo en texto
        3. Los pasos específicos de automatización
        4. Consideraciones técnicas importantes
        5. Posibles excepciones y su manejo
        """
        
        return full_prompt.strip()
    
    def _generate_with_gemini(self, prompt_text: str) -> str:
        """
        Genera respuesta usando Gemini API
        
        Args:
            prompt_text: Texto del prompt
            
        Returns:
            Respuesta generada por Gemini
        """
        try:
            gemini_config = self.config['gemini']
            
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=prompt_text),
                    ],
                ),
            ]
            
            tools = [
                types.Tool(googleSearch=types.GoogleSearch()),
            ]
            
            generate_content_config = types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_budget=gemini_config['thinking_budget'],
                ),
                tools=tools,
                system_instruction=[
                    types.Part.from_text(text=gemini_config['system_instruction']),
                ],
            )
            
            # Generar contenido
            response_parts = []
            for chunk in self.client.models.generate_content_stream(
                model=gemini_config['model'],
                contents=contents,
                config=generate_content_config,
            ):
                if chunk.text:
                    response_parts.append(chunk.text)
            
            return ''.join(response_parts)
            
        except Exception as e:
            self.logger.error(f"Error en la generación con Gemini: {e}")
            raise
    
    def _process_response(self, response: str, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa la respuesta de Gemini y estructura el resultado
        
        Args:
            response: Respuesta de Gemini
            transaction: Transacción original
            
        Returns:
            Resultado estructurado
        """
        return {
            'transaction_id': transaction['id'],
            'original_prompt': transaction['prompt'],
            'generated_response': response,
            'status': 'completed',
            'metadata': {
                'model_used': self.config['gemini']['model'],
                'response_length': len(response),
                'has_context': bool(transaction.get('context')),
                'has_expected_output': bool(transaction.get('expected_output'))
            }
        }
    
    def _classify_error(self, error: Exception) -> str:
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
            'RateLimitError'
        ]
        
        error_type = type(error).__name__
        if any(sys_error in error_type for sys_error in system_errors):
            return 'SystemException'
        
        # Errores de negocio (datos inválidos, lógica de negocio)
        return 'BusinessException'


def run(transaction: Dict[str, Any], config: Dict[str, Any]) -> Tuple[str, str]:
    """
    Función principal de procesamiento
    
    Args:
        transaction: Transacción a procesar
        config: Configuración del framework
        
    Returns:
        Tupla con (status, resultado)
    """
    # Obtener credenciales
    from .init import load_credentials
    credentials = load_credentials()
    
    # Crear procesador y ejecutar
    processor = GeminiProcessor(config, credentials)
    return processor.process_transaction(transaction)
