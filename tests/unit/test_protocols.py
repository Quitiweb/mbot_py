#!/usr/bin/env python3
"""
Test específico de comandos mBot BLE - Prueba protocolos alternativos
"""

import asyncio
from bleak import BleakScanner, BleakClient
import time
import struct

async def test_specific_protocols():
    """Prueba protocolos específicos de mBot"""

    # Encontrar mBot
    devices = await BleakScanner.discover(timeout=5.0)
    mbot_device = None
    for device in devices:
        if 'makeblock' in (device.name or "").lower():
            mbot_device = device
            break

    if not mbot_device:
        print("❌ No se encontró mBot")
        return

    print(f"🤖 Conectando a {mbot_device.name}...")

    async with BleakClient(mbot_device.address) as client:

        # Características a probar
        chars_to_test = [
            "0000ffe3-0000-1000-8000-00805f9b34fb",  # Más común
            "00006487-3c17-d293-8e48-14fe2e4da212",  # También funciona
        ]

        for char_uuid in chars_to_test:
            print(f"\n🔧 PROBANDO CARACTERÍSTICA: {char_uuid}")
            print("=" * 60)

            # 1. Protocolo mBot estándar (el que hemos usado)
            print("📋 1. PROTOCOLO ESTÁNDAR MBOT:")
            await test_standard_protocol(client, char_uuid)

            # 2. Protocolo Makeblock BLE (basado en análisis de apps)
            print("\n📋 2. PROTOCOLO MAKEBLOCK BLE:")
            await test_makeblock_ble_protocol(client, char_uuid)

            # 3. Protocolo simplificado
            print("\n📋 3. PROTOCOLO SIMPLIFICADO:")
            await test_simple_protocol(client, char_uuid)

            # 4. Protocolo con header diferente
            print("\n📋 4. PROTOCOLO CON HEADER ALTERNATIVO:")
            await test_alternative_header_protocol(client, char_uuid)

            await asyncio.sleep(1)

async def test_standard_protocol(client, char_uuid):
    """Protocolo estándar mBot USB/IR"""
    commands = {
        "LED Rojo": bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 255, 0, 0]),
        "Buzzer": bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x22, 0x40, 0x01, 0xf4, 0x01]),
        "Adelante": bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 100, 100]),
    }

    for name, cmd in commands.items():
        try:
            print(f"   📤 {name}: {cmd.hex()}")
            await client.write_gatt_char(char_uuid, cmd)
            await asyncio.sleep(1.5)
            print(f"   ✅ Enviado")
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def test_makeblock_ble_protocol(client, char_uuid):
    """Protocolo específico para Makeblock BLE"""
    commands = {
        "LED Rojo": bytes([0xA5, 0x5A, 0x0C, 0x00, 0x02, 0x08, 0x07, 0x02, 0x00, 0xFF, 0x00, 0x00]),
        "Buzzer": bytes([0xA5, 0x5A, 0x08, 0x00, 0x02, 0x22, 0x01, 0xF4, 0x01]),
        "Adelante": bytes([0xA5, 0x5A, 0x09, 0x00, 0x02, 0x05, 0x64, 0x64]),
    }

    for name, cmd in commands.items():
        try:
            print(f"   📤 {name}: {cmd.hex()}")
            await client.write_gatt_char(char_uuid, cmd)
            await asyncio.sleep(1.5)
            print(f"   ✅ Enviado")
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def test_simple_protocol(client, char_uuid):
    """Protocolo simplificado"""
    commands = {
        "LED Rojo": bytes([0x08, 0x07, 0x02, 0x00, 0xFF, 0x00, 0x00]),  # Sin header
        "Buzzer": bytes([0x22, 0x01, 0xF4, 0x01]),
        "Adelante": bytes([0x05, 0x64, 0x64]),
    }

    for name, cmd in commands.items():
        try:
            print(f"   📤 {name}: {cmd.hex()}")
            await client.write_gatt_char(char_uuid, cmd)
            await asyncio.sleep(1.5)
            print(f"   ✅ Enviado")
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def test_alternative_header_protocol(client, char_uuid):
    """Protocolo con header alternativo"""
    commands = {
        "LED Rojo": bytes([0xF0, 0x0F, 0x08, 0x07, 0x02, 0x00, 0xFF, 0x00, 0x00]),
        "Buzzer": bytes([0xF0, 0x0F, 0x22, 0x01, 0xF4, 0x01]),
        "Adelante": bytes([0xF0, 0x0F, 0x05, 0x64, 0x64]),
    }

    for name, cmd in commands.items():
        try:
            print(f"   📤 {name}: {cmd.hex()}")
            await client.write_gatt_char(char_uuid, cmd)
            await asyncio.sleep(1.5)
            print(f"   ✅ Enviado")
        except Exception as e:
            print(f"   ❌ Error: {e}")

async def monitor_responses():
    """Monitor de respuestas del mBot"""
    print("\n📡 MONITOREANDO RESPUESTAS DEL MBOT")
    print("=" * 40)

    # Encontrar mBot
    devices = await BleakScanner.discover(timeout=5.0)
    mbot_device = None
    for device in devices:
        if 'makeblock' in (device.name or "").lower():
            mbot_device = device
            break

    if not mbot_device:
        return

    def notification_handler(sender, data):
        print(f"📨 {sender}: {data.hex()} = {list(data)}")

    async with BleakClient(mbot_device.address) as client:
        # Activar todas las notificaciones
        notify_chars = [
            "0000ffe2-0000-1000-8000-00805f9b34fb",
            "00006487-3c17-d293-8e48-14fe2e4da212"
        ]

        for char in notify_chars:
            try:
                await client.start_notify(char, notification_handler)
                print(f"✅ Notificaciones activadas en {char}")
            except:
                print(f"❌ No se pudo activar {char}")

        # Enviar un comando simple y esperar respuesta
        print("\n📤 Enviando comando de prueba...")
        test_cmd = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 255, 0, 0])
        try:
            await client.write_gatt_char("0000ffe3-0000-1000-8000-00805f9b34fb", test_cmd)
            print("✅ Comando enviado, esperando respuestas...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"❌ Error: {e}")

async def main():
    print("🔍 TEST ESPECÍFICO DE PROTOCOLOS MBOT BLE")
    print("⚠️  Asegúrate de que el mBot esté encendido y observa si:")
    print("   - Los LEDs cambian de color")
    print("   - Suena el buzzer")
    print("   - El robot se mueve")
    print()
    input("Presiona Enter para continuar...")

    try:
        await test_specific_protocols()
        await monitor_responses()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
