#!/usr/bin/env python3
"""
Test de Bluetooth con bleak (Bluetooth Low Energy) para mBot
"""

import asyncio
import time
from bleak import BleakScanner, BleakClient

async def scan_bluetooth_devices():
    """Escanea dispositivos Bluetooth Low Energy"""
    print("🔵 ESCANEANDO DISPOSITIVOS BLUETOOTH LE")
    print("=" * 50)
    print("🔍 Buscando dispositivos... (esto puede tardar 10 segundos)")

    try:
        devices = await BleakScanner.discover(timeout=10.0)

        if not devices:
            print("❌ No se encontraron dispositivos Bluetooth LE")
            return []

        print(f"✅ Encontrados {len(devices)} dispositivos:")
        print()

        mbot_devices = []

        for device in devices:
            name = device.name or "Sin nombre"
            address = device.address
            rssi = device.rssi if hasattr(device, 'rssi') else 'N/A'

            print(f"📱 {name}")
            print(f"   📍 Dirección: {address}")
            print(f"   📶 RSSI: {rssi}")

            # Buscar dispositivos que podrían ser mBot
            if any(keyword in name.lower() for keyword in ['mbot', 'makeblock', 'arduino', 'esp32']):
                print(f"   🎯 ¡Posible mBot/Arduino encontrado!")
                mbot_devices.append(device)

            print()

        return mbot_devices

    except Exception as e:
        print(f"❌ Error durante escaneo: {e}")
        return []

async def try_connect_device(device):
    """Intenta conectar a un dispositivo específico"""
    print(f"🔗 Intentando conectar a: {device.name} ({device.address})")

    try:
        async with BleakClient(device.address) as client:
            print(f"✅ ¡Conectado a {device.name}!")

            # Obtener información del dispositivo
            print("📋 Información del dispositivo:")
            print(f"   🏷️  Nombre: {device.name}")
            print(f"   📍 Dirección: {device.address}")
            print(f"   🔗 Conectado: {client.is_connected}")

            # Listar servicios disponibles
            print("\n🔧 Servicios disponibles:")
            services = client.services

            for service in services:
                print(f"   🔹 Servicio: {service.uuid}")
                for char in service.characteristics:
                    print(f"     ↳ Característica: {char.uuid}")
                    if "write" in char.properties:
                        print(f"       ✍️  Puede escribir")
                    if "read" in char.properties:
                        print(f"       👁️  Puede leer")
                    if "notify" in char.properties:
                        print(f"       📢 Puede notificar")

            return True

    except Exception as e:
        print(f"❌ Error conectando a {device.name}: {e}")
        return False

async def interactive_ble_test():
    """Test interactivo completo"""
    print("🤖 TEST BLUETOOTH LOW ENERGY PARA MBOT")
    print("=" * 50)

    print("📋 Preparación:")
    print("1. 🔌 Desconecta el cable USB del mBot")
    print("2. 🔋 Enciende el mBot")
    print("3. 🔵 Asegúrate de que Bluetooth esté encendido en tu Mac")
    print("4. ⚙️  El mBot debe estar en modo BLE (algunos modelos lo soportan)")
    print()

    input("⏸️  Presiona Enter cuando esté listo...")

    # Escanear dispositivos
    devices = await scan_bluetooth_devices()

    if not devices:
        print("\n💡 CONSEJOS SI NO VES EL MBOT:")
        print("• Algunos mBot usan Bluetooth clásico, no BLE")
        print("• Verifica que tu mBot soporte Bluetooth Low Energy")
        print("• El mBot debe estar en modo emparejamiento")
        return

    # Intentar conectar a dispositivos encontrados
    print(f"\n🎯 Dispositivos candidatos encontrados: {len(devices)}")

    for i, device in enumerate(devices):
        print(f"\n--- Probando dispositivo {i+1}/{len(devices)} ---")
        success = await try_connect_device(device)

        if success:
            print("✅ ¡Conexión exitosa!")
            response = input("¿Continuar probando otros dispositivos? (y/n): ")
            if response.lower() != 'y':
                break
        else:
            print("❌ Falló la conexión")

async def quick_scan():
    """Escaneo rápido para probar bleak"""
    print("⚡ ESCANEO RÁPIDO DE BLUETOOTH LE")
    print("=" * 40)

    devices = await BleakScanner.discover(timeout=5.0)

    print(f"Encontrados {len(devices)} dispositivos en 5 segundos:")
    for device in devices:
        name = device.name or "Sin nombre"
        print(f"  📱 {name} ({device.address})")

def main():
    """Menú principal"""
    print("🔵 TEST BLEAK BLUETOOTH LE")
    print("=" * 30)

    while True:
        print("\n¿Qué quieres hacer?")
        print("1. ⚡ Escaneo rápido (5 segundos)")
        print("2. 🔍 Escaneo completo (10 segundos)")
        print("3. 🤖 Test interactivo completo")
        print("4. 🚪 Salir")

        choice = input("\nElige opción (1-4): ").strip()

        try:
            if choice == "1":
                asyncio.run(quick_scan())

            elif choice == "2":
                asyncio.run(scan_bluetooth_devices())

            elif choice == "3":
                asyncio.run(interactive_ble_test())

            elif choice == "4":
                print("👋 ¡Hasta luego!")
                break

            else:
                print("❌ Opción no válida")

        except KeyboardInterrupt:
            print("\n⏹️  Operación cancelada")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")
