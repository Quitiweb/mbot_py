#!/usr/bin/env python3
"""
Prueba específica del comando 'para' en el asistente
"""
import time
import sys
import os

# Añadir el directorio actual al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_brain import AIBrain
from mbot_controller import MBotController

def test_para_command():
    """Prueba específica del reconocimiento y ejecución del comando 'para'"""
    print("🤖 Iniciando prueba del comando 'para'...")
    print("=" * 50)

    # Inicializar componentes
    ai_brain = AIBrain()
    mbot_controller = MBotController()

    if not mbot_controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return False

    print("✅ Componentes inicializados correctamente")

    # Lista de variaciones del comando "para"
    test_commands = [
        "para",
        "Para",
        "PARA",
        "para ya",
        "para el robot",
        "detente",
        "Detente",
        "para por favor",
        "que se pare",
        "robot para"
    ]

    print("\n🧪 Probando reconocimiento de comandos...")

    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. Probando: '{command}'")

        # Procesar comando con AI Brain
        result = ai_brain.process_input(command)

        print(f"   Tipo: {result.get('type', 'desconocido')}")
        print(f"   Respuesta: {result.get('response', 'sin respuesta')}")

        if result.get('type') == 'command':
            actual_command = result.get('command')
            print(f"   Comando detectado: {actual_command}")

            if actual_command == 'stop':
                print("   ✅ ¡Comando 'para' reconocido correctamente!")

                # Hacer que el robot se mueva primero
                print("   🔄 Iniciando movimiento...")
                mbot_controller.mbot.doMove(100, 100)
                time.sleep(1)

                # Ejecutar comando de parada
                print("   🛑 Ejecutando comando de parada...")
                mbot_controller.execute_command(actual_command)

                # Verificar que se detuvo
                time.sleep(1)
                print("   ✅ Comando ejecutado")
            else:
                print(f"   ❌ Comando incorrecto detectado: {actual_command}")
        else:
            print("   ❌ No se detectó como comando directo")

    # Prueba final: comando en contexto de conversación
    print("\n🗣️  Probando comando en contexto conversacional...")
    conversation_tests = [
        "Hola robot, para",
        "Por favor robot para ya",
        "Necesito que pares",
        "Robot detente inmediatamente"
    ]

    for command in conversation_tests:
        print(f"\nProbando: '{command}'")
        result = ai_brain.process_input(command)
        print(f"Tipo: {result.get('type')}")

        if result.get('type') == 'command' and result.get('command') == 'stop':
            print("✅ Comando 'para' detectado en conversación")
        else:
            print("❌ Comando 'para' NO detectado en conversación")

    # Limpieza
    mbot_controller.cleanup()
    print("\n🎉 Prueba completada")
    return True

if __name__ == "__main__":
    success = test_para_command()
    if success:
        print("\n✅ El comando 'para' funciona correctamente")
    else:
        print("\n❌ Hay problemas con el comando 'para'")
