"""Plantilla mínima para configurar el mBot simplificado.

Copia este archivo como `config.py` y ajusta los valores para tu robot.
"""

MBOT_CONNECTION_TYPE = "usb"  # "usb" o "ble"
MBOT_BLUETOOTH_ADDRESS = None  # Requerido solo si usas BLE
MBOT_PORT = None               # Usa algo como "/dev/tty.usbmodemXXXX" si deseas fijarlo
MBOT_BAUDRATE = 115200

SENSOR_PORTS = {
    "front": {"port": 1, "slot": 3},  # Sensor ultrasónico frontal
    "left": None,
    "right": None,
}

EXPLORATION_SETTINGS = {
    "forward_speed": 90,
    "turn_speed": 80,
    "reverse_time": 0.4,
    "turn_time": 0.7,
    "obstacle_distance_cm": 25.0,
    "sound_every_seconds": 8.0,
}

FOLLOW_SETTINGS = {
    "min_distance_cm": 15.0,
    "max_distance_cm": 45.0,
    "forward_speed": 75,
    "turn_speed": 70,
    "distance_tolerance_cm": 3.0,
}

SOUND_LIBRARY = [
    [(523, 180), (659, 180), (784, 250)],
    [(784, 140), (659, 140), (523, 200)],
    [(659, 120), (784, 120), (988, 200)],
    [(392, 160), (523, 220)],
]

VOICE_ENABLED = True
WAKE_WORD = "eme bot"
VOICE_LANGUAGE = "es-ES"
WAKE_POLL_INTERVAL = 4.0
COMMAND_TIMEOUT = 4.0

DEBUG_MODE = True
