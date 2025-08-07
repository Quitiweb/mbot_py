#!/usr/bin/env python3
"""
mBot BLE con protocolo de parada corregido
"""

import signal
import sys
import asyncio
from time import sleep
import threading
import serial
import serial.tools.list_ports

try:
    from bleak import BleakScanner, BleakClient
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False

class MBotBLEFixed:
    def __init__(self, connection_type="auto"):
        """
        mBot con protocolo de parada BLE corregido
        """
        signal.signal(signal.SIGINT, self.exit)
        self.exiting = False
        self.connection_type = None
        self.serial = None

        # BLE attributes
        self.ble_client = None
        self.ble_device = None
        self.ble_write_char = "0000ffe3-0000-1000-8000-00805f9b34fb"
        self.ble_connected = False
        self.ble_thread = None
        self.ble_loop = None

        print(f"🤖 Iniciando mBot BLE Fixed (modo: {connection_type})")

        # Conectar
        if connection_type == "auto":
            if self._try_bluetooth_connection():
                pass
            elif self._try_usb_connection():
                pass
            else:
                raise Exception("No se pudo conectar al mBot")
        elif connection_type == "bluetooth":
            if not self._try_bluetooth_connection():
                raise Exception("No se pudo conectar por Bluetooth")
        elif connection_type == "usb":
            if not self._try_usb_connection():
                raise Exception("No se pudo conectar por USB")

    def _try_bluetooth_connection(self):
        """Conecta por BLE"""
        if not BLUETOOTH_AVAILABLE:
            print("🔵 Bluetooth LE no disponible")
            return False

        try:
            print("🔵 Iniciando conexión Bluetooth LE...")

            self.ble_thread = threading.Thread(target=self._run_ble_connection, daemon=True)
            self.ble_thread.start()

            # Esperar conexión
            for _ in range(30):
                if self.ble_connected:
                    self.connection_type = "bluetooth"
                    print("✅ mBot conectado por Bluetooth LE")
                    return True
                sleep(0.5)

            print("🔵 Timeout en conexión Bluetooth LE")
            return False

        except Exception as e:
            print(f"🔵 Error en conexión BLE: {e}")
            return False

    def _run_ble_connection(self):
        """Thread para BLE"""
        try:
            self.ble_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.ble_loop)
            self.ble_loop.run_until_complete(self._async_connect())
        except Exception as e:
            print(f"🔵 Error en thread BLE: {e}")

    async def _async_connect(self):
        """Conexión BLE asíncrona"""
        try:
            # Buscar mBot
            devices = await BleakScanner.discover(timeout=10.0)
            device = None

            for d in devices:
                name = d.name or ""
                if 'makeblock' in name.lower() or 'mbot' in name.lower():
                    device = d
                    break

            if not device:
                print("🔵 No se encontró mBot BLE")
                return

            print(f"🔵 Conectando a {device.name}...")

            # Conectar
            self.ble_client = BleakClient(device.address)
            await self.ble_client.connect()

            if not self.ble_client.is_connected:
                return

            self.ble_device = device
            self.ble_connected = True

            # Mantener conexión
            while self.ble_connected and not self.exiting:
                await asyncio.sleep(0.1)

        except Exception as e:
            print(f"🔵 Error en conexión: {e}")

    def _try_usb_connection(self):
        """Conecta por USB"""
        try:
            print("🔌 Buscando mBot por USB...")
            port = self._find_mbot_usb_port()

            if not port:
                return False

            self.serial = serial.Serial(port, 115200, timeout=1)
            self.connection_type = "usb"
            print(f"✅ mBot conectado por USB ({port})")
            sleep(2)
            return True

        except Exception as e:
            print(f"🔌 Error USB: {e}")
            return False

    def _find_mbot_usb_port(self):
        """Busca puerto USB"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if any(keyword in port.description.upper() for keyword in ["CH340", "CH341", "USB"]):
                return port.device
        return None

    def write(self, data):
        """Envía datos con protocolo corregido"""
        if not data:
            return False

        if self.connection_type == "usb" and self.serial:
            try:
                self.serial.write(data)
                return True
            except:
                return False

        elif self.connection_type == "bluetooth" and self.ble_connected:
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._async_write(data),
                    self.ble_loop
                )
                return future.result(timeout=2.0)
            except:
                return False
        return False

    async def _async_write(self, data):
        """Escritura BLE asíncrona"""
        try:
            if self.ble_client and self.ble_client.is_connected:
                await self.ble_client.write_gatt_char(self.ble_write_char, data)
                return True
            return False
        except:
            return False

    def close(self):
        """Cierra conexión"""
        self.exiting = True

        if self.connection_type == "bluetooth":
            self.ble_connected = False
            if self.ble_client and self.ble_loop:
                try:
                    future = asyncio.run_coroutine_threadsafe(
                        self.ble_client.disconnect(),
                        self.ble_loop
                    )
                    future.result(timeout=2.0)
                except:
                    pass

        elif self.connection_type == "usb" and self.serial:
            try:
                self.serial.close()
            except:
                pass

        print("🔌 Conexión cerrada")

    def exit(self, signal, frame):
        print("\n🛑 Cerrando...")
        self.close()
        sys.exit(0)

    # Métodos corregidos para BLE
    def doMove(self, leftSpeed, rightSpeed):
        """Movimiento con protocolo BLE corregido"""
        if leftSpeed < 0:
            leftSpeed = 256 + leftSpeed
        if rightSpeed < 0:
            rightSpeed = 256 + rightSpeed

        # Protocolo estándar para movimiento
        message = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, leftSpeed & 0xFF, rightSpeed & 0xFF])
        return self.write(message)

    def forceStop(self):
        """PARADA FORZADA - Múltiples métodos"""
        print("🛑 PARADA FORZADA...")

        success = False

        # Método 1: Parada estándar múltiple
        for _ in range(3):
            if self.doMove(0, 0):
                success = True
            sleep(0.05)

        # Método 2: Motores individuales
        for _ in range(2):
            if self.doMotor(9, 0) and self.doMotor(10, 0):
                success = True
            sleep(0.05)

        # Método 3: Protocolo alternativo de parada
        if self.connection_type == "bluetooth":
            # Comando de reset/parada específico para BLE
            reset_cmd = bytes([0xA5, 0x5A, 0x09, 0x00, 0x02, 0x05, 0x00, 0x00])
            if self.write(reset_cmd):
                success = True

            # Comando de parada absoluta
            stop_cmd = bytes([0xff, 0x55, 0x4, 0x0, 0x2, 0xff])
            if self.write(stop_cmd):
                success = True

        return success

    def doRGBLedOnBoard(self, index, red, green, blue):
        """LEDs con limpieza automática"""
        message = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, index, red, green, blue])
        return self.write(message)

    def doBuzzer(self, frequency, duration):
        """Buzzer corregido"""
        freq_high = (frequency >> 8) & 0xFF
        freq_low = frequency & 0xFF
        dur_high = (duration >> 8) & 0xFF
        dur_low = duration & 0xFF

        message = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x22, freq_high, freq_low, dur_high, dur_low])
        return self.write(message)

    def doMotor(self, port, speed):
        """Motor individual"""
        if speed < 0:
            speed = 256 + speed
        message = bytes([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, port, speed & 0xFF])
        return self.write(message)

    def emergencyCleanup(self):
        """Limpieza de emergencia completa"""
        print("🚨 LIMPIEZA DE EMERGENCIA...")

        # Parar todo
        self.forceStop()

        # Apagar LEDs
        for i in range(2):
            self.doRGBLedOnBoard(i, 0, 0, 0)

        # Asegurar parada de motores
        for port in [9, 10]:
            self.doMotor(port, 0)

        print("✅ Limpieza completada")

def test_fixed_mbot():
    """Test del mBot con parada corregida"""
    print("🧪 PROBANDO MBOT CON PARADA CORREGIDA")
    print("=" * 50)

    try:
        mbot = MBotBLEFixed(connection_type="auto")

        print(f"✅ Conectado por: {mbot.connection_type}")

        # Test de la secuencia problemática
        print("\n🚨 REPRODUCIENDO SECUENCIA PROBLEMÁTICA...")
        print("1. LED Verde...")
        mbot.doRGBLedOnBoard(0, 0, 255, 0)

        print("2. Buzzer...")
        mbot.doBuzzer(440, 500)

        print("3. Movimiento...")
        mbot.doMove(100, 100)

        print("4. Esperando 2 segundos...")
        sleep(2)

        print("5. 🛑 PARADA FORZADA...")
        success = mbot.forceStop()
        print(f"   Resultado: {'✅ Éxito' if success else '❌ Falló'}")

        sleep(1)

        print("6. 🚨 LIMPIEZA DE EMERGENCIA...")
        mbot.emergencyCleanup()

        print("\n✅ TEST COMPLETADO")
        print("¿El robot se detuvo correctamente?")

        mbot.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_fixed_mbot()
