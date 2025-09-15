"""
Módulo de finalización y limpieza del framework
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


def save_results(results: List[Dict[str, Any]], config: Dict[str, Any]) -> None:
    """Guarda los resultados exitosos en archivo CSV"""
    if not results:
        return
    
    output_path = config['paths']['output_data']
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
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
            writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
            writer.writeheader()
            writer.writerows(csv_data)


def save_report(results: List[Dict[str, Any]], failed_items: List[Dict[str, Any]], 
                start_time: datetime, config: Dict[str, Any]) -> None:
    """Guarda el reporte final en archivo JSON"""
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() if start_time else 0
    total = len(results) + len(failed_items)
    success_rate = (len(results) / total * 100) if total > 0 else 0
    
    report = {
        'execution_summary': {
            'start_time': start_time.isoformat() if start_time else None,
            'end_time': end_time.isoformat(),
            'duration_seconds': duration,
            'total_items': total,
            'successful_items': len(results),
            'failed_items': len(failed_items),
            'success_rate_percent': round(success_rate, 2)
        }
    }
    
    report_path = Path(config['paths']['logs']) / 'execution_report.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)


def run(results: List[Dict[str, Any]] = None, failed_items: List[Dict[str, Any]] = None, 
        start_time: datetime = None) -> None:
    """
    Función principal de finalización
    
    Args:
        results: Lista de resultados exitosos
        failed_items: Lista de elementos fallidos
        start_time: Tiempo de inicio del proceso
    """
    from .init import load_config
    config = load_config()
    
    results = results or []
    failed_items = failed_items or []
    
    if results:
        save_results(results, config)
    
    save_report(results, failed_items, start_time, config)
