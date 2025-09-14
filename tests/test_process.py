"""
Pruebas unitarias para el módulo de procesamiento
"""

import pytest
import json
import tempfile
import os
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Importar módulos del framework
from framework.process import GeminiProcessor
from framework.init import load_config


class TestGeminiProcessor:
    """Pruebas para la clase GeminiProcessor"""
    
    @pytest.fixture
    def sample_config(self):
        """Configuración de ejemplo para las pruebas"""
        return {
            'gemini': {
                'model': 'gemini-2.5-pro',
                'thinking_budget': -1,
                'system_instruction': 'Eres un agente especializado en flujos de UiPath'
            },
            'logging': {
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'file': 'test.log'
            },
            'processing': {
                'max_retries': 3,
                'retry_delay': 5,
                'batch_size': 10
            },
            'paths': {
                'input_data': 'test_input.csv',
                'output_data': 'test_output.csv',
                'logs': 'test_logs/'
            }
        }
    
    @pytest.fixture
    def sample_credentials(self):
        """Credenciales de ejemplo para las pruebas"""
        return {
            'gemini_api_key': 'test_api_key'
        }
    
    @pytest.fixture
    def sample_transaction(self):
        """Transacción de ejemplo para las pruebas"""
        return {
            'id': '1',
            'prompt': 'Crea un flujo de UiPath para automatizar facturación',
            'context': 'Sistema ERP con interfaz web',
            'expected_output': 'Diagrama de flujo detallado',
            'status': 'pending'
        }
    
    @patch('framework.process.genai.Client')
    def test_processor_initialization(self, mock_client, sample_config, sample_credentials):
        """Prueba la inicialización del procesador"""
        processor = GeminiProcessor(sample_config, sample_credentials)
        
        assert processor.config == sample_config
        assert processor.credentials == sample_credentials
        mock_client.assert_called_once_with(api_key='test_api_key')
    
    def test_prepare_prompt(self, sample_config, sample_credentials, sample_transaction):
        """Prueba la preparación del prompt"""
        with patch('framework.process.genai.Client'):
            processor = GeminiProcessor(sample_config, sample_credentials)
            
            prepared_prompt = processor._prepare_prompt(sample_transaction)
            
            assert 'Crea un flujo de UiPath para automatizar facturación' in prepared_prompt
            assert 'Sistema ERP con interfaz web' in prepared_prompt
            assert 'Diagrama de flujo detallado' in prepared_prompt
            assert 'análisis detallado del proceso' in prepared_prompt
    
    def test_prepare_prompt_without_context(self, sample_config, sample_credentials):
        """Prueba la preparación del prompt sin contexto"""
        with patch('framework.process.genai.Client'):
            processor = GeminiProcessor(sample_config, sample_credentials)
            
            transaction = {
                'id': '1',
                'prompt': 'Test prompt',
                'context': '',
                'expected_output': ''
            }
            
            prepared_prompt = processor._prepare_prompt(transaction)
            
            assert 'Test prompt' in prepared_prompt
            assert 'No se proporcionó contexto específico' in prepared_prompt
    
    @patch('framework.process.genai.Client')
    def test_classify_error_business_exception(self, mock_client, sample_config, sample_credentials):
        """Prueba la clasificación de errores de negocio"""
        processor = GeminiProcessor(sample_config, sample_credentials)
        
        # Error de negocio (datos inválidos)
        error = ValueError("Datos inválidos")
        error_type = processor._classify_error(error)
        
        assert error_type == 'BusinessException'
    
    @patch('framework.process.genai.Client')
    def test_classify_error_system_exception(self, mock_client, sample_config, sample_credentials):
        """Prueba la clasificación de errores de sistema"""
        processor = GeminiProcessor(sample_config, sample_credentials)
        
        # Error de sistema (conexión)
        error = ConnectionError("Error de conexión")
        error_type = processor._classify_error(error)
        
        assert error_type == 'SystemException'


