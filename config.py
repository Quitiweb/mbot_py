# Configuración mínima para el nuevo flujo del mBot

# Conexión
MBOT_CONNECTION_TYPE = "usb"  # "usb" o "bluetooth" (usb recomendado para simplificar)
MBOT_BLUETOOTH_ADDRESS = None
MBOT_PORT = None
MBOT_BAUDRATE = 115200

# Sensores ultrasónicos (puedes ajustar puertos/slots según tu cableado)
SENSOR_PORTS = {
    "front": {"port": 1, "slot": 3},
    "left": None,
    "right": None,
}

# Exploración constante estilo Roomba
EXPLORATION_SETTINGS = {
    "forward_speed": 90,
    "turn_speed": 80,
    "reverse_time": 0.4,
    "turn_time": 0.7,
    "obstacle_distance_cm": 25.0,
    "sound_every_seconds": 8.0,
}

# Parámetros del modo seguir
FOLLOW_SETTINGS = {
    "min_distance_cm": 15.0,
    "max_distance_cm": 45.0,
    "forward_speed": 75,
    "turn_speed": 70,
    "distance_tolerance_cm": 3.0,
}

# Biblioteca de sonidos simpáticos (frecuencia Hz, duración ms)
SOUND_LIBRARY = [
    [(523, 180), (659, 180), (784, 250)],
    [(784, 140), (659, 140), (523, 200)],
    [(659, 120), (784, 120), (988, 200)],
    [(392, 160), (523, 220)],
]

# Escucha por voz (muy simplificada)
VOICE_ENABLED = True
WAKE_WORD = "eme bot"
VOICE_LANGUAGE = "es-ES"
WAKE_POLL_INTERVAL = 4.0   # segundos entre intentos de detectar el wake word
COMMAND_TIMEOUT = 4.0      # segundos máximos para escuchar la orden tras despertar

# Debug sencillo
DEBUG_MODE = True
