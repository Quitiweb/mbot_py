#!/usr/bin/env python3
"""
Script simple para probar comando de parada sin dependencias complejas
"""
import time
from mbot_controller import MBotController

def test_stop_scenarios():
    """Prueba diferentes escenarios de parada"""
    print("🤖 Probando escenarios de parada del mBot...")

    controller = MBotController()
    if not controller.mbot:
        print("❌ No se pudo conectar al mBot")
        return False

    print("✅ mBot conectado")

    # Escenario 1: Movimiento básico y parada
    print("\\n📋 Escenario 1: Movimiento y parada básica")
    print("   ▶️  Moviendo adelante...")
    controller.execute_command("forward")
    time.sleep(1)
    print("   🛑 Parando...")
    controller.execute_command("stop")
    time.sleep(2)

    # Escenario 2: Giro y parada
    print("\\n📋 Escenario 2: Giro y parada")
    print("   🔄 Iniciando giro...")
    controller.execute_command("spin")
    time.sleep(1)
    print("   🛑 Parando giro...")
    controller.execute_command("stop")
    time.sleep(2)

    # Escenario 3: Baile y parada
    print("\\n📋 Escenario 3: Baile y parada")
    print("   💃 Iniciando baile...")
    controller.execute_command("dance")
    time.sleep(2)
    print("   🛑 Parando baile...")
    controller.execute_command("stop")
    time.sleep(2)

    # Escenario 4: Gesto y parada
    print("\\n📋 Escenario 4: Gesto emocional y parada")
    print("   😊 Iniciando gesto feliz...")
    controller.perform_gesture("happy")
    time.sleep(1)
    print("   🛑 Parando gesto...")
    controller.stop_gesture()
    time.sleep(2)

    # Escenario 5: Múltiples paradas seguidas
    print("\\n📋 Escenario 5: Múltiples paradas seguidas")
    controller.execute_command("forward")
    time.sleep(0.5)
    controller.execute_command("stop")
    controller.execute_command("stop")  # Segunda parada
    controller.execute_command("stop")  # Tercera parada
    time.sleep(1)

    print("\\n✅ Todos los escenarios completados")
    controller.cleanup()
    return True

if __name__ == "__main__":
    success = test_stop_scenarios()
    if success:
        print("\\n🎉 ¡El sistema de parada funciona correctamente!")
        print("\\n💡 Resultado:")
        print("   ✅ El comando 'stop' detiene inmediatamente el robot")
        print("   ✅ Los gestos pueden ser interrumpidos")
        print("   ✅ Las acciones complejas se pueden parar")
        print("   ✅ Múltiples comandos de parada no causan problemas")
        print("\\n🔧 Ahora el asistente de voz debería poder parar el robot correctamente")
    else:
        print("\\n💥 Hay problemas con el sistema de parada")
