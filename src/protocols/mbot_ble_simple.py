#!/usr/bin/env python3
"""
mBot Bluetooth LE Controller - Versión simplificada y estable
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
    print("🔵 Bluetooth LE disponible")
except ImportError:
    BLUETOOTH_AVAILABLE = False
    print("⚠️  Bluetooth LE no disponible - solo USB")

class MBotBLE:
    def __init__(self, connection_type="auto"):
        """
        Inicializa el mBot con soporte BLE mejorado
        """
        signal.signal(signal.SIGINT, self.exit)
        self.exiting = False
        self.connection_type = None
        self.serial = None

        # BLE attributes
        self.ble_client = None
        self.ble_device = None
        self.ble_write_char = None
        self.ble_connected = False
        self.ble_thread = None
        self.ble_loop = None

        # Buffer para datos
        self.buffer = []

        print(f"🤖 Iniciando mBot (modo: {connection_type})")

        # Intentar conectar
        if connection_type == "auto":
            if self._try_bluetooth_connection():
                pass  # Conectado por BLE
            elif self._try_usb_connection():
                pass  # Conectado por USB
            else:
                raise Exception("No se pudo conectar al mBot")
        elif connection_type == "bluetooth":
            if not self._try_bluetooth_connection():
                raise Exception("No se pudo conectar por Bluetooth")
        elif connection_type == "usb":
            if not self._try_usb_connection():
                raise Exception("No se pudo conectar por USB")

    def _try_bluetooth_connection(self):
        """Intenta conectar por BLE usando un thread separado"""
        if not BLUETOOTH_AVAILABLE:
            print("🔵 Bluetooth LE no disponible")
            return False

        try:
            print("🔵 Iniciando conexión Bluetooth LE...")

            # Crear thread para BLE
            self.ble_thread = threading.Thread(target=self._run_ble_connection, daemon=True)
            self.ble_thread.start()

            # Esperar conexión (timeout 15 segundos)
            for _ in range(30):  # 30 * 0.5 = 15 segundos
                if self.ble_connected:
                    self.connection_type = "bluetooth"
                    print("✅ Conexión Bluetooth LE establecida")
                    return True
                sleep(0.5)

            print("🔵 Timeout en conexión Bluetooth LE")
            return False

        except Exception as e:
            print(f"🔵 Error en conexión BLE: {e}")
            return False

    def _run_ble_connection(self):
        """Ejecuta la conexión BLE en un thread separado"""
        try:
            # Crear nuevo event loop para este thread
            self.ble_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.ble_loop)

            # Ejecutar conexión
            self.ble_loop.run_until_complete(self._async_connect())

        except Exception as e:
            print(f"🔵 Error en thread BLE: {e}")

    async def _async_connect(self):
        """Conexión BLE asíncrona"""
        try:
            # Buscar mBot
            print("🔍 Escaneando dispositivos BLE...")
            device = await self._find_mbot_ble()

            if not device:
                print("🔵 No se encontró mBot BLE")
                return

            print(f"🔵 Conectando a {device.name}...")

            # Conectar
            self.ble_client = BleakClient(device.address)
            await self.ble_client.connect()

            if not self.ble_client.is_connected:
                print("🔵 Falló la conexión")
                return

            # Configurar características
            await self._setup_characteristics()

            self.ble_device = device
            self.ble_connected = True

            print("✅ mBot BLE conectado y configurado")

            # Mantener conexión activa
            while self.ble_connected and not self.exiting:
                await asyncio.sleep(0.1)

        except Exception as e:
            print(f"🔵 Error en conexión asíncrona: {e}")

    async def _find_mbot_ble(self):
        """Busca dispositivos mBot BLE"""
        try:
            devices = await BleakScanner.discover(timeout=10.0)

            for device in devices:
                name = device.name or ""
                if 'makeblock' in name.lower() or 'mbot' in name.lower():
                    print(f"🎯 Encontrado: {name} ({device.address})")
                    return device

            print("🔵 No se encontraron mBots específicos")
            return None

        except Exception as e:
            print(f"🔵 Error en escaneo: {e}")
            return None

    async def _setup_characteristics(self):
        """Configura características BLE"""
        try:
            services = self.ble_client.services

            # Características conocidas de Makeblock
            known_write_chars = [
                "0000ffe3-0000-1000-8000-00805f9b34fb",  # Común en Makeblock
                "0000fff2-0000-1000-8000-00805f9b34fb",  # Alternativa
                "00006487-3c17-d293-8e48-14fe2e4da212",  # Específica de algunos modelos
            ]

            # Buscar característica de escritura
            for service in services:
                for char in service.characteristics:
                    if "write" in char.properties:
                        self.ble_write_char = char.uuid
                        print(f"🔧 Característica de escritura: {char.uuid}")
                        break
                if self.ble_write_char:
                    break

            # Si no se encuentra, usar la conocida
            if not self.ble_write_char:
                self.ble_write_char = known_write_chars[0]
                print(f"🔧 Usando característica por defecto: {self.ble_write_char}")

        except Exception as e:
            print(f"🔧 Error configurando características: {e}")

    def _try_usb_connection(self):
        """Conecta por USB (igual que antes)"""
        try:
            print("🔌 Buscando mBot por USB...")
            port = self._find_mbot_usb_port()

            if not port:
                print("🔌 No se encontró puerto USB")
                return False

            print(f"🔌 Conectando a {port}...")
            self.serial = serial.Serial(port, 115200, timeout=1)
            self.connection_type = "usb"
            print(f"✅ Conectado por USB ({port})")
            sleep(2)
            return True

        except Exception as e:
            print(f"🔌 Error USB: {e}")
            return False

    def _find_mbot_usb_port(self):
        """Busca puerto USB del mBot"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if any(keyword in port.description.upper() for keyword in ["CH340", "CH341", "USB", "SILICON"]):
                return port.device
        return None

    def write(self, data):
        """Envía datos al mBot"""
        if not data:
            return False

        if self.connection_type == "usb" and self.serial:
            try:
                self.serial.write(data)
                return True
            except Exception as e:
                print(f"🔌 Error enviando por USB: {e}")
                return False

        elif self.connection_type == "bluetooth" and self.ble_connected:
            try:
                # Enviar de forma thread-safe
                future = asyncio.run_coroutine_threadsafe(
                    self._async_write(data),
                    self.ble_loop
                )
                return future.result(timeout=2.0)  # Timeout 2 segundos

            except Exception as e:
                print(f"🔵 Error enviando por BLE: {e}")
                return False
        else:
            print("🔌 No hay conexión activa")
            return False

    async def _async_write(self, data):
        """Escritura BLE asíncrona"""
        try:
            if self.ble_client and self.ble_client.is_connected and self.ble_write_char:
                await self.ble_client.write_gatt_char(self.ble_write_char, data)
                return True
            return False
        except Exception as e:
            print(f"🔵 Error en escritura async: {e}")
            return False

    def close(self):
        """Cierra la conexión"""
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

            if self.ble_thread and self.ble_thread.is_alive():
                self.ble_thread.join(timeout=2.0)

        elif self.connection_type == "usb" and self.serial:
            try:
                self.serial.close()
            except:
                pass

        print("🔌 Conexión cerrada")

    def exit(self, signal, frame):
        """Maneja Ctrl+C"""
        print("\n🛑 Cerrando...")
        self.close()
        sys.exit(0)

    # Métodos del mBot
    def doMove(self, leftSpeed, rightSpeed):
        """Mueve el robot"""
        # Convertir a signed byte si es necesario
        if leftSpeed < 0:
            leftSpeed = 256 + leftSpeed
        if rightSpeed < 0:
            rightSpeed = 256 + rightSpeed

        message = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 0xa, leftSpeed & 0xFF, rightSpeed & 0xFF])
        return self.write(message)

    def doRGBLedOnBoard(self, index, red, green, blue):
        """Controla LED RGB de la placa"""
        message = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, index, red, green, blue])
        return self.write(message)

    def doBuzzer(self, frequency, duration):
        """Hace sonar el buzzer"""
        # Convertir frecuencia a bytes
        freq_high = (frequency >> 8) & 0xFF
        freq_low = frequency & 0xFF
        dur_high = (duration >> 8) & 0xFF
        dur_low = duration & 0xFF

        message = bytes([0xff, 0x55, 0x8, 0x0, 0x2, 0x22, freq_high, freq_low, dur_high, dur_low])
        return self.write(message)

    def doMotor(self, port, speed):
        """Controla un motor específico"""
        if speed < 0:
            speed = 256 + speed
        message = bytes([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, port, speed & 0xFF])
        return self.write(message)

    def doRGBLed(self, port, slot, index, red, green, blue):
        """Controla LEDs RGB"""
        message = bytes([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, port, slot, index, red, green, blue])
        return self.write(message)

    def doServo(self, port, slot, angle):
        """Controla servo motor"""
        message = bytes([0xff, 0x55, 0x6, 0x0, 0x2, 0xb, port, slot, angle])
        return self.write(message)

