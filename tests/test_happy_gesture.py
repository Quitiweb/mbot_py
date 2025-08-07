#!/usr/bin/env python3
"""
Test simple del sistema sin audio para probar el gesto 'happy'
"""

from mbot_controller import MBotController
from gesture_engine_fixed import GestureEngineFixed
from config import *
import time

def test_happy_gesture_only():
    """Prueba solo el gesto happy que causaba bucles"""
    print("🤖 TEST DEL GESTO HAPPY SIN AUDIO")
    print("=" * 50)

    try:
        # Crear controlador
        print("🔗 Conectando mBot...")
        mbot_controller = MBotController(connection_type="auto")

        if not mbot_controller.mbot:
            print("❌ No se pudo conectar al mBot")
            return

        print(f"✅ mBot conectado via {mbot_controller.mbot.connection_type}")

        # Crear gesture engine arreglado
        print("🎭 Creando gesture engine...")
        gesture_engine = GestureEngineFixed(mbot_controller)

        print("✅ Sistema listo")
        print()
        print("🎯 PROBANDO EL GESTO 'HAPPY' QUE CAUSABA EL BUCLE...")
        print("   Observa si el robot:")
        print("   - Cambia LEDs a verde")
        print("   - Se mueve un poco")
        print("   - Y luego SE DETIENE COMPLETAMENTE")
        print()
        input("Presiona Enter para ejecutar el gesto...")

        # Ejecutar el gesto problemático
        print("🎭 Ejecutando gesto 'happy' por 3 segundos...")
        gesture_engine.set_emotion("happy", 3)

        # Esperar y observar
        print("⏳ Esperando 5 segundos para verificar que se detiene...")
        time.sleep(5)

        print("🔍 Verificando estado final...")

        # Asegurar que todo está parado
        if mbot_controller.mbot:
            mbot_controller.mbot.doMove(0, 0)
            mbot_controller.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            mbot_controller.mbot.doRGBLedOnBoard(1, 0, 0, 0)

        print("✅ TEST COMPLETADO")
        print("¿Se quedó el robot en bucle infinito? (debería estar parado)")

        # Limpiar
        gesture_engine.stop_all()
        if hasattr(mbot_controller, 'cleanup'):
            mbot_controller.cleanup()

        mbot_controller.mbot.close()

    except KeyboardInterrupt:
        print("\\n🛑 Interrumpido por usuario")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_happy_gesture_only()
