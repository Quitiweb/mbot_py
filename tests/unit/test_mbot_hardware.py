#!/usr/bin/env python3
"""
Diagnóstico del mBot - Prueba directa de conexión y movimientos
"""

import sys
import time
import threading
from mbot_py.lib.mBot import mBot

def test_basic_connection():
    """Prueba la conexión básica con el mBot"""
    print("🔧 Probando conexión básica con mBot...")

    try:
        # Intentar conectar
        mbot = mBot()
        print("✅ mBot conectado correctamente")

        # Probar pitido de confirmación
        print("🎵 Enviando pitido de prueba...")
        mbot.doBuzzer(880, 500)  # La 880Hz por 500ms
        time.sleep(1)

        return mbot

    except Exception as e:
        print(f"❌ Error conectando mBot: {e}")
        print("💡 Asegúrate de que:")
        print("   - El mBot está conectado por USB")
        print("   - No hay otros programas usando el puerto")
        print("   - El driver CH340 está instalado")
        return None

def test_movements(mbot):
    """Prueba los movimientos básicos"""
    print("\n🚗 Probando movimientos básicos...")

    movements = [
        ("adelante", 100, 100, 1),
        ("atrás", -100, -100, 1),
        ("derecha", 80, -80, 0.5),
        ("izquierda", -80, 80, 0.5),
    ]

    for direction, left_speed, right_speed, duration in movements:
        try:
            print(f"   Moviendo {direction}...")
            mbot.doMove(left_speed, right_speed)
            time.sleep(duration)
            mbot.doMove(0, 0)  # Parar
            time.sleep(0.5)    # Pausa entre movimientos
            print(f"   ✅ {direction} completado")

        except Exception as e:
            print(f"   ❌ Error en {direction}: {e}")

    print("🛑 Deteniendo robot...")
    mbot.doMove(0, 0)

def test_leds(mbot):
    """Prueba los LEDs"""
    print("\n💡 Probando LEDs...")

    colors = [
        ("rojo", 255, 0, 0),
        ("verde", 0, 255, 0),
        ("azul", 0, 0, 255),
        ("amarillo", 255, 255, 0),
        ("morado", 255, 0, 255),
        ("cian", 0, 255, 255),
        ("blanco", 255, 255, 255)
    ]

    for color_name, r, g, b in colors:
        try:
            print(f"   LED {color_name}...")
            # Encender ambos LEDs del mismo color
            mbot.doRGBLedOnBoard(0, r, g, b)  # LED 1
            mbot.doRGBLedOnBoard(1, r, g, b)  # LED 2
            time.sleep(0.8)

        except Exception as e:
            print(f"   ❌ Error con LED {color_name}: {e}")

    # Apagar LEDs
    try:
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)
        print("   ✅ LEDs apagados")
    except Exception as e:
        print(f"   ❌ Error apagando LEDs: {e}")

def test_buzzer(mbot):
    """Prueba el buzzer con diferentes tonos"""
    print("\n🎵 Probando buzzer...")

    notes = [
        ("Do", 523, 300),
        ("Re", 587, 300),
        ("Mi", 659, 300),
        ("Fa", 698, 300),
        ("Sol", 784, 300),
        ("La", 880, 300),
        ("Si", 988, 300),
        ("Do alto", 1047, 500)
    ]

    for note_name, frequency, duration in notes:
        try:
            print(f"   Tocando {note_name} ({frequency}Hz)...")
            mbot.doBuzzer(frequency, duration)
            time.sleep(duration / 1000 + 0.1)  # Convertir ms a segundos + pausa

        except Exception as e:
            print(f"   ❌ Error con nota {note_name}: {e}")

