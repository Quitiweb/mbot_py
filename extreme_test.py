#!/usr/bin/env python3
"""
Test EXTREMO para mBot - Comandos obviamente visibles
"""

import asyncio
from bleak import BleakScanner, BleakClient
import time

async def extreme_test():
    """Test con comandos extremos para asegurar visibilidad"""

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

        char_uuid = "0000ffe3-0000-1000-8000-00805f9b34fb"  # La que mejor funciona

        print("🔴 LED ROJO EXTREMO (255, 0, 0)")
        cmd = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 255, 0, 0])
        await client.write_gatt_char(char_uuid, cmd)
        print("   Mira los LEDs del mBot - deben estar ROJOS brillantes")
        await asyncio.sleep(3)

        print("🟢 LED VERDE EXTREMO (0, 255, 0)")
        cmd = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 0, 255, 0])
        await client.write_gatt_char(char_uuid, cmd)
        print("   Mira los LEDs del mBot - deben estar VERDES brillantes")
        await asyncio.sleep(3)

        print("🔵 LED AZUL EXTREMO (0, 0, 255)")
        cmd = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 0, 0, 255])
        await client.write_gatt_char(char_uuid, cmd)
        print("   Mira los LEDs del mBot - deben estar AZULES brillantes")
        await asyncio.sleep(3)

        print("⚪ LEDs BLANCOS EXTREMO (255, 255, 255)")
        cmd = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 255, 255, 255])
        await client.write_gatt_char(char_uuid, cmd)
        print("   Mira los LEDs del mBot - deben estar BLANCOS brillantes")
        await asyncio.sleep(3)

        print("🎵 BUZZER EXTREMO - Frecuencia alta (2000Hz)")
        # Frecuencia 2000Hz = 0x07D0
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x22, 0x07, 0xD0, 0x03, 0xE8])  # 2000Hz, 1000ms
        await client.write_gatt_char(char_uuid, cmd)
        print("   Escucha - debe sonar un pitido AGUDO por 1 segundo")
        await asyncio.sleep(2)

        print("🎵 BUZZER MEDIO (500Hz)")
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x22, 0x01, 0xF4, 0x03, 0xE8])  # 500Hz, 1000ms
        await client.write_gatt_char(char_uuid, cmd)
        print("   Escucha - debe sonar un pitido MEDIO por 1 segundo")
        await asyncio.sleep(2)

        print("⬆️ MOVIMIENTO EXTREMO ADELANTE (255, 255)")
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 255, 255])
        await client.write_gatt_char(char_uuid, cmd)
        print("   El mBot debe moverse RÁPIDO hacia adelante")
        await asyncio.sleep(2)

        print("🛑 PARAR")
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 0, 0])
        await client.write_gatt_char(char_uuid, cmd)
        await asyncio.sleep(1)

        print("⬇️ MOVIMIENTO EXTREMO ATRÁS (-255, -255)")
        # Para valores negativos usar complemento a 2 en un byte
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 1, 1])  # Atrás muy lento
        await client.write_gatt_char(char_uuid, cmd)
        print("   El mBot debe moverse hacia atrás")
        await asyncio.sleep(2)

        print("🛑 PARAR FINAL")
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 0, 0])
        await client.write_gatt_char(char_uuid, cmd)

        print("🔄 GIRO EXTREMO (255, -255)")
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 255, 1])  # Un lado rápido, otro lento
        await client.write_gatt_char(char_uuid, cmd)
        print("   El mBot debe GIRAR rápidamente")
        await asyncio.sleep(2)

        print("🛑 PARAR FINAL")
        cmd = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 0, 0])
        await client.write_gatt_char(char_uuid, cmd)

        print("⚫ APAGAR LEDs")
        cmd = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, 0x0, 0, 0, 0])
        await client.write_gatt_char(char_uuid, cmd)

        print("\n✅ PRUEBAS EXTREMAS COMPLETADAS")
        print("Si no viste/oíste NADA, entonces hay un problema de protocolo")

async def test_motor_individual():
    """Test de motores individuales"""
    print("\n🔧 PROBANDO MOTORES INDIVIDUALES")

    devices = await BleakScanner.discover(timeout=5.0)
    mbot_device = None
    for device in devices:
        if 'makeblock' in (device.name or "").lower():
            mbot_device = device
            break

    if not mbot_device:
        return

    async with BleakClient(mbot_device.address) as client:
        char_uuid = "0000ffe3-0000-1000-8000-00805f9b34fb"

        print("🔧 Motor izquierdo M1 a velocidad 200")
        cmd = bytes([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, 0x9, 200])  # Motor puerto 9
        await client.write_gatt_char(char_uuid, cmd)
        await asyncio.sleep(2)

        print("🔧 Parar motor M1")
        cmd = bytes([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, 0x9, 0])
        await client.write_gatt_char(char_uuid, cmd)
        await asyncio.sleep(1)

        print("🔧 Motor derecho M2 a velocidad 200")
        cmd = bytes([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, 0xa, 200])  # Motor puerto 10
        await client.write_gatt_char(char_uuid, cmd)
        await asyncio.sleep(2)

        print("🔧 Parar motor M2")
        cmd = bytes([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, 0xa, 0])
        await client.write_gatt_char(char_uuid, cmd)

def main():
    print("🔥 TEST EXTREMO PARA MBOT - COMANDOS OBVIAMENTE VISIBLES")
    print("=" * 60)
    print("⚠️  IMPORTANTE:")
    print("   1. El mBot debe estar encendido (LED de encendido visible)")
    print("   2. Cable USB desconectado")
    print("   3. Ponlo en un lugar donde puedas verlo bien")
    print("   4. Sube el volumen si quieres oír el buzzer")
    print("   5. Observa CUIDADOSAMENTE los LEDs y el movimiento")
    print()
    input("Presiona Enter cuando esté todo listo...")

    asyncio.run(extreme_test())
    print()
    input("¿Viste algo? Presiona Enter para probar motores individuales...")
    asyncio.run(test_motor_individual())

if __name__ == "__main__":
    main()
