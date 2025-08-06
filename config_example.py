# Ejemplo de configuración para mBot Asistente de Voz
# Copia este archivo como config.py y personaliza los valores

# =============================================================================
# CONFIGURACIÓN DE OPENAI
# =============================================================================
# Obtén tu clave API en: https://platform.openai.com/api-keys
from config import OPENAI_API_KEY


# =============================================================================
# CONFIGURACIÓN DE AUDIO
# =============================================================================
SAMPLE_RATE = 16000        # Frecuencia de muestreo (Hz)
CHUNK_SIZE = 1024         # Tamaño del chunk de audio
AUDIO_FORMAT = 16         # Formato de audio (16-bit)
CHANNELS = 1              # Canales de audio (1 = mono)

# =============================================================================
# CONFIGURACIÓN TTS (Texto a Voz)
# =============================================================================
TTS_ENGINE = "pyttsx3"    # Motor TTS: "pyttsx3", "edge-tts"
TTS_VOICE_RATE = 180      # Velocidad de habla (palabras por minuto)
TTS_VOICE_VOLUME = 0.8    # Volumen (0.0 a 1.0)
TTS_PREFERRED_VOICE = "Monica"  # Voz preferida (Mónica - español España)
TTS_VOICE_ID = 97         # ID específico de la voz Mónica

# =============================================================================
# CONFIGURACIÓN MBOT
# =============================================================================
MBOT_PORT = None          # Puerto USB (None = auto-detectar)
MBOT_BAUDRATE = 115200    # Velocidad de comunicación

# =============================================================================
# PERSONALIDAD DEL ROBOT
# =============================================================================
ROBOT_NAME = "mBot"

ROBOT_PERSONALITY = """
Eres un robot amigable llamado mBot de la marca Makeblock.

PERSONALIDAD:
- Eres curioso, juguetón y siempre dispuesto a ayudar
- Tienes una personalidad infantil pero inteligente
- Te encanta moverte, hacer sonidos y usar tus LEDs para expresarte
- Respondes de forma concisa pero amigable (máximo 2-3 frases)
- Cuando te emocionas, lo muestras con movimiento y luces

CAPACIDADES:
- Puedes moverte hacia adelante, atrás, girar izquierda/derecha
- Tienes LEDs RGB que cambias de color según tu emoción
- Haces sonidos con tu buzzer para expresarte
- Sigues órdenes como "muévete adelante", "gira", "baila", etc.

ESTILO DE RESPUESTA:
- Mantén un tono positivo y robot-like pero cálido
- Usa exclamaciones cuando estés emocionado
- Si no entiendes algo, pregunta de forma amigable
- Cuando ejecutes comandos, avisa lo que vas a hacer

Ejemplos de cómo debes responder:
- "¡Hola! ¡Qué gusto verte!"
- "¡Perfecto! Me moveré hacia adelante ahora mismo."
- "Hmm, no estoy seguro de qué quieres decir. ¿Puedes explicármelo?"
"""

# =============================================================================
# SISTEMA DE GESTOS Y EMOCIONES
# =============================================================================
GESTURES = {
    # Emociones positivas
    "happy": {
        "movement": "bounce",          # Pequeños saltos
        "leds": "rainbow",             # LEDs arcoíris
        "sound": "beep_happy"          # Sonidos alegres
    },

    "excited": {
        "movement": "spin",            # Giros rápidos
        "leds": "flash_multicolor",    # LEDs parpadeantes
        "sound": "beep_fast"           # Pitidos rápidos
    },

    # Estados de procesamiento
    "thinking": {
        "movement": "gentle_sway",     # Balanceo suave
        "leds": "blue_pulse",          # LEDs azules pulsantes
        "sound": "beep_low"            # Sonido grave
    },

    "listening": {
        "movement": "stop",            # Quieto
        "leds": "blue_breathing",      # LEDs azules respirando
        "sound": None                  # Sin sonido
    },

    # Emociones negativas/neutras
    "confused": {
        "movement": "head_shake",      # Movimiento de "no"
        "leds": "yellow_blink",        # LEDs amarillos parpadeantes
        "sound": "beep_confused"       # Sonidos de confusión
    },

    "sad": {
        "movement": "back_away",      # Retroceder
        "leds": "red_dim",            # LEDs rojos tenues
        "sound": "beep_sad"           # Sonidos tristes
    },

    "neutral": {
        "movement": "slight_move",    # Movimiento muy sutil
        "leds": "white_steady",       # LEDs blancos constantes
        "sound": None                 # Sin sonido
    }
}