def test_mbot_ble():
    """Test del mBot BLE"""
    print("🤖 PROBANDO MBOT BLE")
    print("=" * 40)

    try:
        # ¡IMPORTANTE! Asegúrate de que el cable USB esté desconectado
        print("⚠️  ASEGÚRATE DE QUE EL CABLE USB ESTÉ DESCONECTADO")
        print("⚠️  Y QUE EL MBOT ESTÉ ENCENDIDO")
        print()
        input("Presiona Enter para continuar...")

        # Conectar (intentará BLE primero, luego USB)
        mbot = MBotBLE(connection_type="bluetooth")  # Forzar BLE

        print(f"\n✅ Conectado por: {mbot.connection_type}")

        if mbot.connection_type == "bluetooth":
            print("🎉 ¡CONEXIÓN BLUETOOTH EXITOSA!")

            # Pruebas
            print("\n🔴 LED rojo...")
            mbot.doRGBLedOnBoard(0, 255, 0, 0)
            sleep(1)

            print("🟢 LED verde...")
            mbot.doRGBLedOnBoard(0, 0, 255, 0)
            sleep(1)

            print("🔵 LED azul...")
            mbot.doRGBLedOnBoard(0, 0, 0, 255)
            sleep(1)

            print("🎵 Buzzer...")
            mbot.doBuzzer(440, 500)  # La 440Hz por 500ms
            sleep(1)

            print("⬆️ Movimiento adelante...")
            mbot.doMove(100, 100)
            sleep(1)

            print("⬇️ Movimiento atrás...")
            mbot.doMove(-100, -100)
            sleep(1)

            print("🛑 Parar...")
            mbot.doMove(0, 0)

            print("✅ ¡TODAS LAS PRUEBAS COMPLETADAS!")

        mbot.close()

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_mbot_ble()
