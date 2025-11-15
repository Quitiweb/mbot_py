"""Controlador reducido del mBot para los nuevos modos autónomos."""

import random
import time
from typing import Dict, Optional

from ..protocols.mbot_original_protocol import MBotOriginalProtocol
from config import (
    MBOT_CONNECTION_TYPE,
    SENSOR_PORTS,
    SOUND_LIBRARY,
)


class _SimulatedMBot:
    """Implementación muy básica para depurar sin hardware real."""

    def __init__(self):
        self.connection_type = "simulation"

    def doMove(self, left_speed: int, right_speed: int):
        print(f"[SIM] Move L:{left_speed} R:{right_speed}")

    def doRGBLedOnBoard(self, index: int, red: int, green: int, blue: int):
        print(f"[SIM] LED{index} -> ({red}, {green}, {blue})")

    def doBuzzer(self, frequency: int, duration: int = 0):
        print(f"[SIM] Buzzer {frequency}Hz durante {duration}ms")

    def close(self):
        print("[SIM] Cerrar controlador")


class MBotController:
    """Controlador simplificado con utilidades para mover y leer sensores."""

    def __init__(self, connection_type: str = MBOT_CONNECTION_TYPE):
        self.connection_type = connection_type
        self.is_simulation = False
        self.sensor_ports: Dict[str, Optional[Dict[str, int]]] = SENSOR_PORTS
        self._last_distance_cache: Dict[str, float] = {}
        self._last_distance_timestamp: Dict[str, float] = {}
        self._sound_index = 0

        try:
            print(f"🔗 Intentando conectar mBot ({connection_type})...")
            self.mbot = MBotOriginalProtocol(connection_type)
            print(f"✅ mBot conectado via {self.mbot.connection_type}")
        except Exception as exc:  # pragma: no cover - hardware fallback
            print(f"❌ No se pudo conectar al mBot: {exc}")
            print("💡 Usando modo simulación.")
            self.mbot = _SimulatedMBot()
            self.is_simulation = True

    # ------------------------------------------------------------------
    # Movimientos básicos
    # ------------------------------------------------------------------
    def drive(self, left_speed: int, right_speed: int):
        self.mbot.doMove(left_speed, right_speed)

    def drive_forward(self, speed: int):
        self.drive(speed, speed)

    def drive_backward(self, speed: int):
        self.drive(-speed, -speed)

    def turn_left(self, speed: int):
        self.drive(-speed, speed)

    def turn_right(self, speed: int):
        self.drive(speed, -speed)

    def stop(self):
        self.drive(0, 0)

    # ------------------------------------------------------------------
    # Sensores
    # ------------------------------------------------------------------
    def read_distance(self, sensor: str = "front", freshness: float = 0.2) -> Optional[float]:
        """Lee la distancia en cm para el sensor dado."""

        port_config = self.sensor_ports.get(sensor)
        if not port_config:
            return None

        now = time.time()
        if (
            sensor in self._last_distance_timestamp
            and now - self._last_distance_timestamp[sensor] < freshness
        ):
            return self._last_distance_cache.get(sensor)

        reader = getattr(self.mbot, "get_ultrasonic_distance", None)
        if not reader:
            return None

        try:
            distance = reader(port_config["port"], port_config["slot"])
        except NotImplementedError:
            distance = None

        if distance is not None:
            self._last_distance_cache[sensor] = distance
            self._last_distance_timestamp[sensor] = now
        return distance

    # ------------------------------------------------------------------
    # Sonidos
    # ------------------------------------------------------------------
    def play_sound_sequence(self, sequence):
        for frequency, duration in sequence:
            self.mbot.doBuzzer(int(frequency), int(duration))
            time.sleep(duration / 1000.0)

    def play_random_sound(self):
        if not SOUND_LIBRARY:
            return
        sequence = random.choice(SOUND_LIBRARY)
        self.play_sound_sequence(sequence)

    # ------------------------------------------------------------------
    # Acciones especiales
    # ------------------------------------------------------------------
    def perform_dance(self):
        """Un mini baile reutilizable por el comando 'bailar'."""
        print("💃 Iniciando mini baile...")
        steps = [
            (80, -80, 0.5),
            (-80, 80, 0.5),
            (90, 90, 0.4),
            (-70, -70, 0.3),
        ]
        for left, right, duration in steps:
            self.drive(left, right)
            self.mbot.doRGBLedOnBoard(0, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.mbot.doRGBLedOnBoard(1, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            time.sleep(duration)
        self.stop()
        self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
        self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
        self.play_random_sound()

    def flash_leds(self, color=(0, 255, 0), duration=0.3):
        self.mbot.doRGBLedOnBoard(0, *color)
        self.mbot.doRGBLedOnBoard(1, *color)
        time.sleep(duration)
        self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
        self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

    # ------------------------------------------------------------------
    def shutdown(self):
        self.stop()
        if hasattr(self.mbot, "close"):
            self.mbot.close()


if __name__ == "__main__":  # pragma: no cover - comprobación manual
    controller = MBotController()
    controller.drive_forward(60)
    time.sleep(1)
    controller.stop()
    print("Distancia frontal:", controller.read_distance("front"))
    controller.perform_dance()
    controller.shutdown()