class TestProcessModule:
    """Pruebas para el módulo process"""
    
    @patch('framework.process.load_credentials')
    @patch('framework.process.GeminiProcessor')
    def test_run_function(self, mock_processor_class, mock_load_credentials):
        """Prueba la función run del módulo process"""
        # Configurar mocks
        mock_credentials = {'gemini_api_key': 'test_key'}
        mock_load_credentials.return_value = mock_credentials
        
        mock_processor = Mock()
        mock_processor.process_transaction.return_value = ('Success', 'result')
        mock_processor_class.return_value = mock_processor
        
        # Datos de prueba
        transaction = {
            'id': '1',
            'prompt': 'Test prompt',
            'context': 'Test context'
        }
        config = {
            'gemini': {
                'model': 'gemini-2.5-pro',
                'thinking_budget': -1,
                'system_instruction': 'Test instruction'
            }
        }
        
        # Ejecutar función
        from framework.process import run
        status, result = run(transaction, config)
        
        # Verificar resultados
        assert status == 'Success'
        assert result == 'result'
        mock_load_credentials.assert_called_once()
        mock_processor_class.assert_called_once_with(config, mock_credentials)
        mock_processor.process_transaction.assert_called_once_with(transaction)


class TestInitModule:
    """Pruebas para el módulo init"""
    
    def test_load_config_success(self):
        """Prueba la carga exitosa de configuración"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_data = {
                'gemini': {
                    'model': 'gemini-2.5-pro',
                    'thinking_budget': -1
                },
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    'file': 'test.log'
                },
                'paths': {
                    'logs': 'test_logs/'
                }
            }
            json.dump(config_data, f)
            config_path = f.name
        
        try:
            config = load_config(config_path)
            assert config == config_data
        finally:
            os.unlink(config_path)
    
    def test_load_config_file_not_found(self):
        """Prueba el manejo de archivo de configuración no encontrado"""
        with pytest.raises(FileNotFoundError):
            load_config('nonexistent_config.json')
    
    def test_load_config_invalid_json(self):
        """Prueba el manejo de JSON inválido"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('invalid json content')
            config_path = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                load_config(config_path)
        finally:
            os.unlink(config_path)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'})
    def test_load_credentials_success(self):
        """Prueba la carga exitosa de credenciales"""
        from framework.init import load_credentials
        
        credentials = load_credentials()
        assert credentials['gemini_api_key'] == 'test_api_key'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_load_credentials_missing_key(self):
        """Prueba el manejo de clave API faltante"""
        from framework.init import load_credentials
        
        with pytest.raises(ValueError, match="GEMINI_API_KEY no está configurada"):
            load_credentials()
    
    def test_verify_dependencies(self):
        """Prueba la verificación de dependencias"""
        # Esta prueba puede fallar si no están instaladas las dependencias
        # En un entorno de CI/CD se instalarían primero
        from framework.init import verify_dependencies
        
        # Solo verificamos que la función no lance excepciones
        result = verify_dependencies()
        assert isinstance(result, bool)


class TestGetTransaction:
    """Pruebas para el módulo get_transaction"""
    
    def test_run_success(self):
        """Prueba la ejecución exitosa de get_transaction"""
        from framework.get_transaction import run
        
        item = {
            'id': '1',
            'prompt': 'Test prompt',
            'context': 'Test context',
            'expected_output': 'Test output'
        }
        
        transaction = run(item)
        
        assert transaction['id'] == '1'
        assert transaction['prompt'] == 'Test prompt'
        assert transaction['context'] == 'Test context'
        assert transaction['expected_output'] == 'Test output'
        assert transaction['status'] == 'pending'
    
    def test_run_missing_id(self):
        """Prueba el manejo de ID faltante"""
        from framework.get_transaction import run
        
        item = {
            'prompt': 'Test prompt'
        }
        
        with pytest.raises(ValueError, match="Campo requerido 'id'"):
            run(item)
    
    def test_run_missing_prompt(self):
        """Prueba el manejo de prompt faltante"""
        from framework.get_transaction import run
        
        item = {
            'id': '1'
        }
        
        with pytest.raises(ValueError, match="Campo requerido 'prompt'"):
            run(item)
    
    def test_validate_prompt_valid(self):
        """Prueba la validación de prompt válido"""
        from framework.get_transaction import validate_prompt
        
        assert validate_prompt("Este es un prompt válido con suficiente contenido") is True
    
    def test_validate_prompt_invalid(self):
        """Prueba la validación de prompt inválido"""
        from framework.get_transaction import validate_prompt
        
        assert validate_prompt("Corto") is False
        assert validate_prompt("") is False
        assert validate_prompt(None) is False


if __name__ == '__main__':
    pytest.main([__file__])
