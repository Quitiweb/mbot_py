# Configuración del Asistente mBot
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "tu-api-key-aqui")

# Ollama Configuration (IA Local)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL_NAME = "qwen2.5:7b"
AI_BACKEND = "ollama"  # "openai" o "ollama"

# Audio Configuration
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
AUDIO_FORMAT = 16  # 16-bit
CHANNELS = 1  # Mono

# TTS Configuration
TTS_ENGINE = "pyttsx3"  # o "edge-tts"
TTS_VOICE_RATE = 180  # Velocidad de habla
TTS_VOICE_VOLUME = 0.8  # Volumen (0.0 a 1.0)
TTS_PREFERRED_VOICE = "Monica"  # Voz preferida (Mónica - español España)
TTS_VOICE_ID = 97  # ID específico de la voz Mónica

# mBot Configuration
MBOT_PORT = None  # None para auto-detectar
MBOT_BAUDRATE = 115200

# AI Personality
ROBOT_NAME = "mBot"
ROBOT_PERSONALITY = """
Eres un robot amigable llamado mBot. Tienes una personalidad curiosa, juguetona y útil.
Te gusta moverte, hacer sonidos y encender tus luces LED para expresarte.
Respondes de forma concisa pero amigable. Cuando te emocionas, lo expresas con movimiento.
Puedes seguir órdenes como moverse hacia adelante, atrás, girar, etc.
Siempre mantén un tono positivo y robot-like pero cálido.
"""

# Gesture System
GESTURES = {
    "happy": {"movement": "bounce", "leds": "rainbow", "sound": "beep_happy"},
    "excited": {"movement": "spin", "leds": "flash_multicolor", "sound": "beep_fast"},
    "thinking": {"movement": "gentle_sway", "leds": "blue_pulse", "sound": "beep_low"},
    "confused": {"movement": "head_shake", "leds": "yellow_blink", "sound": "beep_confused"},
    "sad": {"movement": "back_away", "leds": "red_dim", "sound": "beep_sad"},
    "neutral": {"movement": "slight_move", "leds": "white_steady", "sound": None},
    "listening": {"movement": "stop", "leds": "blue_breathing", "sound": None}
}

# Voice Commands
DIRECT_COMMANDS = {
    "adelante": "forward",
    "atrás": "backward",
    "derecha": "right",
    "izquierda": "left",
    "para": "stop",
    "detente": "stop",
    "gira": "spin",
    "baila": "dance",
    "luz": "light_show"
}

# Debug
DEBUG_MODE = True
LOG_AUDIO = False
