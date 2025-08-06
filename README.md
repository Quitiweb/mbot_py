# mBot Asistente de Voz 🤖🎤

Un sistema avanzado de conversación natural que convierte tu mBot en un asistente inteligente y expresivo usando IA.

## 🌟 Características

- **🎤 Conversación por voz**: Habla naturalmente con tu mBot
- **🧠 IA integrada**: Usa ChatGPT para respuestas inteligentes
- **😊 Expresiones emocionales**: El mBot expresa emociones con LEDs, movimientos y sonidos
- **🎭 Gestos sincronizados**: Movimientos que acompañan la conversación
- **🎯 Comandos directos**: Control directo con comandos de voz
- **🎵 Sistema de sonidos**: Pitidos expresivos según el estado emocional

## 🎯 Funcionalidades

### Conversación Natural
- Activación por palabra clave ("robot")
- Reconocimiento de voz en español
- Respuestas contextuales usando ChatGPT
- Personalidad robótica pero amigable

### Expresiones Emocionales
- **Feliz**: LEDs arcoíris, pequeños saltos, pitidos alegres
- **Emocionado**: LEDs parpadeantes, giros, pitidos rápidos
- **Pensando**: LEDs azules pulsantes, balanceo suave
- **Confundido**: LEDs amarillos parpadeantes, movimiento de "no"
- **Triste**: LEDs rojos tenues, retroceder lentamente
- **Escuchando**: LEDs azules respirando, quieto y atento

### Comandos de Voz
- "adelante" - Mover hacia adelante
- "atrás" - Retroceder
- "derecha" / "izquierda" - Girar
- "para" / "detente" - Detenerse
- "baila" - Secuencia de baile
- "gira" - Giro completo
- "luz" - Espectáculo de luces

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)
```bash
./install.sh
```

### Opción 2: Manual
```bash
# Instalar dependencias del sistema (macOS)
brew install portaudio ffmpeg

# Instalar dependencias de Python
pip3 install -r requirements.txt

# Instalar Whisper (opcional, para STT local)
pip3 install openai-whisper
```

## ⚙️ Configuración

1. **API de OpenAI**: Edita `config.py` y añade tu clave:
```python
OPENAI_API_KEY = "tu-clave-api-aqui"
```

2. **Conectar mBot**: Conecta tu mBot por USB

3. **Verificar audio**: Asegúrate de que micrófono y altavoces funcionen

## 🎮 Uso

### Iniciar el Asistente
```bash
python3 main.py
```

### Interacción Básica
1. Di **"robot"** para activar
2. Espera la respuesta del mBot
3. Habla normalmente o da comandos
4. Di **"adiós"** para terminar la conversación

### Ejemplos de Conversación
```
👤: "Robot"
🤖: "¿Sí? ¿En qué puedo ayudarte?"

👤: "¿Cómo te sientes hoy?"
🤖: "¡Me siento genial! Mis motores están perfectos y mis LEDs brillan con energía."
    [LEDs arcoíris + pequeños movimientos de alegría]

👤: "Muévete hacia adelante"
🤖: "¡Adelante vamos! Me muevo hacia delante."
    [Se mueve hacia adelante + LEDs + sonido]

👤: "Puedes bailar para mí"
🤖: "¡Música, maestro! ¡Es hora de bailar!"
    [Secuencia de baile con LEDs de colores]
```

## 📁 Estructura del Proyecto

```
mbot_project/
├── main.py              # 🚀 Aplicación principal
├── audio_handler.py     # 🎤 Manejo de voz (STT/TTS)
├── ai_brain.py         # 🧠 Procesamiento con ChatGPT
├── mbot_controller.py  # 🤖 Control del hardware mBot
├── gesture_engine.py   # 🎭 Sistema de gestos/emociones
├── config.py           # ⚙️ Configuración general
├── requirements.txt    # 📦 Dependencias Python
├── install.sh         # 🛠️ Script de instalación
└── mbot_py/           # 📚 Librería base del mBot
    └── lib/mBot.py
```

## 🔧 Componentes Técnicos

### Sistema de Audio
- **STT**: Google Speech Recognition / OpenAI Whisper
- **TTS**: pyttsx3 (offline) o edge-tts
- **Activación**: Palabra clave "robot"
- **Idioma**: Español (configurable)

### Inteligencia Artificial
- **Motor**: OpenAI ChatGPT-3.5-turbo
- **Personalidad**: Robot amigable y expresivo
- **Contexto**: Mantiene historial de conversación
- **Emociones**: Análisis de sentimiento en respuestas

### Control del mBot
- **Comunicación**: Puerto serie USB
- **Movimientos**: Motores izquierdo/derecho independientes
- **LEDs**: RGB programables (2 LEDs)
- **Sonidos**: Buzzer con notas musicales
- **Sensores**: Preparado para sensores futuros

## 🎨 Personalización

### Cambiar Personalidad
Edita `ROBOT_PERSONALITY` en `config.py`:
```python
ROBOT_PERSONALITY = """
Eres un robot [tu descripción personalizada]...
"""
```

### Añadir Nuevos Gestos
Modifica `GESTURES` en `config.py`:
```python
GESTURES = {
    "mi_emocion": {
        "movement": "mi_movimiento",
        "leds": "mi_patron_led",
        "sound": "mi_sonido"
    }
}
```

### Comandos Personalizados
Añade a `DIRECT_COMMANDS` en `config.py`:
```python
DIRECT_COMMANDS = {
    "mi_comando": "accion_mbot",
}
```

## 🐛 Solución de Problemas

### mBot no conecta
- Verifica que esté conectado por USB
- Comprueba que el driver CH340 esté instalado
- Revisa que no haya otros programas usando el puerto

### Micrófono no funciona
- Verifica permisos de micrófono en Configuración del Sistema
- Prueba con otro micrófono
- Ajusta `SAMPLE_RATE` en config.py

### OpenAI API no responde
- Verifica tu clave API en config.py
- Comprueba tu saldo de OpenAI
- Revisa tu conexión a internet

### PyAudio no se instala
```bash
# macOS
brew install portaudio
pip3 install pyaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
```

## 📈 Próximas Características

- [ ] **Whisper local**: STT offline
- [ ] **Interfaz web**: Control desde navegador
- [ ] **Reconocimiento facial**: Usando cámara web
- [ ] **Más sensores**: Ultrasonido, línea, luz
- [ ] **Voces premium**: ElevenLabs integration
- [ ] **Comandos complejos**: "Ve a la cocina y enciende la luz"
- [ ] **Memoria persistente**: Recordar conversaciones
- [ ] **Multi-idioma**: Soporte para inglés, francés, etc.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una branch para tu feature
3. Commit tus cambios
4. Push a la branch
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **Makeblock** por el increíble mBot
- **OpenAI** por ChatGPT y Whisper
- **Comunidad Python** por las excelentes librerías

---

**¡Hecho con ❤️ para hacer los robots más humanos y amigables!**

¿Tienes preguntas? ¡Abre un issue o contacta conmigo!
