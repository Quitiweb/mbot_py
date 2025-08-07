# mBot Voice Assistant 🤖🎤

Un asistente de voz inteligente para el robot mBot que utiliza IA local (Ollama) para conversaciones naturales y control completo del robot.

## 🌟 Características

- **IA Local**: Funciona con Ollama (Qwen2.5) sin necesidad de conexión a internet
- **Conectividad Dual**: Soporte automático para Bluetooth LE y USB
- **Control de Voz**: Reconocimiento de comandos en español
- **Síntesis de Voz**: Respuestas habladas con voz natural
- **Sistema de Gestos**: Expresiones emocionales con movimiento, LEDs y sonidos
- **Protocolo Original**: Compatible 100% con el protocolo oficial de mBot

## 📁 Estructura del Proyecto

```
mbot_project/
├── main.py                    # Punto de entrada principal
├── config.py                  # Configuración del sistema
├── requirements.txt           # Dependencias Python
├── setup.py                   # Configuración del paquete
├──
├── src/                       # Código fuente principal
│   ├── core/                  # Componentes centrales
│   │   ├── audio_handler.py   # Manejo de audio (STT/TTS)
│   │   ├── ai_brain.py        # Motor de IA (Ollama)
│   │   └── mbot_controller.py # Controlador principal del robot
│   ├── protocols/             # Protocolos de comunicación
│   │   ├── mbot_original_protocol.py  # Protocolo oficial mBot
│   │   ├── mbot_ble_fixed.py          # Protocolo BLE mejorado
│   │   └── mbot_ble_simple.py         # Protocolo BLE básico
│   └── engines/               # Motores especializados
│       ├── gesture_engine.py         # Motor de gestos (v1)
│       └── gesture_engine_fixed.py   # Motor de gestos mejorado
│
├── tests/                     # Suite de pruebas
│   ├── unit/                  # Tests unitarios
│   │   ├── test_mbot.py       # Tests del robot
│   │   ├── test_connection.py # Tests de conectividad
│   │   └── test_protocols.py  # Tests de protocolos
│   └── integration/           # Tests de integración
│       ├── test_complete_system.py  # Test del sistema completo
│       ├── test_integration.py      # Tests de integración
│       └── test_voices.py           # Tests de síntesis de voz
│
├── tools/                     # Herramientas de desarrollo
│   ├── diagnostics/           # Herramientas de diagnóstico
│   │   ├── diagnose_loop.py   # Diagnóstico de bucles
│   │   └── investigate_*.py   # Herramientas de investigación
│   ├── extreme_test.py        # Tests extremos
│   └── mbot_tools.py          # Herramientas generales
│
├── legacy/                    # Código heredado/obsoleto
│   ├── mbot_final.py          # Versión anterior
│   └── mbot_enhanced*.py      # Versiones experimentales
│
└── mbot_py/                   # Librería original de mBot
    └── lib/mBot.py            # Implementación original
```

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd mbot_project
```

### 2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Ollama (IA Local)
```bash
# Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelo Qwen2.5
ollama pull qwen2.5:7b
```

### 5. Configuración
```bash
cp config_example.py config.py
# Editar config.py según tus necesidades
```

## 🎮 Uso

### Ejecutar el asistente
```bash
python main.py
```

### Comandos disponibles
- **Activación**: Di "robot" para activar el asistente
- **Movimiento**: "ve hacia adelante", "gira a la derecha", "para"
- **Gestos**: "muéstrate feliz", "haz una danza", "parpadea"
- **Conversación**: Habla naturalmente con el robot

## 🧪 Testing

### Ejecutar tests unitarios
```bash
python -m pytest tests/unit/ -v
```

### Ejecutar tests de integración
```bash
python -m pytest tests/integration/ -v
```

### Tests específicos
```bash
# Test de conectividad
python tests/unit/test_connection.py

# Test del sistema completo
python tests/integration/test_complete_system.py
```

## 🛠️ Herramientas de Desarrollo

### Diagnóstico de problemas
```bash
# Diagnóstico de bucles infinitos
python tools/diagnostics/diagnose_loop.py

# Investigación de conectividad
python tools/diagnostics/investigate_ble.py
```

### Tests extremos
```bash
python tools/extreme_test.py
```

## 📡 Conectividad

### Bluetooth LE (Recomendado)
- Conexión automática
- Mayor estabilidad
- Sin cables

### USB
- Conexión por cable
- Fallback automático
- Mayor velocidad

## 🎛️ Configuración

Edita `config.py` para personalizar:

```python
# IA Backend
AI_BACKEND = "ollama"  # o "openai"
OLLAMA_MODEL_NAME = "qwen2.5:7b"

# Conectividad
MBOT_CONNECTION_TYPE = "auto"  # "bluetooth", "usb", "auto"

# Audio
TTS_PREFERRED_VOICE = "Monica"  # Voz española
SAMPLE_RATE = 16000

# Personalidad del robot
ROBOT_PERSONALITY = "Eres un robot amigable..."
```

## 🐛 Resolución de Problemas

### mBot no se conecta
1. Verificar que el robot esté encendido
2. Comprobar drivers Bluetooth/USB
3. Ejecutar `python tests/unit/test_connection.py`

### Audio no funciona
1. Verificar micrófono/altavoces
2. Ejecutar `python tests/integration/test_voices.py`
3. Revisar configuración de PyAudio

### IA no responde
1. Verificar que Ollama esté ejecutándose: `ollama serve`
2. Verificar modelo: `ollama list`
3. Ejecutar `python tests/integration/test_ollama_ai.py`

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Makeblock](https://www.makeblock.com/) por el robot mBot
- [Ollama](https://ollama.ai/) por la IA local
- Comunidad open source de Python
