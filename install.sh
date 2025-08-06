#!/bin/bash

echo "🤖 Instalador de mBot Asistente de Voz"
echo "====================================="

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    exit 1
fi

echo "✅ Python3 encontrado: $(python3 --version)"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    exit 1
fi

echo "✅ pip3 encontrado"

# Instalar dependencias del sistema (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detectado macOS - Instalando dependencias del sistema..."

    # Verificar si Homebrew está instalado
    if ! command -v brew &> /dev/null; then
        echo "⚠️  Homebrew no está instalado. Instalándolo..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    # Instalar portaudio para PyAudio
    echo "📦 Instalando portaudio..."
    brew install portaudio

    # Instalar ffmpeg para procesamiento de audio
    echo "📦 Instalando ffmpeg..."
    brew install ffmpeg
fi

# Crear entorno virtual (opcional pero recomendado)
echo "📦 Creando entorno virtual..."
python3 -m venv mbot_env

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source mbot_env/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias de Python
echo "📦 Instalando dependencias de Python..."

# Instalar PyAudio (puede requerir dependencias del sistema)
echo "🎤 Instalando PyAudio..."
pip install pyaudio

# Instalar otras dependencias
echo "📦 Instalando resto de dependencias..."
pip install -r requirements.txt

# Instalar OpenAI Whisper
echo "🎧 Instalando Whisper de OpenAI..."
pip install openai-whisper

# Verificar instalaciones
echo ""
echo "🧪 Verificando instalaciones..."

python3 -c "
try:
    import pyaudio
    print('✅ PyAudio: OK')
except ImportError:
    print('❌ PyAudio: FALLO')

try:
    import speech_recognition
    print('✅ SpeechRecognition: OK')
except ImportError:
    print('❌ SpeechRecognition: FALLO')

try:
    import pyttsx3
    print('✅ pyttsx3: OK')
except ImportError:
    print('❌ pyttsx3: FALLO')

try:
    import openai
    print('✅ OpenAI: OK')
except ImportError:
    print('❌ OpenAI: FALLO')

try:
    import serial
    print('✅ PySerial: OK')
except ImportError:
    print('❌ PySerial: FALLO')
"

echo ""
echo "📝 CONFIGURACIÓN NECESARIA:"
echo "1. Configura tu API key de OpenAI en config.py"
echo "2. Conecta tu mBot por USB"
echo "3. Asegúrate de que tu micrófono y altavoces funcionen"
echo ""
echo "🚀 EJECUTAR EL ASISTENTE:"
echo "   source mbot_env/bin/activate"
echo "   python3 main.py"
echo ""
echo "✅ Instalación completada!"
