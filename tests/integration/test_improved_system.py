#!/usr/bin/env python3
"""
Test del Sistema mBot Mejorado - Mascota Robótica Inteligente
Prueba todos los comportamientos nuevos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import time
from src.core.mbot_behaviors import MBotBehaviors
from src.core.ai_brain import AIBrain
from src.core.mbot_controller import MBotController

def test_behavior_system():
    """Prueba el nuevo sistema de comportamientos"""
    print("🎭 PRUEBA DEL SISTEMA DE COMPORTAMIENTOS")
    print("=" * 50)

    behaviors = MBotBehaviors()

    # Pruebas de detección de comportamientos
    test_cases = [
        ("hola", "greeting"),
        ("puedes bailar", "dance"),
        ("te gusta la música", "dance"),
        ("echa patrás", None),  # Esto debe ser detectado como comando de movimiento
        ("cómo estás", "status"),
        ("jugamos", "play"),
        ("adiós", "goodbye")
    ]

    print("🔍 Probando detección de comportamientos:")
    for text, expected in test_cases:
        detected = behaviors.detect_behavior(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{text}' -> {detected} (esperado: {expected})")

    print("\n🎬 Probando respuestas aleatorias:")
    for behavior_name in ["greeting", "dance", "play"]:
        print(f"\n{behavior_name.upper()}:")
        for i in range(3):
            response = behaviors.get_behavior_response(behavior_name)
            print(f"  {i+1}. {response['response']}")

def test_ai_brain_improvements():
    """Prueba la IA mejorada"""
    print("\n🧠 PRUEBA DE IA MEJORADA")
    print("=" * 30)

    try:
        ai_brain = AIBrain()

        # Pruebas de comandos de movimiento inmediato
        movement_tests = [
            "echa patrás",
            "no te acerques tanto",
            "ven aquí",
            "para ahí mismo"
        ]

        print("⚡ Probando comandos de movimiento inmediato:")
        for text in movement_tests:
            result = ai_brain.process_input(text)
            print(f"'{text}' -> {result['type']}: {result['response']}")

        # Pruebas de comportamientos
        behavior_tests = [
            "hola qué tal",
            "puedes bailar para mí",
            "cómo te sientes hoy"
        ]

        print("\n🎭 Probando comportamientos:")
        for text in behavior_tests:
            result = ai_brain.process_input(text)
            response_type = result['type']
            if response_type == "behavior":
                print(f"'{text}' -> {result['behavior']}: {result['response']}")
            else:
                print(f"'{text}' -> {response_type}: {result['response']}")

    except Exception as e:
        print(f"❌ Error probando IA: {e}")
        print("(Probablemente Ollama no está ejecutándose)")

def test_mbot_behaviors_live():
    """Prueba comportamientos con mBot real"""
    print("\n🤖 PRUEBA CON MBOT REAL")
    print("=" * 30)

    try:
        # Conectar mBot
        mbot_controller = MBotController(connection_type="auto")
        print(f"✅ mBot conectado via {mbot_controller.mbot.connection_type}")

        # Prueba rápida de comportamientos físicos
        print("\n🎬 Probando comportamientos físicos:")

        # Saludo
        print("1. Saludo...")
        for _ in range(2):
            mbot_controller.mbot.doMove(50, -50)  # Giro derecha
            mbot_controller.mbot.doRGBLedOnBoard(0, 0, 255, 0)  # Verde
            time.sleep(0.3)
            mbot_controller.mbot.doMove(-50, 50)  # Giro izquierda
            mbot_controller.mbot.doRGBLedOnBoard(1, 0, 255, 0)
            time.sleep(0.3)
        mbot_controller.mbot.doMove(0, 0)
        mbot_controller.mbot.doBuzzer(523, 200)

        time.sleep(1)

        # Modo escucha
        print("2. Modo escucha...")
        mbot_controller.mbot.doRGBLedOnBoard(0, 0, 100, 255)  # Azul escucha
        mbot_controller.mbot.doRGBLedOnBoard(1, 0, 100, 255)
        time.sleep(2)

        # Pequeño movimiento de vida
        print("3. Movimiento de vida...")
        mbot_controller.mbot.doMove(20, -20)  # Leve balanceo
        time.sleep(0.3)
        mbot_controller.mbot.doMove(0, 0)

        time.sleep(1)

        # Retroceso educado
        print("4. Retroceso educado...")
        mbot_controller.mbot.doRGBLedOnBoard(0, 255, 255, 0)  # Amarillo precaución
        mbot_controller.mbot.doRGBLedOnBoard(1, 255, 255, 0)
        mbot_controller.mbot.doBuzzer(300, 200)  # Beep disculpa
        mbot_controller.mbot.doMove(-80, -80)
        time.sleep(1)
        mbot_controller.mbot.doMove(0, 0)

        # Limpieza final
        mbot_controller.mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot_controller.mbot.doRGBLedOnBoard(1, 0, 0, 0)

        print("✅ Pruebas físicas completadas")

        mbot_controller.cleanup()

    except Exception as e:
        print(f"❌ Error con mBot real: {e}")
        print("(¿Está el mBot conectado?)")

def test_response_length():
    """Verifica que las respuestas sean cortas"""
    print("\n📏 PRUEBA DE LONGITUD DE RESPUESTAS")
    print("=" * 40)

    behaviors = MBotBehaviors()

    # Verificar que todas las respuestas sean cortas
    max_words = 10
    long_responses = []

    for behavior_name, behavior_data in behaviors.behaviors.items():
        for response in behavior_data["responses"]:
            word_count = len(response.split())
            if word_count > max_words:
                long_responses.append((behavior_name, response, word_count))

    if long_responses:
        print("❌ Respuestas demasiado largas encontradas:")
        for behavior, response, count in long_responses:
            print(f"  {behavior}: '{response}' ({count} palabras)")
    else:
        print("✅ Todas las respuestas son apropiadamente cortas")

    # Verificar que no hay emoticonos
    emoji_responses = []
    emojis = ['👤', '🤖', '😊', '😄', '🎵', '🚀', '✨', '🎭', '🕺', '💃']

    for behavior_name, behavior_data in behaviors.behaviors.items():
        for response in behavior_data["responses"]:
            for emoji in emojis:
                if emoji in response:
                    emoji_responses.append((behavior_name, response))

    if emoji_responses:
        print("❌ Emoticonos encontrados:")
        for behavior, response in emoji_responses:
            print(f"  {behavior}: '{response}'")
    else:
        print("✅ No se encontraron emoticonos")

if __name__ == "__main__":
    print("🚀 TEST DEL SISTEMA MBOT MEJORADO")
    print("=" * 60)
    print("Probando el nuevo sistema de mascota robótica inteligente")
    print()

    input("🎭 Presiona Enter para probar el sistema de comportamientos...")
    test_behavior_system()

    input("\n🧠 Presiona Enter para probar la IA mejorada...")
    test_ai_brain_improvements()

    input("\n📏 Presiona Enter para probar longitud de respuestas...")
    test_response_length()

    response = input("\n🤖 ¿Probar con mBot real? (s/n): ")
    if response.lower() in ['s', 'sí', 'si', 'y', 'yes']:
        test_mbot_behaviors_live()

    print("\n🎉 TODAS LAS PRUEBAS COMPLETADAS")
    print("El mBot está listo para ser una mascota robótica inteligente!")
