#!/bin/bash

echo "🤖 Instalador de mBot Asistente de Voz con IA Local"
echo "================================================="

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

# Función para instalar Ollama
install_ollama() {
    echo "🧠 Instalando Ollama (IA Local)..."

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if ! command -v ollama &> /dev/null; then
            echo "   Instalando Ollama con Homebrew..."
            brew install ollama
        else
            echo "   ✅ Ollama ya está instalado"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if ! command -v ollama &> /dev/null; then
            echo "   Instalando Ollama para Linux..."
            curl -fsSL https://ollama.com/install.sh | sh
        else
            echo "   ✅ Ollama ya está instalado"
        fi
    else
        echo "   ❌ SO no soportado para instalación automática de Ollama"
        echo "   Por favor visita: https://ollama.com/download"
        return 1
    fi
}

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

    # Instalar Ollama
    install_ollama
fi

# Instalar Ollama en Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detectado Linux - Instalando dependencias del sistema..."

    # Instalar dependencias básicas
    sudo apt-get update
    sudo apt-get install -y python3-dev portaudio19-dev ffmpeg

    # Instalar Ollama
    install_ollama
fi

# Configurar IA local
echo "🧠 Configurando IA local con Ollama..."

# Esperar un momento para que Ollama se inicialice
echo "⏳ Iniciando Ollama server..."
ollama serve &
OLLAMA_PID=$!
sleep 5

# Descargar modelo recomendado
echo "📥 Descargando modelo IA avanzado (Qwen2.5 7B)..."
echo "   Esto puede tardar varios minutos dependiendo de tu conexión..."
ollama pull qwen2.5:7b

echo "✅ IA local configurada correctamente"

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
    import requests
    print('✅ Requests: OK')
except ImportError:
    print('❌ Requests: FALLO')

try:
    import serial
    print('✅ PySerial: OK')
except ImportError:
    print('❌ PySerial: FALLO')

# Verificar Ollama
import subprocess
try:
    result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
    if 'qwen2.5:7b' in result.stdout:
        print('✅ Ollama + Qwen2.5: OK')
    else:
        print('⚠️  Ollama instalado pero modelo no descargado')
except:
    print('❌ Ollama: FALLO')
"

echo ""
echo "🎉 CONFIGURACIÓN COMPLETADA!"
echo "============================"
echo "✅ IA Local: Ollama con modelo Qwen2.5 7B instalado"
echo "✅ Dependencias de Python instaladas"
echo "✅ Entorno virtual creado"
echo ""
echo "📋 PARA USAR EL ASISTENTE:"
echo "1. Conecta tu mBot por USB"
echo "2. Asegúrate de que tu micrófono y altavoces funcionen"
echo "3. Si Ollama no está ejecutándose, arrancalo con: ollama serve"
echo ""
echo "🚀 EJECUTAR EL ASISTENTE:"
echo "   source mbot_env/bin/activate"
echo "   python3 main.py"
echo ""
echo "🧪 PROBAR SOLO LA IA:"
echo "   python3 ai_brain.py"
echo ""
echo "✅ ¡Todo listo para usar tu asistente mBot con IA local!"
