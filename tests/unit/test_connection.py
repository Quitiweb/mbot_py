#!/usr/bin/env python3
"""
Test de conectividad mBot - USB y Bluetooth
"""

import sys
import time
from mbot_enhanced import MBotEnhanced

def test_connection_type(connection_type, bluetooth_address=None):
    """Prueba un tipo de conexión específico"""
    print(f"\n{'='*60}")
    print(f"🔌 PROBANDO CONEXIÓN: {connection_type.upper()}")
    print(f"{'='*60}")

    try:
        print(f"🔗 Intentando conectar por {connection_type}...")
        robot = MBotEnhanced(connection_type, bluetooth_address)

        print(f"✅ ¡Conexión exitosa!")
        print(f"📊 Detalles: {robot.get_connection_info()}")

        # Probar funcionalidades básicas
        print("🧪 Probando funcionalidades básicas...")

        # Test 1: Buzzer
        print("   🎵 Probando buzzer...")
        robot.doBuzzer(440, 300)
        time.sleep(0.5)

        # Test 2: LEDs
        print("   💡 Probando LEDs...")
        robot.doRGBLedOnBoard(0, 255, 0, 0)  # LED 1 rojo
        robot.doRGBLedOnBoard(1, 0, 255, 0)  # LED 2 verde
        time.sleep(1)
        robot.doRGBLedOnBoard(0, 0, 0, 0)    # Apagar
        robot.doRGBLedOnBoard(1, 0, 0, 0)    # Apagar

        # Test 3: Movimiento básico
        print("   🚗 Probando movimiento...")
        robot.doMove(50, 50)   # Adelante lento
        time.sleep(0.5)
        robot.doMove(0, 0)     # Parar

        print(f"🎉 ¡Todas las pruebas pasaron para {connection_type}!")

        robot.close()
        return True

    except Exception as e:
        print(f"❌ Error con {connection_type}: {e}")
        return False

def test_auto_connection():
    """Prueba la conexión automática"""
    print(f"\n{'='*60}")
    print("🔄 PROBANDO CONEXIÓN AUTOMÁTICA")
    print("📝 (Bluetooth primero, luego USB)")
    print(f"{'='*60}")

    try:
        robot = MBotEnhanced("auto")
        print(f"✅ Conexión automática exitosa!")
        print(f"📊 Conectado via: {robot.get_connection_info()}")

        # Prueba rápida
        robot.doBuzzer(523, 200)  # Do
        time.sleep(0.3)
        robot.doBuzzer(659, 200)  # Mi

        robot.close()
        return True

    except Exception as e:
        print(f"❌ Error en conexión automática: {e}")
        return False

def interactive_bluetooth_test():
    """Permite al usuario especificar una dirección Bluetooth manualmente"""
    print(f"\n{'='*60}")
    print("🔵 PRUEBA BLUETOOTH INTERACTIVA")
    print(f"{'='*60}")

    print("Si conoces la dirección MAC de tu mBot, puedes ingresarla:")
    print("Ejemplo: 00:11:22:33:44:55")
    print("O presiona Enter para buscar automáticamente")

    bluetooth_address = input("Dirección MAC (opcional): ").strip()
    if not bluetooth_address:
        bluetooth_address = None

    return test_connection_type("bluetooth", bluetooth_address)

def main():
    """Función principal del test de conectividad"""
    print("🤖 TEST DE CONECTIVIDAD MBOT ENHANCED")
    print("🔗 Probando conexiones USB y Bluetooth")
    print("=" * 70)

    results = {}

    while True:
        print("\n¿Qué tipo de conexión quieres probar?")
        print("1. 🔄 Conexión automática (Bluetooth → USB)")
        print("2. 🔵 Solo Bluetooth")
        print("3. 🔌 Solo USB")
        print("4. 🔵 Bluetooth con dirección específica")
        print("5. 🧪 Probar todos los tipos")
        print("6. 📊 Ver resultados")
        print("7. 🚪 Salir")

        choice = input("\nElige opción (1-7): ").strip()

        if choice == "1":
            results["auto"] = test_auto_connection()

        elif choice == "2":
            results["bluetooth"] = test_connection_type("bluetooth")

        elif choice == "3":
            results["usb"] = test_connection_type("usb")

        elif choice == "4":
            results["bluetooth_manual"] = interactive_bluetooth_test()

        elif choice == "5":
            print("\n🧪 EJECUTANDO TODAS LAS PRUEBAS...")
            results["usb"] = test_connection_type("usb")
            results["bluetooth"] = test_connection_type("bluetooth")
            results["auto"] = test_auto_connection()

        elif choice == "6":
            print(f"\n{'='*60}")
            print("📊 RESUMEN DE RESULTADOS")
            print(f"{'='*60}")

            if not results:
                print("❌ No se han ejecutado pruebas aún")
            else:
                for test_type, success in results.items():
                    status = "✅ ÉXITO" if success else "❌ FALLÓ"
                    print(f"{status} - {test_type}")

                successful = sum(1 for success in results.values() if success)
                total = len(results)
                print(f"\n🏁 Resultado: {successful}/{total} pruebas exitosas")

                if successful > 0:
                    print("🎉 ¡Al menos una conexión funciona!")
                    print("💡 Usa la que mejor te funcione en main.py")

        elif choice == "7":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Test interrumpido por el usuario")
    except Exception as e:
        print(f"❌ Error crítico: {e}")

    print("🔚 Fin del test de conectividad")
