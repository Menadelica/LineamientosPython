"""
Módulo de finalización y limpieza del framework
"""

import logging
import csv
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class ProcessEndHandler:
    """Manejador de finalización de procesos"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Inicializa el manejador de finalización
        
        Args:
            config: Configuración del framework
        """
        self.logger = logging.getLogger('gemini_automation.end')
        self.config = config
        self.results = []
        self.failed_items = []
        self.start_time = None
        self.end_time = None
    
    def set_start_time(self, start_time: datetime) -> None:
        """Establece el tiempo de inicio del proceso"""
        self.start_time = start_time
    
    def add_result(self, result: Dict[str, Any]) -> None:
        """
        Agrega un resultado exitoso
        
        Args:
            result: Resultado del procesamiento
        """
        self.results.append(result)
    
    def add_failed_item(self, item: Dict[str, Any]) -> None:
        """
        Agrega un elemento fallido
        
        Args:
            item: Elemento que falló
        """
        self.failed_items.append(item)
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Genera el reporte final de ejecución
        
        Returns:
            Diccionario con estadísticas del proceso
        """
        self.end_time = datetime.now()
        
        if self.start_time:
            duration = (self.end_time - self.start_time).total_seconds()
        else:
            duration = 0
        
        total_items = len(self.results) + len(self.failed_items)
        success_rate = (len(self.results) / total_items * 100) if total_items > 0 else 0
        
        report = {
            'execution_summary': {
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'end_time': self.end_time.isoformat(),
                'duration_seconds': duration,
                'total_items': total_items,
                'successful_items': len(self.results),
                'failed_items': len(self.failed_items),
                'success_rate_percent': round(success_rate, 2)
            },
            'details': {
                'successful_results': self.results,
                'failed_items': self.failed_items
            }
        }
        
        return report
    
    def save_results(self, results: List[Dict[str, Any]]) -> None:
        """
        Guarda los resultados exitosos en archivo CSV
        
        Args:
            results: Lista de resultados a guardar
        """
        if not results:
            self.logger.warning("No hay resultados para guardar")
            return
        
        output_path = self.config['paths']['output_data']
        
        # Crear directorio si no existe
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Preparar datos para CSV
        csv_data = []
        for result in results:
            if isinstance(result, dict) and 'generated_response' in result:
                csv_data.append({
                    'id': result.get('transaction_id', ''),
                    'original_prompt': result.get('original_prompt', ''),
                    'generated_response': result.get('generated_response', ''),
                    'status': result.get('status', ''),
                    'model_used': result.get('metadata', {}).get('model_used', ''),
                    'response_length': result.get('metadata', {}).get('response_length', 0),
                    'processed_at': datetime.now().isoformat()
                })
        
        if csv_data:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                fieldnames = csv_data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
            
            self.logger.info(f"Resultados guardados en: {output_path}")
    
    def save_report(self, report: Dict[str, Any]) -> None:
        """
        Guarda el reporte final en archivo JSON
        
        Args:
            report: Reporte a guardar
        """
        import json
        
        report_path = Path(self.config['paths']['logs']) / 'execution_report.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Reporte guardado en: {report_path}")
    
    def cleanup_resources(self) -> None:
        """
        Limpia recursos y conexiones
        """
        try:
            # Aquí se pueden cerrar conexiones de base de datos, APIs, etc.
            self.logger.info("Recursos limpiados correctamente")
        except Exception as e:
            self.logger.error(f"Error durante la limpieza de recursos: {e}")
    
    def log_summary(self, report: Dict[str, Any]) -> None:
        """
        Registra un resumen de la ejecución
        
        Args:
            report: Reporte de ejecución
        """
        summary = report['execution_summary']
        
        self.logger.info("=" * 50)
        self.logger.info("RESUMEN DE EJECUCIÓN")
        self.logger.info("=" * 50)
        self.logger.info(f"Tiempo de inicio: {summary['start_time']}")
        self.logger.info(f"Tiempo de fin: {summary['end_time']}")
        self.logger.info(f"Duración: {summary['duration_seconds']} segundos")
        self.logger.info(f"Total de elementos: {summary['total_items']}")
        self.logger.info(f"Exitosos: {summary['successful_items']}")
        self.logger.info(f"Fallidos: {summary['failed_items']}")
        self.logger.info(f"Tasa de éxito: {summary['success_rate_percent']}%")
        self.logger.info("=" * 50)


def run(results: List[Dict[str, Any]] = None, failed_items: List[Dict[str, Any]] = None, 
        start_time: datetime = None) -> None:
    """
    Función principal de finalización
    
    Args:
        results: Lista de resultados exitosos
        failed_items: Lista de elementos fallidos
        start_time: Tiempo de inicio del proceso
    """
    # Cargar configuración
    from .init import load_config
    config = load_config()
    
    # Crear manejador de finalización
    handler = ProcessEndHandler(config)
    
    # Configurar datos
    if start_time:
        handler.set_start_time(start_time)
    
    if results:
        handler.add_result(results)
    
    if failed_items:
        handler.add_failed_item(failed_items)
    
    # Generar y guardar reporte
    report = handler.generate_report()
    handler.save_report(report)
    
    # Guardar resultados
    if results:
        handler.save_results(results)
    
    # Limpiar recursos
    handler.cleanup_resources()
    
    # Registrar resumen
    handler.log_summary(report)
