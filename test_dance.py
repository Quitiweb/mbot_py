#!/usr/bin/env python3
"""
Test del nuevo baile espectacular de mBot
"""

from mbot_controller import MBotController
import time

def test_new_dance():
    """Prueba el nuevo baile elaborado"""
    print("💃 PRUEBA DEL BAILE ESPECTACULAR MBOT")
    print("=" * 50)

    controller = MBotController()

    if not controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return

    print("🎵 ¡Prepárate para el espectáculo!")
    print("🎶 El mBot va a tocar 'Cumpleaños Feliz' versión robot")
    print("💃 Con coreografía completa y efectos de luces")
    print()

    input("⏸️  Presiona Enter cuando estés listo para el show...")

    # Ejecutar el baile
    print("🎭 ¡Empezando el espectáculo!")
    controller.perform_dance()

    print("\n🎉 ¡Espectáculo terminado!")
    print("¿Qué te pareció el nuevo baile?")

def test_individual_commands():
    """Prueba los comandos individuales relacionados con baile"""
    print("\n🎯 PRUEBA DE COMANDOS DE BAILE")
    print("=" * 40)

    controller = MBotController()
    if not controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return

    commands = [
        ("baile completo", lambda: controller.perform_dance()),
        ("giro simple", lambda: controller.perform_spin()),
        ("espectáculo de luces", lambda: controller.perform_light_show())
    ]

    for name, command_func in commands:
        print(f"\n🎪 Ejecutando: {name}")
        input("⏸️  Presiona Enter para continuar...")
        command_func()
        print(f"✅ {name} completado")

def test_with_ai_integration():
    """Prueba el baile integrado con IA"""
    print("\n🧠 PRUEBA CON INTEGRACIÓN IA")
    print("=" * 35)

    from ai_brain import AIBrain

    controller = MBotController()
    ai_brain = AIBrain()

    if not controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return

    # Comandos que deberían activar el baile
    dance_commands = [
        "baila",
        "baila para mí",
        "puedes bailar",
        "haz un baile"
    ]

    for cmd in dance_commands:
        print(f"\n👤 Comando: '{cmd}'")
        result = ai_brain.process_input(cmd)

        print(f"🧠 Tipo: {result['type']}")
        print(f"🤖 Respuesta: {result['response']}")

        if result['type'] == 'command' and result.get('command') == 'dance':
            print("⚡ Ejecutando baile...")
            controller.execute_command('dance')
            print("✅ Baile ejecutado")
        else:
            print("💬 Procesado como conversación")

        input("⏸️  Presiona Enter para probar siguiente comando...")

if __name__ == "__main__":
    print("🤖 SUITE DE PRUEBAS DEL BAILE MBOT")
    print("=" * 50)

    try:
        while True:
            print("\n¿Qué quieres probar?")
            print("1. 🎵 Baile espectacular completo")
            print("2. 🎯 Comandos individuales")
            print("3. 🧠 Integración con IA")
            print("4. 🎪 Todo")
            print("5. 🚪 Salir")

            choice = input("\nElige opción (1-5): ").strip()

            if choice == "1":
                test_new_dance()
            elif choice == "2":
                test_individual_commands()
            elif choice == "3":
                test_with_ai_integration()
            elif choice == "4":
                test_new_dance()
                test_individual_commands()
                test_with_ai_integration()
            elif choice == "5":
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")

    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas")
    except Exception as e:
        print(f"❌ Error: {e}")
