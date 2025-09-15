#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración de la API de Gemini
"""

import os
from dotenv import load_dotenv

def debug_api_config():
    print("🔍 DIAGNÓSTICO DE CONFIGURACIóN DE API GEMINI")
    print("=" * 50)
    
    # Verificar archivo .env
    env_exists = os.path.exists('.env')
    print(f"Archivo .env: {'✅ Encontrado' if env_exists else '❌ No encontrado'}")
    
    if env_exists:
        with open('.env', 'r', encoding='utf-8') as f:
            has_key = 'GEMINI_API_KEY' in f.read()
            print(f"GEMINI_API_KEY en .env: {'✅ Sí' if has_key else '❌ No'}")
    
    # Cargar .env y verificar variable de entorno
    load_dotenv()
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ GEMINI_API_KEY NO encontrada en variables de entorno")
        return
    
    print(f"✅ GEMINI_API_KEY cargada: {api_key[:10]}...{api_key[-4:]}")
    print(f"📏 Longitud: {len(api_key)} caracteres")
    
    if api_key.startswith('AIza') and len(api_key) == 39:
        print("✅ Formato correcto (Google API Key)")
    else:
        print("⚠️ Formato no estándar para Google API Key")

    # Test básico de conexión
    print("\n🔗 Probando conexión con Gemini...")
    try:
        from google import genai
        client = genai.Client(api_key=api_key)
        
        # Test con modelo simple
        contents = [genai.types.Content(
            role="user",
            parts=[genai.types.Part.from_text("Hello")]
        )]
        
        models_to_try = ["gemini-2.0-flash-exp", "gemini-1.5-flash"]
        
        for model in models_to_try:
            try:
                response = list(client.models.generate_content_stream(
                    model=model,
                    contents=contents,
                    config=genai.types.GenerateContentConfig()
                ))
                if response:
                    print(f"✅ API Key VÁLIDA con {model}")
                    print(f"📝 Respuesta: {response[0].text[:50]}...")
                    break
            except Exception:
                continue
        else:
            print("❌ No se pudo conectar con ningún modelo")
            
    except ImportError:
        print("❌ Módulo google.genai no disponible")
    except Exception as e:
        if "API key not valid" in str(e):
            print("❌ API Key NO VÁLIDA")
        elif "PERMISSION_DENIED" in str(e):
            print("❌ Sin permisos para usar la API")
        else:
            print(f"❌ Error: {e}")

    print("\n🎯 RECOMENDACIONES:")
    if not api_key or "demo_key" in api_key or "tu_clave" in api_key:
        print("1. Obtén una clave en: https://makersuite.google.com/app/apikey")
        print("2. Configura GEMINI_API_KEY en el archivo .env")
    else:
        print("1. Verifica que tu clave API esté activa")
        print("2. Asegúrate de tener cuota disponible")

if __name__ == "__main__":
    debug_api_config()
