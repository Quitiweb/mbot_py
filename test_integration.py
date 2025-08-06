#!/usr/bin/env python3
"""
Test de integración IA + mBot
Prueba que los comandos de la IA realmente muevan el robot
"""

from ai_brain import AIBrain
from mbot_controller import MBotController
import time

def test_ai_mbot_integration():
    """Prueba la integración completa IA -> Comandos -> mBot"""
    print("🧪 PRUEBA DE INTEGRACIÓN IA + MBOT")
    print("=" * 40)

    # Inicializar componentes
    print("🧠 Inicializando IA...")
    ai_brain = AIBrain()

    print("🤖 Inicializando mBot...")
    mbot_controller = MBotController()

    if not mbot_controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return

    print("✅ Componentes inicializados")

    # Lista de comandos para probar
    test_commands = [
        "muévete hacia adelante",
        "gira a la derecha",
        "baila para mí",
        "para ahora",
        "luz",
        "atrás"
    ]

    for i, command in enumerate(test_commands, 1):
        print(f"\n--- Prueba {i}/{len(test_commands)} ---")
        print(f"👤 Comando: \"{command}\"")

        # 1. Procesar con IA
        result = ai_brain.process_input(command)
        print(f"🧠 Tipo: {result['type']}")
        print(f"🧠 Respuesta: {result['response']}")

        if result['type'] == 'command':
            print(f"⚡ Comando detectado: {result['command']}")

            # 2. Ejecutar comando en mBot
            print("🤖 Ejecutando en mBot...")
            mbot_controller.execute_command(result['command'])

            print("✅ Comando ejecutado")
        else:
            print("💬 Procesado como conversación (sin movimiento)")

        # Pausa entre pruebas
        input("⏸️  Presiona Enter para continuar...")

    print("\n🎉 Prueba de integración completada")

def test_gesture_integration():
    """Prueba específica de gestos emocionales"""
    print("\n🎭 PRUEBA DE GESTOS EMOCIONALES")
    print("=" * 40)

    mbot_controller = MBotController()
    if not mbot_controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return

    # Probar cada gesto directamente
    gestures_to_test = ["happy", "excited", "thinking", "confused", "sad", "neutral"]

    for gesture in gestures_to_test:
        print(f"\n🎭 Probando gesto: {gesture}")
        mbot_controller.perform_gesture(gesture)
        input("⏸️  ¿Viste el gesto? Presiona Enter para continuar...")

    print("✅ Prueba de gestos completada")

def test_conversation_with_movement():
    """Prueba conversación real con movimientos"""
    print("\n💬 PRUEBA DE CONVERSACIÓN CON MOVIMIENTOS")
    print("=" * 40)

    ai_brain = AIBrain()
    mbot_controller = MBotController()

    if not mbot_controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return

    conversation_tests = [
        "Hola robot, ¿cómo estás?",  # Conversación
        "adelante",                  # Comando directo
        "¿puedes bailar?",          # Conversación que menciona baile
        "baila",                    # Comando directo de baile
        "para",                     # Comando de parada
        "¿qué tal si giras?",       # Conversación que menciona giro
        "gira",                     # Comando directo
    ]

    for i, user_input in enumerate(conversation_tests, 1):
        print(f"\n--- Conversación {i}/{len(conversation_tests)} ---")
        print(f"👤 Usuario: \"{user_input}\"")

        result = ai_brain.process_input(user_input)

        print(f"🤖 Respuesta: {result['response']}")
        print(f"😊 Emoción: {result['emotion']}")
        print(f"🎯 Tipo: {result['type']}")

        if result['type'] == 'command':
            print(f"⚡ Ejecutando comando: {result['command']}")
            mbot_controller.execute_command(result['command'])
        else:
            print(f"🎭 Ejecutando gesto emocional: {result['emotion']}")
            mbot_controller.perform_gesture(result['emotion'])

        print("⏳ Observa el robot...")
        time.sleep(3)
        input("⏸️  ¿Se movió correctamente? Presiona Enter para continuar...")

    print("🎉 Prueba de conversación completada")

def main():
    """Función principal"""
    print("🤖 SUITE DE PRUEBAS DE INTEGRACIÓN")
    print("=" * 50)

    while True:
        print("\n¿Qué prueba quieres ejecutar?")
        print("1. Integración IA + mBot (comandos)")
        print("2. Gestos emocionales")
        print("3. Conversación con movimientos")
        print("4. Todas las pruebas")
        print("5. Salir")

        choice = input("\nElige una opción (1-5): ").strip()

        if choice == "1":
            test_ai_mbot_integration()
        elif choice == "2":
            test_gesture_integration()
        elif choice == "3":
            test_conversation_with_movement()
        elif choice == "4":
            test_ai_mbot_integration()
            test_gesture_integration()
            test_conversation_with_movement()
        elif choice == "5":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas")
    except Exception as e:
        print(f"❌ Error: {e}")
