#!/usr/bin/env python3
"""
mBot BLE usando EXACTAMENTE los mismos comandos que la librería original
"""

import signal
import sys
import asyncio
import struct
import time
from time import sleep
import threading
import serial
import serial.tools.list_ports

try:
    from bleak import BleakScanner, BleakClient
    BLUETOOTH_AVAILABLE = True
except ImportError:
    BLUETOOTH_AVAILABLE = False

class MBotOriginalProtocol:
    def __init__(self, connection_type="auto"):
        """
        mBot usando EXACTAMENTE el protocolo original
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
        self._request_index = 1
        self._serial_buffer = bytearray()

        print(f"🤖 Iniciando mBot con protocolo ORIGINAL (modo: {connection_type})")

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
        """Conecta por USB usando el método original"""
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
        """Busca puerto USB - MÉTODO ORIGINAL"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.description or "CH340" in port.description:
                return port.device
        return None

    def __writePackage(self, pack):
        """Método de escritura ORIGINAL"""
        if self.connection_type == "usb" and self.serial:
            self.serial.write(pack)
            self.serial.flush()
            sleep(0.01)
            return True

        elif self.connection_type == "bluetooth" and self.ble_connected:
            try:
                future = asyncio.run_coroutine_threadsafe(
                    self._async_write(pack),
                    self.ble_loop
                )
                result = future.result(timeout=2.0)
                sleep(0.01)  # Mismo delay que USB
                return result
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

    # ------------------------------------------------------------------
    # Lectura simplificada de sensores (solo USB en esta versión)
    # ------------------------------------------------------------------
    def _next_request_index(self):
        self._request_index = (self._request_index + 1) % 255
        if self._request_index == 0:
            self._request_index = 1
        return self._request_index

    def get_ultrasonic_distance(self, port=1, slot=3, timeout=0.5):
        if self.connection_type != "usb" or not self.serial:
            raise NotImplementedError("La lectura del sensor ultrasónico solo está disponible por USB en esta versión simplificada.")

        idx = self._next_request_index()
        packet = bytearray([0xff, 0x55, 0x04, idx, 0x01, 0x01, port, slot])
        self.__writePackage(packet)
        response = self._read_serial_frame(idx, timeout)
        if not response:
            return None
        _, value = response
        return value

    def _read_serial_frame(self, expected_idx, timeout):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.serial.in_waiting:
                data = self.serial.read(self.serial.in_waiting)
                self._serial_buffer.extend(data)

            parsed = self._try_parse_frame(expected_idx)
            if parsed:
                return parsed

            sleep(0.01)
        return None

    def _try_parse_frame(self, expected_idx):
        buffer = self._serial_buffer
        while len(buffer) >= 3:
            if buffer[0] != 0xff or buffer[1] != 0x55:
                buffer.pop(0)
                continue

            length = buffer[2]
            total = length + 3
            if len(buffer) < total:
                return None

            frame = bytes(buffer[:total])
            del buffer[:total]

            idx = frame[3]
            if expected_idx is not None and idx != expected_idx:
                # Descartar respuestas antiguas
                continue

            data_type = frame[4]
            payload = frame[5:]
            value = self._decode_value(data_type, payload)
            return idx, value
        return None

    def _decode_value(self, data_type, payload):
        if data_type == 1 and payload:
            return payload[0]
        if data_type == 2 and len(payload) >= 4:
            return struct.unpack('f', payload[:4])[0]
        if data_type == 3 and len(payload) >= 2:
            return struct.unpack('h', payload[:2])[0]
        return None

    def short2bytes(self, sval):
        """Conversión ORIGINAL de short a bytes"""
        val = struct.pack("h", sval)
        return [val[i] for i in range(2)]

    def float2bytes(self, fval):
        """Conversión ORIGINAL de float a bytes"""
        val = struct.pack("f", fval)
        return [val[i] for i in range(4)]

    # MÉTODOS ORIGINALES EXACTOS
    def doMove(self, leftSpeed, rightSpeed):
        """MÉTODO ORIGINAL - Usar velocidades con signo correcto"""
        self.__writePackage(bytearray([0xff, 0x55, 0x7, 0x0, 0x2, 0x5] + self.short2bytes(-leftSpeed) + self.short2bytes(rightSpeed)))

    def doRGBLedOnBoard(self, index, red, green, blue):
        """MÉTODO ORIGINAL"""
        self.__writePackage(bytearray([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, index, red, green, blue]))

    def doRGBLed(self, port, slot, index, red, green, blue):
        """MÉTODO ORIGINAL"""
        self.__writePackage(bytearray([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, port, slot, index, red, green, blue]))

    def doBuzzer(self, buzzer, time=0):
        """MÉTODO ORIGINAL"""
        self.__writePackage(bytearray([0xff, 0x55, 0x7, 0x0, 0x2, 0x22] + self.short2bytes(buzzer) + self.short2bytes(time)))

    def doMotor(self, port, speed):
        """MÉTODO ORIGINAL"""
        self.__writePackage(bytearray([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, port]+self.short2bytes(speed)))

    def doServo(self, port, slot, angle):
        """MÉTODO ORIGINAL"""
        self.__writePackage(bytearray([0xff, 0x55, 0x6, 0x0, 0x2, 0xb, port, slot, angle]))

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

def test_original_protocol():
    """Test con protocolo original exacto"""
    print("🧪 PROBANDO PROTOCOLO ORIGINAL EXACTO")
    print("=" * 50)

    try:
        # Conectar
        mbot = MBotOriginalProtocol(connection_type="auto")

        print(f"\n✅ Conectado por: {mbot.connection_type}")

        print("\n1️⃣ PROBANDO COMANDO MOVE ORIGINAL...")
        print("   Adelante con protocolo original...")
        mbot.doMove(100, 100)  # Esto debería ser: -100 (izq) y 100 (der) como 2 bytes cada uno
        sleep(1)

        print("   STOP con protocolo original...")
        mbot.doMove(0, 0)  # Esto debería ser: 0 y 0 como 2 bytes cada uno
        sleep(1)

        print("\n2️⃣ PROBANDO LED ORIGINAL...")
        mbot.doRGBLedOnBoard(0, 255, 0, 0)  # Rojo
        sleep(1)
        mbot.doRGBLedOnBoard(0, 0, 0, 0)   # Apagar

        print("\n3️⃣ PROBANDO BUZZER ORIGINAL...")
        mbot.doBuzzer(440, 500)  # 440Hz por 500ms como 2 bytes cada uno
        sleep(1)

        print("\n4️⃣ PROBANDO GIRO...")
        print("   Giro izquierda...")
        mbot.doMove(100, -100)  # Debería ser: -100 (izq) y -100 (der)
        sleep(1)

        print("   STOP final...")
        mbot.doMove(0, 0)

        print("\n✅ TEST PROTOCOLO ORIGINAL COMPLETADO")
        print("¿Se detuvo correctamente esta vez?")

        mbot.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔬 TEST DEL PROTOCOLO ORIGINAL EXACTO")
    print("=" * 60)
    print("Este test usa EXACTAMENTE los mismos comandos que la librería original")
    print("La diferencia clave: velocidades como 2 bytes (short) en lugar de 1 byte")
    print()
    input("Presiona Enter para probar...")

    test_original_protocol()