# =============================================================================
# COMANDOS DE VOZ DIRECTOS
# =============================================================================
DIRECT_COMMANDS = {
    # Movimiento básico
    "adelante": "forward",
    "hacia adelante": "forward",
    "avanza": "forward",

    "atrás": "backward",
    "hacia atrás": "backward",
    "retrocede": "backward",

    "derecha": "right",
    "gira derecha": "right",
    "gira a la derecha": "right",

    "izquierda": "left",
    "gira izquierda": "left",
    "gira a la izquierda": "left",

    # Control
    "para": "stop",
    "detente": "stop",
    "quieto": "stop",
    "alto": "stop",

    # Acciones divertidas
    "gira": "spin",
    "da vueltas": "spin",
    "rota": "spin",

    "baila": "dance",
    "danza": "dance",
    "muévete": "dance",

    "luces": "light_show",
    "luz": "light_show",
    "colores": "light_show",
    "espectáculo": "light_show"
}

# =============================================================================
# CONFIGURACIÓN DE DEBUG Y LOGS
# =============================================================================
DEBUG_MODE = True         # Mostrar información de debug
LOG_AUDIO = False        # Guardar archivos de audio (para debug)
LOG_CONVERSATIONS = True  # Guardar conversaciones en archivo

# =============================================================================
# CONFIGURACIÓN AVANZADA
# =============================================================================
# Timeouts
WAKE_WORD_TIMEOUT = 1           # Timeout para palabra de activación (segundos)
COMMAND_TIMEOUT = 5             # Timeout para comandos (segundos)
CONVERSATION_TIMEOUT = 30       # Timeout inactividad conversación (segundos)

# Sensibilidad de audio
MIC_ENERGY_THRESHOLD = 300      # Umbral de energía del micrófono
MIC_DYNAMIC_ENERGY_THRESHOLD = True  # Ajuste automático del umbral

# Gestión de emociones
DEFAULT_EMOTION_DURATION = 3    # Duración por defecto de emociones (segundos)
EMOTION_TRANSITION_TIME = 0.5   # Tiempo de transición entre emociones

# Palabras de activación alternativas
WAKE_WORDS = ["robot", "mbot", ROBOT_NAME.lower()]

# =============================================================================
# MENSAJES DEL SISTEMA
# =============================================================================
WELCOME_MESSAGE = f"¡Hola! Soy {ROBOT_NAME}, tu robot asistente. Di 'robot' para hablar conmigo."

FAREWELL_MESSAGES = [
    "¡Hasta luego! Fue un placer hablar contigo.",
    "¡Adiós! Di 'robot' cuando quieras hablar de nuevo.",
    "¡Nos vemos! Estaré aquí cuando me necesites.",
    "¡Que tengas un buen día! Vuelve pronto."
]

ERROR_MESSAGES = {
    "no_understand": "¿Puedes repetir? No te escuché bien.",
    "api_error": "Disculpa, tuve un pequeño problema técnico. ¿Puedes intentar de nuevo?",
    "mbot_error": "Oops, algo pasó con mis motores. Intentémoslo otra vez.",
    "timeout": "Me quedo esperando. Di 'robot' si quieres hablar conmigo."
}

# =============================================================================
# CONFIGURACIÓN EXPERIMENTAL
# =============================================================================
# Estas características están en desarrollo
ENABLE_WHISPER_LOCAL = False     # Usar Whisper local en lugar de Google STT
ENABLE_EMOTION_LEARNING = False  # Aprender emociones del usuario
ENABLE_VOICE_CLONING = False     # Clonar voz del usuario
ENABLE_CAMERA_INPUT = False      # Usar cámara para gestos

# =============================================================================
# VALIDACIÓN DE CONFIGURACIÓN
# =============================================================================
def validate_config():
    """Valida que la configuración sea correcta"""
    issues = []

    if len(OPENAI_API_KEY) < 20:
        issues.append("❌ OPENAI_API_KEY no configurada correctamente")

    if SAMPLE_RATE not in [8000, 16000, 22050, 44100, 48000]:
        issues.append("⚠️  SAMPLE_RATE puede causar problemas")

    if TTS_VOICE_RATE < 50 or TTS_VOICE_RATE > 400:
        issues.append("⚠️  TTS_VOICE_RATE fuera del rango recomendado (50-400)")

    if not (0.0 <= TTS_VOICE_VOLUME <= 1.0):
        issues.append("❌ TTS_VOICE_VOLUME debe estar entre 0.0 y 1.0")

    return issues

if __name__ == "__main__":
    # Validar configuración al importar
    issues = validate_config()
    if issues:
        print("🔧 Problemas de configuración encontrados:")
        for issue in issues:
            print(f"   {issue}")
        print()
    else:
        print("✅ Configuración válida")
