#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración de la API de Gemini
"""

import os
from dotenv import load_dotenv

def debug_api_config():
    print("🔍 DIAGNÓSTICO DE CONFIGURACIÓN DE API GEMINI")
    print("=" * 50)
    
    # 1. Verificar archivo .env
    print("1. Verificando archivo .env...")
    if os.path.exists('.env'):
        print("✅ Archivo .env encontrado")
        with open('.env', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'GEMINI_API_KEY' in content:
                print("✅ GEMINI_API_KEY encontrada en .env")
            else:
                print("❌ GEMINI_API_KEY NO encontrada en .env")
    else:
        print("❌ Archivo .env NO encontrado")
    
    # 2. Cargar .env
    print("\n2. Cargando variables de entorno...")
    load_dotenv()
    
    # 3. Verificar variable de entorno
    print("\n3. Verificando variable de entorno...")
    api_key = os.environ.get('GEMINI_API_KEY')
    if api_key:
        print(f"✅ GEMINI_API_KEY cargada: {api_key[:10]}...{api_key[-4:]}")
        print(f"📏 Longitud de la clave: {len(api_key)} caracteres")
        
        # Verificar formato básico de Google API Key
        if api_key.startswith('AIza') and len(api_key) == 39:
            print("✅ Formato de clave parece correcto (Google API Key)")
        else:
            print("⚠️  Formato de clave no estándar para Google API Key")
    else:
        print("❌ GEMINI_API_KEY NO encontrada en variables de entorno")
    
    # 4. Test básico de conexión
    print("\n4. Probando conexión básica con Gemini...")
    try:
        from google import genai
        
        if api_key:
            client = genai.Client(api_key=api_key)
            print("✅ Cliente Gemini creado exitosamente")
            
            # Test mínimo
            try:
                # Intentar una operación muy simple para validar la clave
                contents = [
                    genai.types.Content(
                        role="user",
                        parts=[genai.types.Part.from_text("Hello")],
                    ),
                ]
                
                response_chunks = list(client.models.generate_content_stream(
                    model="gemini-2.0-flash-exp",
                    contents=contents,
                    config=genai.types.GenerateContentConfig()
                ))
                
                if response_chunks:
                    print("✅ API Key es VÁLIDA - Respuesta recibida")
                    print(f"📝 Primera respuesta: {response_chunks[0].text[:50]}...")
                else:
                    print("⚠️  API Key válida pero sin respuesta")
                    
            except Exception as e:
                error_str = str(e)
                if "API key not valid" in error_str:
                    print("❌ API Key NO VÁLIDA - Verifica tu clave")
                elif "PERMISSION_DENIED" in error_str:
                    print("❌ API Key válida pero sin permisos para este modelo")
                elif "MODEL_NOT_FOUND" in error_str:
                    print("⚠️  API Key válida pero modelo no encontrado, probando con otro...")
                    try:
                        # Probar con modelo diferente
                        response_chunks = list(client.models.generate_content_stream(
                            model="gemini-1.5-flash",
                            contents=contents,
                            config=genai.types.GenerateContentConfig()
                        ))
                        if response_chunks:
                            print("✅ API Key es VÁLIDA con gemini-1.5-flash")
                        else:
                            print("⚠️  Sin respuesta con gemini-1.5-flash")
                    except Exception as e2:
                        print(f"❌ Error con gemini-1.5-flash también: {e2}")
                else:
                    print(f"❌ Error inesperado: {e}")
        else:
            print("❌ No se puede probar sin API Key")
            
    except ImportError:
        print("❌ Módulo google.genai no disponible")
    except Exception as e:
        print(f"❌ Error al crear cliente: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 RECOMENDACIONES:")
    
    if not api_key:
        print("1. Configura GEMINI_API_KEY en el archivo .env")
        print("2. Obtén una clave en: https://makersuite.google.com/app/apikey")
    elif "demo_key" in api_key or "tu_clave" in api_key:
        print("1. Reemplaza la clave demo con tu clave API real")
        print("2. Obtén una clave en: https://makersuite.google.com/app/apikey")
    else:
        print("1. Verifica que tu clave API esté activa en Google AI Studio")
        print("2. Asegúrate de tener cuota disponible en tu cuenta")
        print("3. Verifica que el servicio Gemini esté habilitado")

if __name__ == "__main__":
    debug_api_config()
