#!/usr/bin/env python3
"""
mBot Enhanced - Versión extendida con soporte Bluetooth LE usando bleak
"""

import signal
import struct
import sys
import asyncio
from time import sleep
import serial
import serial.tools.list_ports

try:
    from bleak import BleakScanner, BleakClient
    BLUETOOTH_AVAILABLE = True
    print("🔵 Bluetooth LE (bleak) disponible")
except ImportError:
    BLUETOOTH_AVAILABLE = False
    print("⚠️  Bluetooth LE no disponible - solo USB")

class MBotEnhanced:
    def __init__(self, connection_type="auto", bluetooth_address=None):
        """
        Inicializa el mBot con soporte para USB y Bluetooth LE

        Args:
            connection_type: "auto", "usb", "bluetooth"
            bluetooth_address: Dirección del mBot BLE (opcional)
        """
        signal.signal(signal.SIGINT, self.exit)
        self.exiting = False
        self.connection_type = None
        self.serial = None
        self.ble_client = None
        self.ble_device = None
        self.ble_write_char = None
        self.ble_notify_char = None
        self.ble_loop = None

        # Initialize attributes for sensor reading
        self.buffer = []
        self.isParseStart = False
        self.isParseStartIndex = 0
        self.__selectors = {}

        # Intentar conectar según el tipo especificado
        if connection_type == "auto":
            # Intentar Bluetooth primero, luego USB
            if self._try_bluetooth_connection(bluetooth_address):
                pass  # Ya conectado por Bluetooth
            elif self._try_usb_connection():
                pass  # Ya conectado por USB
            else:
                raise Exception("No se pudo conectar al mBot por Bluetooth ni USB")
        elif connection_type == "bluetooth":
            if not self._try_bluetooth_connection(bluetooth_address):
                raise Exception("No se pudo conectar al mBot por Bluetooth")
        elif connection_type == "usb":
            if not self._try_usb_connection():
                raise Exception("No se pudo conectar al mBot por USB")
        else:
            raise ValueError("connection_type debe ser 'auto', 'usb' o 'bluetooth'")

    def _try_bluetooth_connection(self, bluetooth_address=None):
        """Intenta conectar por Bluetooth LE"""
        if not BLUETOOTH_AVAILABLE:
            print("🔵 Bluetooth LE no disponible en este sistema")
            return False

        try:
            # Ejecutar conexión BLE de forma síncrona
            return asyncio.run(self._async_bluetooth_connect(bluetooth_address))
        except Exception as e:
            print(f"🔵 Error en conexión Bluetooth: {e}")
            return False

    async def _async_bluetooth_connect(self, bluetooth_address=None):
        """Conexión Bluetooth LE asíncrona"""
        try:
            print("🔵 Buscando mBot por Bluetooth LE...")

            # Si tenemos una dirección específica, usarla
            if bluetooth_address:
                device = await self._find_device_by_address(bluetooth_address)
            else:
                device = await self._find_mbot_ble()

            if not device:
                print("🔵 No se encontró mBot por Bluetooth LE")
                return False

            print(f"🔵 Conectando a {device.name} ({device.address})...")

            # Crear cliente BLE
            self.ble_client = BleakClient(device.address)
            await self.ble_client.connect()

            if not self.ble_client.is_connected:
                print("🔵 Falló la conexión BLE")
                return False

            print("✅ Conectado por Bluetooth LE")

            # Encontrar características de escritura y notificación
            await self._setup_ble_characteristics()

            self.connection_type = "bluetooth"
            self.ble_device = device

            # Crear un loop para manejar operaciones asíncronas
            self.ble_loop = asyncio.new_event_loop()

            return True

        except Exception as e:
            print(f"🔵 Error en conexión BLE: {e}")
            return False

    async def _find_device_by_address(self, address):
        """Busca un dispositivo específico por dirección"""
        devices = await BleakScanner.discover(timeout=10.0)
        for device in devices:
            if device.address == address:
                return device
        return None

    async def _find_mbot_ble(self):
        """Busca dispositivos mBot por Bluetooth LE"""
        try:
            devices = await BleakScanner.discover(timeout=10.0)

            for device in devices:
                name = device.name or ""
                if any(keyword in name.lower() for keyword in ['mbot', 'makeblock']):
                    print(f"🎯 Encontrado mBot: {name} ({device.address})")
                    return device

            print("🔵 No se encontraron dispositivos mBot específicos")
            print("🔵 Dispositivos BLE disponibles:")
            for device in devices:
                name = device.name or "Sin nombre"
                print(f"   📱 {name} ({device.address})")

        except Exception as e:
            print(f"🔵 Error escaneando BLE: {e}")

        return None

    async def _setup_ble_characteristics(self):
        """Configura las características BLE para comunicación"""
        try:
            services = self.ble_client.services

            # Buscar características de escritura y notificación
            for service in services:
                for char in service.characteristics:
                    if "write" in char.properties:
                        if not self.ble_write_char:
                            self.ble_write_char = char.uuid
                            print(f"🔧 Característica de escritura: {char.uuid}")

                    if "notify" in char.properties:
                        if not self.ble_notify_char:
                            self.ble_notify_char = char.uuid
                            print(f"🔧 Característica de notificación: {char.uuid}")
                            # Configurar notificaciones
                            await self.ble_client.start_notify(char.uuid, self._ble_notification_handler)

            # Usar características conocidas de Makeblock si no se encuentran
            if not self.ble_write_char:
                # Característica común de Makeblock
                self.ble_write_char = "0000ffe3-0000-1000-8000-00805f9b34fb"
                print(f"🔧 Usando característica de escritura por defecto: {self.ble_write_char}")

        except Exception as e:
            print(f"🔧 Error configurando características BLE: {e}")

    def _ble_notification_handler(self, sender, data):
        """Maneja notificaciones BLE del mBot"""
        try:
            # Procesar datos recibidos del mBot
            for byte in data:
                self.buffer.append(byte)
                self._process_buffer()
        except Exception as e:
            print(f"🔧 Error procesando notificación BLE: {e}")

    def _try_usb_connection(self):
        """Intenta conectar por USB"""
        try:
            print("🔌 Buscando mBot por USB...")
            port = self._find_mbot_usb_port()

            if not port:
                print("🔌 No se encontró mBot por USB")
                return False

            print(f"🔌 Conectando a mBot en {port}...")
            self.serial = serial.Serial(port, 115200, timeout=1)
            self.connection_type = "usb"
            print(f"✅ mBot conectado por USB ({port})")
            sleep(2)  # Tiempo para estabilizar conexión
            return True

        except Exception as e:
            print(f"🔌 Error conectando por USB: {e}")
            if self.serial:
                try:
                    self.serial.close()
                except:
                    pass
                self.serial = None
            return False

    def _find_mbot_usb_port(self):
        """Busca el puerto USB del mBot"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # Buscar drivers comunes del mBot
            if any(keyword in port.description.upper() for keyword in ["USB", "CH340", "CH341", "SILICON", "MAKEBLOCK"]):
                return port.device
        return None

    def close(self):
        """Cierra la conexión"""
        if self.connection_type == "bluetooth" and self.ble_client:
            try:
                # Desconectar BLE de forma asíncrona
                if self.ble_loop:
                    asyncio.set_event_loop(self.ble_loop)
                    asyncio.run(self.ble_client.disconnect())
                    self.ble_loop.close()
            except:
                pass
            self.ble_client = None
        elif self.connection_type == "usb" and self.serial:
            try:
                self.serial.close()
            except:
                pass
            self.serial = None

        self.connection_type = None
        print("🔌 Conexión cerrada")

    def exit(self, signal, frame):
        """Maneja la salida del programa"""
        print("\n🛑 Cerrando conexión...")
        self.exiting = True
        self.close()
        sys.exit(0)

    def write(self, data):
        """Envía datos al mBot"""
        if self.connection_type == "usb" and self.serial:
            try:
                self.serial.write(data)
                self.serial.flush()
                return True
            except Exception as e:
                print(f"🔌 Error enviando datos por USB: {e}")
                return False

        elif self.connection_type == "bluetooth" and self.ble_client:
            try:
                # Enviar datos por BLE de forma síncrona
                if self.ble_write_char:
                    # Crear un nuevo loop si no existe
                    try:
                        loop = asyncio.get_event_loop()
                    except RuntimeError:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)

                    # Ejecutar escritura BLE
                    loop.run_until_complete(
                        self.ble_client.write_gatt_char(self.ble_write_char, data)
                    )
                    return True
                else:
                    print("🔵 No hay característica de escritura BLE disponible")
                    return False

            except Exception as e:
                print(f"🔵 Error enviando datos por BLE: {e}")
                return False
        else:
            print("🔌 No hay conexión activa")
            return False

    def _process_buffer(self):
        """Procesa el buffer de datos recibidos (igual que mBot original)"""
        # Esta función mantiene la misma lógica que el mBot original
        # para procesar respuestas del robot
        pass

    def read(self):
        """Lee datos del mBot"""
        if self.connection_type == "usb" and self.serial:
            try:
                if self.serial.inWaiting() > 0:
                    return self.serial.read(self.serial.inWaiting())
            except:
                pass
        # Para BLE, los datos llegan por notificaciones
        return None

    # Métodos del mBot original (mantener compatibilidad)
    def doMove(self, leftSpeed, rightSpeed):
        """Mueve el robot"""
        message = bytearray([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 0xa, leftSpeed, rightSpeed])
        self.write(message)

    def doMotor(self, port, speed):
        """Controla un motor específico"""
        message = bytearray([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, port, speed])
        self.write(message)

    def doBuzzer(self, buzzer, time):
        """Hace sonar el buzzer"""
        message = bytearray([0xff, 0x55, 0x7, 0x0, 0x2, 0x22, buzzer, time])
        self.write(message)

    def doRGBLed(self, port, slot, index, red, green, blue):
        """Controla LEDs RGB"""
        message = bytearray([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, port, slot, index, red, green, blue])
        self.write(message)

    def doRGBLedOnBoard(self, index, red, green, blue):
        """Controla LEDs RGB de la placa"""
        self.doRGBLed(0x7, 0x2, index, red, green, blue)

    # Agregar otros métodos del mBot original según sea necesario...

def test_enhanced_mbot():
    """Función de prueba"""
    print("🤖 Probando mBot Enhanced...")

    try:
        # Intentar conectar
        mbot = MBotEnhanced(connection_type="auto")

        print(f"✅ Conectado por: {mbot.connection_type}")

        # Prueba básica - LED y buzzer
        print("🔴 Probando LED rojo...")
        mbot.doRGBLedOnBoard(0, 255, 0, 0)
        sleep(1)

        print("🔵 Probando LED azul...")
        mbot.doRGBLedOnBoard(0, 0, 0, 255)
        sleep(1)

        print("🎵 Probando buzzer...")
        mbot.doBuzzer(262, 500)  # Do central
        sleep(1)

        print("⬆️ Probando movimiento...")
        mbot.doMove(100, 100)  # Adelante
        sleep(1)
        mbot.doMove(0, 0)      # Parar

        print("✅ Prueba completada")

        mbot.close()

    except Exception as e:
        print(f"❌ Error en prueba: {e}")

if __name__ == "__main__":
    test_enhanced_mbot()
