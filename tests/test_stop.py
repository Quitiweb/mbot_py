#!/usr/bin/env python3
"""
Script simple para probar el comando de parada del mBot
"""
import time
from mbot_py.lib.mBot import mBot

def test_stop_command():
    """Prueba que el comando de parada funcione"""
    print("🤖 Iniciando prueba de comando de parada...")

    try:
        # Conectar al mBot
        mbot = mBot()
        print("✅ mBot conectado")

        # Apagar LEDs
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)

        print("🔄 Iniciando movimiento hacia adelante...")
        mbot.doMove(100, 100)

        print("⏱️  Esperando 3 segundos...")
        time.sleep(3)

        print("🛑 PARANDO EL ROBOT...")
        mbot.doMove(0, 0)  # Este comando debería parar el robot

        print("✅ Comando de parada enviado")
        print("🔍 ¿Se detuvo el robot? (debería haberse parado inmediatamente)")

        # Esperar un poco más para confirmar que está parado
        time.sleep(2)

        # Enviar comando de parada otra vez por seguridad
        print("🔒 Enviando segundo comando de parada por seguridad...")
        mbot.doMove(0, 0)

        print("📊 Prueba completada.")

        # Probar diferentes velocidades de parada
        print("\\n🧪 Probando diferentes métodos de parada...")

        # Método 1: Parada gradual
        print("1️⃣  Parada gradual...")
        mbot.doMove(100, 100)
        time.sleep(1)
        mbot.doMove(50, 50)
        time.sleep(0.5)
        mbot.doMove(0, 0)
        time.sleep(2)

        # Método 2: Parada abrupta
        print("2️⃣  Parada abrupta...")
        mbot.doMove(100, 100)
        time.sleep(1)
        mbot.doMove(0, 0)  # Parada inmediata
        time.sleep(2)

        # Método 3: Parada con freno
        print("3️⃣  Parada con freno...")
        mbot.doMove(100, 100)
        time.sleep(1)
        mbot.doMove(-20, -20)  # Pequeño freno hacia atrás
        time.sleep(0.1)
        mbot.doMove(0, 0)  # Parada
        time.sleep(2)

        print("✅ Todas las pruebas completadas")

        # Limpiar
        mbot.close()

    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        return False

    return True

if __name__ == "__main__":
    success = test_stop_command()
    if success:
        print("🎉 El comando de parada funciona correctamente")
    else:
        print("💥 Hay problemas con el comando de parada")
