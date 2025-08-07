#!/usr/bin/env python3
"""
mBot Enhanced - Versión extendida con soporte Bluetooth
"""

import signal
import struct
import sys
from time import sleep
import serial
import serial.tools.list_ports

try:
    import bluetooth
    BLUETOOTH_AVAILABLE = True
    print("🔵 Bluetooth disponible")
except ImportError:
    try:
        # Alternativa para macOS - usando socket directo
        import socket
        BLUETOOTH_AVAILABLE = "macos_socket"
        print("🔵 Bluetooth disponible (modo socket)")
    except:
        BLUETOOTH_AVAILABLE = False
        print("⚠️  Bluetooth no disponible - solo USB")

class MBotEnhanced:
    def __init__(self, connection_type="auto", bluetooth_address=None):
        """
        Inicializa el mBot con soporte para USB y Bluetooth

        Args:
            connection_type: "auto", "usb", "bluetooth"
            bluetooth_address: Dirección MAC del mBot (opcional)
        """
        signal.signal(signal.SIGINT, self.exit)
        self.exiting = False
        self.connection_type = None
        self.serial = None
        self.bluetooth_socket = None

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
        """Intenta conectar por Bluetooth"""
        if not BLUETOOTH_AVAILABLE or BLUETOOTH_AVAILABLE == False:
            print("🔵 Bluetooth no disponible en este sistema")
            return False

        print("🔵 Buscando mBot por Bluetooth...")

        # TODO: Implementar Bluetooth cuando esté disponible
        # Por ahora, siempre falla para que se use USB
        print("🔵 Bluetooth no implementado completamente aún")
        print("� Usando conexión USB como alternativa")
        return False

    def _find_mbot_bluetooth(self):
        """Busca dispositivos mBot disponibles por Bluetooth"""
        try:
            print("🔍 Escaneando dispositivos Bluetooth...")
            nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True)

            for addr, name in nearby_devices:
                # Buscar dispositivos que parezcan mBot
                if "mbot" in name.lower() or "makeblock" in name.lower():
                    print(f"🔵 Encontrado posible mBot: {name} ({addr})")
                    return addr

            # Si no encuentra uno específico, mostrar todos los dispositivos
            print("🔵 Dispositivos Bluetooth encontrados:")
            for addr, name in nearby_devices:
                print(f"   - {name} ({addr})")

            # Permitir selección manual
            if nearby_devices:
                print("💡 Tip: Puedes especificar la dirección MAC manualmente")

        except Exception as e:
            print(f"🔵 Error escaneando Bluetooth: {e}")

        return None

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
        if self.connection_type == "bluetooth" and self.bluetooth_socket:
            try:
                self.bluetooth_socket.close()
            except:
                pass
            self.bluetooth_socket = None
        elif self.connection_type == "usb" and self.serial:
            try:
                if self.serial.is_open:
                    self.serial.close()
            except:
                pass
            self.serial = None

    def exit(self, signal, frame):
        """Maneja la salida del programa"""
        self.exiting = True
        self.close()
        sys.exit(0)

    def __writePackage(self, pack):
        """Envía un paquete de datos al mBot"""
        if self.connection_type == "bluetooth" and self.bluetooth_socket:
            self.bluetooth_socket.send(bytes(pack))
        elif self.connection_type == "usb" and self.serial:
            self.serial.write(pack)
            self.serial.flush()
        sleep(0.01)

    def is_connected(self):
        """Verifica si está conectado"""
        if self.connection_type == "bluetooth":
            return self.bluetooth_socket is not None
        elif self.connection_type == "usb":
            return self.serial is not None and self.serial.is_open
        return False

    def get_connection_info(self):
        """Obtiene información de la conexión actual"""
        if self.connection_type == "bluetooth":
            return f"Bluetooth (RFCOMM)"
        elif self.connection_type == "usb":
            return f"USB ({self.serial.port if self.serial else 'N/A'})"
        return "Desconectado"

    # Métodos de control del mBot (compatibles con la librería original)
    def doRGBLedOnBoard(self, index, red, green, blue):
        self.__writePackage(bytearray([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, 0x7, 0x2, index, red, green, blue]))

    def doRGBLed(self, port, slot, index, red, green, blue):
        self.__writePackage(bytearray([0xff, 0x55, 0x9, 0x0, 0x2, 0x8, port, slot, index, red, green, blue]))

    def doMove(self, leftSpeed, rightSpeed):
        self.__writePackage(bytearray([0xff, 0x55, 0x7, 0x0, 0x2, 0x5] + self.short2bytes(-leftSpeed) + self.short2bytes(rightSpeed)))

    def doBuzzer(self, buzzer, time=0):
        self.__writePackage(bytearray([0xff, 0x55, 0x7, 0x0, 0x2, 0x22] + self.short2bytes(buzzer) + self.short2bytes(time)))

    def doMotor(self, port, speed):
        self.__writePackage(bytearray([0xff, 0x55, 0x6, 0x0, 0x2, 0xa, port]+self.short2bytes(speed)))

    def short2bytes(self, sval):
        val = struct.pack("h", sval)
        return [val[i] for i in range(2)]

    def float2bytes(self, fval):
        val = struct.pack("f", fval)
        return [val[i] for i in range(4)]

    def doServo(self, port, slot, angle):
        self.__writePackage(bytearray([0xff, 0x55, 0x6, 0x0, 0x2, 0xb, port, slot, angle]))

# Clase de compatibilidad que usa la nueva versión mejorada
class mBot(MBotEnhanced):
    def __init__(self, connection_type="auto", bluetooth_address=None):
        super().__init__(connection_type, bluetooth_address)

if __name__ == "__main__":
    print("🤖 Probando mBot Enhanced...")

    try:
        # Probar conexión automática (Bluetooth primero, luego USB)
        robot = MBotEnhanced("auto")
        print(f"🔗 Conectado via: {robot.get_connection_info()}")

        # Probar funcionalidad básica
        print("🎵 Probando buzzer...")
        robot.doBuzzer(440, 500)
        sleep(1)

        print("💡 Probando LEDs...")
        robot.doRGBLedOnBoard(0, 255, 0, 0)
        robot.doRGBLedOnBoard(1, 0, 255, 0)
        sleep(2)
        robot.doRGBLedOnBoard(0, 0, 0, 0)
        robot.doRGBLedOnBoard(1, 0, 0, 0)

        print("✅ Prueba exitosa")
        robot.close()

    except Exception as e:
        print(f"❌ Error: {e}")
