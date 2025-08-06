#!/usr/bin/env python3
"""
Test del nuevo AI Brain con Ollama
"""

from ai_brain import AIBrain

def test_ollama_ai():
    """Prueba el nuevo AI Brain con Ollama"""
    print("🧠 Iniciando test de AI Brain con Ollama...")

    # Crear instancia del AI Brain
    brain = AIBrain()

    # Pruebas de conversación
    test_messages = [
        "Hola robot, ¿cómo estás?",
        "¿Cuál es tu nombre?",
        "¿Qué puedes hacer?",
        "Cuéntame un chiste",
        "para ahora mismo"  # Comando directo
    ]

    for message in test_messages:
        print(f"\n👤 Usuario: {message}")

        result = brain.process_input(message)

        print(f"🤖 Tipo: {result.get('type', 'N/A')}")
        print(f"🤖 Respuesta: {result.get('response', 'N/A')}")
        print(f"😊 Emoción: {result.get('emotion', 'N/A')}")

        if result.get('type') == 'command':
            print(f"⚡ Comando: {result.get('command', 'N/A')}")

        print("-" * 50)

    print("✅ Test completado!")

if __name__ == "__main__":
    test_ollama_ai()
