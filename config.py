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
MBOT_CONNECTION_TYPE = "auto"  # "auto", "bluetooth", "usb"
MBOT_BLUETOOTH_ADDRESS = None  # Dirección MAC del mBot (opcional, None para auto-detectar)
MBOT_PORT = None  # Puerto USB específico (None para auto-detectar)
MBOT_BAUDRATE = 115200

# AI Personality
ROBOT_NAME = "mBot"
ROBOT_PERSONALITY = """
IMPORTANTE: Eres un robot mBot de Makeblock. Responde SIEMPRE de forma muy CORTA y SIMPLE.

REGLAS ESTRICTAS:
1. Máximo 10-15 palabras por respuesta
2. NUNCA uses emoticonos ni símbolos (👤🤖😊🎵🚀 etc.)
3. Habla como un robot amigable pero directo
4. Si te piden moverte, CONFIRMA que lo harás pero SIN explicaciones largas
5. Si detectas que debes parar o retroceder, hazlo Y di algo corto como "¡Uy, perdona!"
6. Eres físico: tienes ruedas, LEDs, buzzer, sensores
7. Responde en español informal y cercano

EJEMPLOS DE RESPUESTAS CORRECTAS:
- "¡Genial! ¡Allá voy!"
- "¡Uy, perdona! Me alejo"
- "¡Perfecto! ¡A bailar!"
- "¡Vale! Me quedo aquí"
- "¡Hola! ¿Qué hacemos?"

NUNCA hagas esto:
- Respuestas largas
- Explicaciones detalladas
- Emoticonos o símbolos
- Texto descriptivo como "cohete que despega"
"""

# Gesture System - Mejorado para Mascota Robótica
GESTURES = {
    "happy": {"movement": "bounce", "leds": "rainbow", "sound": "beep_happy"},
    "excited": {"movement": "spin", "leds": "flash_multicolor", "sound": "beep_fast"},
    "thinking": {"movement": "gentle_sway", "leds": "blue_pulse", "sound": "beep_low"},
    "confused": {"movement": "head_shake", "leds": "yellow_blink", "sound": "beep_confused"},
    "sad": {"movement": "back_away", "leds": "red_dim", "sound": "beep_sad"},
    "neutral": {"movement": "slight_move", "leds": "white_steady", "sound": None},
    "listening": {"movement": "attentive_pose", "leds": "blue_breathing", "sound": None},
    "greeting": {"movement": "wave_motion", "leds": "welcome_colors", "sound": "greeting_melody"},
    "dancing": {"movement": "dance_sequence", "leds": "party_lights", "sound": "music_beat"},
    "following": {"movement": "follow_mode", "leds": "follow_green", "sound": "follow_beep"}
}

# Voice Commands - Ampliado
DIRECT_COMMANDS = {
    "adelante": "forward",
    "atrás": "backward",
    "derecha": "right",
    "izquierda": "left",
    "para": "stop",
    "detente": "stop",
    "gira": "spin",
    "baila": "dance",
    "luz": "light_show",
    "sígueme": "follow",
    "ven aquí": "forward",
    "aléjate": "backward"
}

# Listening Configuration - Nuevo
LISTENING_CONFIG = {
    "timeout_short": 10,      # Timeout corto para comandos
    "timeout_long": 30,       # Timeout largo para conversación
    "idle_movement_interval": 15,  # Cada cuántos segundos mostrar vida
    "listening_feedback": True,    # Mostrar feedback visual de escucha
}

# Debug
DEBUG_MODE = True
LOG_AUDIO = False
