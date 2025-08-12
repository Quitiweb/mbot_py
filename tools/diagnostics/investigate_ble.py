#!/usr/bin/env python3
"""
Investigador BLE para mBot - Analiza las características y protocolos
"""

import asyncio
from bleak import BleakScanner, BleakClient

async def analyze_mbot_ble():
    """Analiza en detalle las características del mBot BLE"""
    print("🔍 ANALIZANDO MBOT BLE EN DETALLE")
    print("=" * 50)

    # Encontrar el mBot
    print("Buscando mBot...")
    devices = await BleakScanner.discover(timeout=10.0)

    mbot_device = None
    for device in devices:
        name = device.name or ""
        if 'makeblock' in name.lower() or 'mbot' in name.lower():
            mbot_device = device
            break

    if not mbot_device:
        print("❌ No se encontró mBot")
        return

    print(f"✅ Encontrado: {mbot_device.name} ({mbot_device.address})")

    # Conectar y analizar
    async with BleakClient(mbot_device.address) as client:
        print("\n📋 SERVICIOS Y CARACTERÍSTICAS:")
        print("-" * 40)

        services = client.services
        write_chars = []
        notify_chars = []

        for service in services:
            print(f"\n🔧 Servicio: {service.uuid}")
            if service.description:
                print(f"   Descripción: {service.description}")

            for char in service.characteristics:
                props = ", ".join(char.properties)
                print(f"   📡 {char.uuid} [{props}]")

                if "write" in char.properties:
                    write_chars.append(char.uuid)
                if "notify" in char.properties:
                    notify_chars.append(char.uuid)

        print(f"\n📝 CARACTERÍSTICAS DE ESCRITURA ({len(write_chars)}):")
        for char in write_chars:
            print(f"   ✍️  {char}")

        print(f"\n📢 CARACTERÍSTICAS DE NOTIFICACIÓN ({len(notify_chars)}):")
        for char in notify_chars:
            print(f"   📨 {char}")

        # Probar diferentes comandos en diferentes características
        print(f"\n🧪 PROBANDO COMANDOS...")
        print("-" * 40)

        # Comandos de prueba (protocolo mBot estándar)
        test_commands = {
            "LED_ROJO": bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 255, 0, 0]),
            "BUZZER": bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x22, 0x40, 0x01, 0xf4, 0x01]),
            "MOVE_FORWARD": bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 100, 100]),
        }

        for write_char in write_chars:
            print(f"\n🔧 Probando característica: {write_char}")

            for cmd_name, cmd_data in test_commands.items():
                try:
                    print(f"   📤 Enviando {cmd_name}...")
                    await client.write_gatt_char(write_char, cmd_data)
                    print(f"   ✅ {cmd_name} enviado sin errores")

                    # Esperar un poco para ver el efecto
                    await asyncio.sleep(1.5)

                except Exception as e:
                    print(f"   ❌ Error con {cmd_name}: {e}")

        # Configurar notificaciones para ver respuestas
        print(f"\n📡 CONFIGURANDO NOTIFICACIONES...")
        for notify_char in notify_chars:
            try:
                print(f"📨 Activando notificaciones en {notify_char}")
                await client.start_notify(notify_char, notification_handler)
                await asyncio.sleep(2)  # Esperar notificaciones
                await client.stop_notify(notify_char)
            except Exception as e:
                print(f"❌ Error con notificaciones: {e}")

def notification_handler(sender, data):
    """Maneja notificaciones del mBot"""
    print(f"📨 Notificación de {sender}: {data.hex()} ({list(data)})")

async def test_makeblock_app_commands():
    """Prueba comandos que usa la app oficial de Makeblock"""
    print("\n🎮 PROBANDO COMANDOS DE LA APP MAKEBLOCK")
    print("=" * 50)

    # Encontrar mBot
    devices = await BleakScanner.discover(timeout=5.0)
    mbot_device = None
    for device in devices:
        name = device.name or ""
        if 'makeblock' in name.lower():
            mbot_device = device
            break

    if not mbot_device:
        print("❌ No se encontró mBot")
        return

    async with BleakClient(mbot_device.address) as client:
        # Comandos que posiblemente usa la app oficial
        app_commands = {
            "INIT": bytes([0xA5, 0x5A, 0x07, 0x01, 0x01, 0x29]),  # Posible inicialización
            "LED_ON": bytes([0xA5, 0x5A, 0x0A, 0x01, 0x07, 0x02, 0x09, 0xFF, 0x00, 0x00]),  # LED rojo
            "BUZZER_BEEP": bytes([0xA5, 0x5A, 0x08, 0x01, 0x22, 0x01, 0xB8, 0x0B]),  # Buzzer
            "MOVE": bytes([0xA5, 0x5A, 0x09, 0x01, 0x05, 0x64, 0x64, 0x00, 0x00]),  # Movimiento
        }

        # Probar con la característica más común
        write_char = "0000ffe3-0000-1000-8000-00805f9b34fb"

        for cmd_name, cmd_data in app_commands.items():
            try:
                print(f"📤 Enviando {cmd_name}: {cmd_data.hex()}")
                await client.write_gatt_char(write_char, cmd_data)
                await asyncio.sleep(2)
                print(f"✅ {cmd_name} enviado")
            except Exception as e:
                print(f"❌ Error con {cmd_name}: {e}")

async def main():
    """Función principal"""
    try:
        await analyze_mbot_ble()
        await test_makeblock_app_commands()
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    print("🔍 INVESTIGADOR BLE PARA MBOT")
    print("Asegúrate de que el mBot esté encendido y sin cable USB")
    print()
    input("Presiona Enter para empezar...")

    asyncio.run(main())
