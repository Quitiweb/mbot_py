#!/usr/bin/env python3
"""
Test para diagnosticar el problema del bucle infinito
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import time
import threading
from legacy.mbot_final import MBotFinal

def test_individual_components():
    """Prueba cada componente del gesto 'happy' individualmente"""
    print("🔧 DIAGNÓSTICO DEL PROBLEMA DEL BUCLE INFINITO")
    print("=" * 50)

    try:
        # Conectar mBot
        mbot = MBotFinal(connection_type="auto")
        print(f"✅ Conectado por: {mbot.connection_type}")

        print("\n1️⃣ PROBANDO SOLO LEDs RAINBOW...")
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Rojo, Verde, Azul
        for i, color in enumerate(colors):
            print(f"   Color {i+1}: RGB{color}")
            mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
            mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
            time.sleep(1)

        # Apagar LEDs
        print("   Apagando LEDs...")
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)
        time.sleep(1)

        print("\n2️⃣ PROBANDO SOLO MOVIMIENTO BOUNCE...")
        print("   Adelante...")
        mbot.doMove(100, 100)
        time.sleep(0.3)

        print("   Atrás...")
        mbot.doMove(-80, -80)  # Valores negativos
        time.sleep(0.2)

        print("   Parar...")
        mbot.doMove(0, 0)
        time.sleep(1)

        print("\n3️⃣ PROBANDO SOLO BUZZER...")
        print("   Beep corto...")
        mbot.doBuzzer(440, 300)  # 440Hz por 300ms
        time.sleep(1)

        print("\n4️⃣ PROBANDO COMBINACIÓN SECUENCIAL (SIN HILOS)...")
        print("   LED Verde...")
        mbot.doRGBLedOnBoard(0, 0, 255, 0)
        time.sleep(0.5)

        print("   Movimiento...")
        mbot.doMove(80, 80)
        time.sleep(0.3)
        mbot.doMove(0, 0)

        print("   Buzzer...")
        mbot.doBuzzer(523, 200)  # Do agudo, corto
        time.sleep(0.5)

        print("   Apagar...")
        mbot.doRGBLedOnBoard(0, 0, 0, 0)

        print("\n✅ DIAGNÓSTICO COMPLETADO - ¿Hubo algún problema?")

        mbot.close()

    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")

def test_problematic_sequence():
    """Reproduce exactamente la secuencia problemática"""
    print("\n🚨 REPRODUCIENDO SECUENCIA PROBLEMÁTICA...")
    print("=" * 50)

    try:
        mbot = MBotFinal(connection_type="auto")

        # Simular exactamente lo que hace el gesto "happy"
        print("🎭 Ejecutando gesto 'happy' completo...")

        # Crear hilos como lo hace el sistema real
        def led_thread():
            print("   🔴 Hilo LEDs iniciado...")
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
            for color in colors:
                mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
                mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
                time.sleep(0.5)
            print("   🔴 Hilo LEDs terminado")

        def movement_thread():
            print("   🚗 Hilo movimiento iniciado...")
            mbot.doMove(100, 100)
            time.sleep(0.3)
            mbot.doMove(-80, -80)
            time.sleep(0.2)
            mbot.doMove(0, 0)
            print("   🚗 Hilo movimiento terminado")

        def sound_thread():
            print("   🔊 Hilo sonido iniciado...")
            # Beep happy - múltiples tonos
            tones = [262, 330, 392, 523]  # Do, Mi, Sol, Do
            for tone in tones:
                mbot.doBuzzer(tone, 200)
                time.sleep(0.3)
            print("   🔊 Hilo sonido terminado")

        # Lanzar todos los hilos simultáneamente (como hace el sistema)
        threads = []
        threads.append(threading.Thread(target=led_thread))
        threads.append(threading.Thread(target=movement_thread))
        threads.append(threading.Thread(target=sound_thread))

        print("🚀 Lanzando hilos simultáneos...")
        for t in threads:
            t.start()

        print("⏳ Esperando que terminen...")
        for t in threads:
            t.join()

        print("✅ Secuencia terminada - Robot debe estar parado")

        # Verificar estado final
        print("🔍 Verificando estado final...")
        mbot.doMove(0, 0)  # Asegurar parada
        mbot.doRGBLedOnBoard(0, 0, 0, 0)  # Apagar LEDs
        mbot.doRGBLedOnBoard(1, 0, 0, 0)

        print("✅ Estado limpiado")

        mbot.close()

    except Exception as e:
        print(f"❌ Error en secuencia problemática: {e}")

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DEL PROBLEMA DE BUCLE INFINITO")
    print("=" * 60)
    print("Este script probará cada componente individualmente")
    print("para identificar qué causa el bucle infinito.")
    print()
    input("Presiona Enter para empezar...")

    test_individual_components()

    print("\n" + "="*60)
    input("¿Viste algún problema arriba? Presiona Enter para probar la secuencia completa...")

    test_problematic_sequence()

    print("\n🏁 DIAGNÓSTICO COMPLETADO")
    print("Si el robot se quedó en bucle, el problema está en la coordinación de hilos")
