#!/usr/bin/env python3
"""
Test específico para conectividad Bluetooth del mBot
"""

import time
import sys

def test_bluetooth_discovery():
    """Prueba el descubrimiento de dispositivos Bluetooth"""
    print("🔵 PROBANDO DESCUBRIMIENTO BLUETOOTH")
    print("=" * 50)

    try:
        import bluetooth
        print("✅ Módulo bluetooth importado correctamente")
    except ImportError as e:
        print(f"❌ Error importando bluetooth: {e}")
        print("💡 Intenta: pip3 install pybluez")
        return False

    try:
        print("🔍 Escaneando dispositivos Bluetooth...")
        print("⏳ Esto puede tardar 10-15 segundos...")

        nearby_devices = bluetooth.discover_devices(duration=10, lookup_names=True)

        if not nearby_devices:
            print("❌ No se encontraron dispositivos Bluetooth")
            print("💡 Asegúrate de que:")
            print("   - El Bluetooth esté encendido")
            print("   - El mBot esté encendido")
            print("   - El mBot esté en modo emparejamiento")
            return False

        print(f"✅ Encontrados {len(nearby_devices)} dispositivos:")
        for addr, name in nearby_devices:
            print(f"   📱 {name} ({addr})")
            if "mbot" in name.lower() or "makeblock" in name.lower():
                print(f"      🎯 ¡Posible mBot encontrado!")

        return True

    except Exception as e:
        print(f"❌ Error durante escaneo: {e}")
        return False

def test_bluetooth_connection(address=None):
    """Prueba conectar a un dispositivo específico"""
    if not address:
        print("❌ Se necesita una dirección MAC para conectar")
        return False

    print(f"\n🔵 PROBANDO CONEXIÓN A: {address}")
    print("=" * 50)

    try:
        import bluetooth

        print(f"🔗 Intentando conectar a {address}...")

        # Crear socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        # Intentar conectar
        sock.connect((address, 1))  # Canal RFCOMM 1

        print("✅ ¡Conexión Bluetooth exitosa!")

        # Prueba básica - enviar comando
        print("🧪 Enviando comando de prueba...")
        test_command = bytearray([0xff, 0x55, 0x7, 0x0, 0x2, 0x22, 0x40, 0x01, 0xf4, 0x01])
        sock.send(bytes(test_command))

        print("✅ Comando enviado correctamente")

        sock.close()
        return True

    except Exception as e:
        print(f"❌ Error conectando: {e}")
        return False

def interactive_bluetooth_test():
    """Test interactivo de Bluetooth"""
    print("🤖 TEST INTERACTIVO DE BLUETOOTH MBOT")
    print("=" * 50)

    print("Pasos para preparar el mBot:")
    print("1. 🔌 Desconecta el cable USB del mBot")
    print("2. 🔋 Enciende el mBot con el botón de encendido")
    print("3. 🔵 Asegúrate de que el Bluetooth del Mac esté encendido")
    print("4. ⚙️  Si es la primera vez, empareja el mBot desde Configuración > Bluetooth")
    print()

    input("⏸️  Presiona Enter cuando hayas completado los pasos anteriores...")

    # Paso 1: Descubrir dispositivos
    if not test_bluetooth_discovery():
        return False

    # Paso 2: Permitir selección manual
    print("\n" + "="*50)
    print("💡 Si viste tu mBot en la lista anterior, puedes intentar conectarte")
    print("💡 Necesitas la dirección MAC (formato: XX:XX:XX:XX:XX:XX)")
    print()

    mac_address = input("🔵 Ingresa la dirección MAC del mBot (o Enter para salir): ").strip()

    if mac_address:
        test_bluetooth_connection(mac_address)

    print("\n🔚 Test completado")

def main():
    print("🔵 TEST DE BLUETOOTH PARA MBOT")
    print("=" * 50)

    while True:
        print("\n¿Qué quieres probar?")
        print("1. 🔍 Escanear dispositivos Bluetooth")
        print("2. 🔗 Conectar a dirección específica")
        print("3. 🤖 Test interactivo completo")
        print("4. 🚪 Salir")

        choice = input("\nElige opción (1-4): ").strip()

        if choice == "1":
            test_bluetooth_discovery()

        elif choice == "2":
            address = input("Dirección MAC: ").strip()
            test_bluetooth_connection(address)

        elif choice == "3":
            interactive_bluetooth_test()

        elif choice == "4":
            print("👋 ¡Hasta luego!")
            break

        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Test interrumpido")
    except Exception as e:
        print(f"❌ Error crítico: {e}")
