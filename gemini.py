# Ejemplo de uso directo de Gemini API (versión original)
# Este archivo se mantiene como referencia, pero se recomienda usar main.py

# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate_example():
    """
    Función de ejemplo para generar contenido con Gemini
    Esta es la implementación original que se ha integrado en el framework
    """
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Crea un flujo de UiPath para automatizar el proceso de facturación"""),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""Eres un agente especializado en flujos de UiPath"""),
        ],
    )

    print("Generando respuesta con Gemini...")
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
    print("\n\n--- Fin de la respuesta ---")


def generate_custom_prompt(prompt_text: str):
    """
    Genera contenido con un prompt personalizado
    
    Args:
        prompt_text: Texto del prompt a enviar a Gemini
    """
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt_text),
            ],
        ),
    ]
    tools = [
        types.Tool(googleSearch=types.GoogleSearch(
        )),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config = types.ThinkingConfig(
            thinking_budget=-1,
        ),
        tools=tools,
        system_instruction=[
            types.Part.from_text(text="""Eres un agente especializado en flujos de UiPath y automatizaciones"""),
        ],
    )

    print(f"Generando respuesta para: {prompt_text[:50]}...")
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")
    print("\n\n--- Fin de la respuesta ---")


if __name__ == "__main__":
    print("🤖 Ejemplo de uso directo de Gemini API")
    print("Para usar el framework completo, ejecuta: python main.py")
    print("\n" + "="*50 + "\n")
    
    # Ejecutar ejemplo
    generate_example()
    
    print("\n" + "="*50)
    print("Para usar el framework REFramework completo:")
    print("1. Configura la variable de entorno GEMINI_API_KEY")
    print("2. Ejecuta: python main.py")
    print("3. Los resultados se guardarán en data/output/")