def test_gesture_simulation(mbot):
    """Simula un gesto complejo (movimiento + LEDs + sonido)"""
    print("\n🎭 Probando gesto complejo (baile)...")

    try:
        # Baile simple: giros con LEDs y música
        dance_sequence = [
            # (movimiento_izq, movimiento_der, led_r, led_g, led_b, buzzer_freq, duracion)
            (80, -80, 255, 0, 0, 523, 0.5),    # Girar derecha + rojo + Do
            (-80, 80, 0, 255, 0, 659, 0.5),   # Girar izquierda + verde + Mi
            (80, -80, 0, 0, 255, 784, 0.5),   # Girar derecha + azul + Sol
            (-80, 80, 255, 255, 0, 1047, 0.5) # Girar izquierda + amarillo + Do alto
        ]

        for left, right, r, g, b, freq, duration in dance_sequence:
            # Movimiento
            mbot.doMove(left, right)

            # LEDs
            mbot.doRGBLedOnBoard(0, r, g, b)
            mbot.doRGBLedOnBoard(1, r, g, b)

            # Sonido
            mbot.doBuzzer(freq, int(duration * 1000))

            time.sleep(duration)

        # Parar todo
        mbot.doMove(0, 0)
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)

        print("✅ Gesto complejo completado")

    except Exception as e:
        print(f"❌ Error en gesto complejo: {e}")

def test_threading_interference():
    """Prueba si hay problemas con múltiples hilos"""
    print("\n🧵 Probando interferencia entre hilos...")

    try:
        mbot = mBot()

        def move_robot():
            """Hilo de movimiento"""
            for i in range(3):
                print(f"   Hilo movimiento: giro {i+1}")
                mbot.doMove(60, -60)
                time.sleep(0.3)
                mbot.doMove(0, 0)
                time.sleep(0.2)

        def flash_leds():
            """Hilo de LEDs"""
            for i in range(6):
                color = 255 if i % 2 == 0 else 0
                print(f"   Hilo LEDs: flash {i+1}")
                mbot.doRGBLedOnBoard(0, color, 0, 0)
                mbot.doRGBLedOnBoard(1, color, 0, 0)
                time.sleep(0.25)

        def play_sounds():
            """Hilo de sonidos"""
            for i in range(4):
                freq = 440 + (i * 100)
                print(f"   Hilo sonido: tono {i+1}")
                mbot.doBuzzer(freq, 200)
                time.sleep(0.4)

        # Ejecutar hilos en paralelo
        thread1 = threading.Thread(target=move_robot)
        thread2 = threading.Thread(target=flash_leds)
        thread3 = threading.Thread(target=play_sounds)

        thread1.start()
        thread2.start()
        thread3.start()

        thread1.join()
        thread2.join()
        thread3.join()

        # Limpiar
        mbot.doMove(0, 0)
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)

        print("✅ Prueba de hilos completada")

    except Exception as e:
        print(f"❌ Error en prueba de hilos: {e}")

def main():
    """Función principal de diagnóstico"""
    print("🤖 DIAGNÓSTICO COMPLETO DEL MBOT")
    print("=" * 40)

    # 1. Probar conexión básica
    mbot = test_basic_connection()
    if not mbot:
        print("\n❌ No se pudo conectar al mBot. Abortando diagnóstico.")
        return

    input("\n⏸️  Presiona Enter para continuar con los movimientos...")

    # 2. Probar movimientos
    test_movements(mbot)

    input("\n⏸️  Presiona Enter para continuar con los LEDs...")

    # 3. Probar LEDs
    test_leds(mbot)

    input("\n⏸️  Presiona Enter para continuar con el buzzer...")

    # 4. Probar buzzer
    test_buzzer(mbot)

    input("\n⏸️  Presiona Enter para probar un gesto complejo...")

    # 5. Probar gesto complejo
    test_gesture_simulation(mbot)

    input("\n⏸️  Presiona Enter para probar hilos múltiples...")

    # 6. Probar hilos
    test_threading_interference()

    print("\n🎉 DIAGNÓSTICO COMPLETADO")
    print("Si todos los tests pasaron, el mBot funciona correctamente.")
    print("Si alguno falló, revisa las conexiones y drivers.")

    # Asegurar que todo esté parado
    try:
        mbot.doMove(0, 0)
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Diagnóstico interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error crítico en diagnóstico: {e}")

    print("🔚 Fin del diagnóstico")
