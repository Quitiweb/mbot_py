# mBot Voice Assistant

Convierte tu mBot en un asistente de voz que entiende comandos en español, responde con una personalidad breve y controla motores, LEDs y sonidos usando IA local (Ollama).

## Qué hace

- Escucha la palabra clave “robot” y mantiene conversaciones cortas.
- Traduce órdenes como “adelante”, “gira”, “baila” o “sígueme” en movimientos reales.
- Expresa emociones mediante LEDs y sonidos mientras habla desde el portátil.
- Funciona totalmente offline gracias a Ollama y al modelo `qwen2.5:7b`.

## Requisitos

- macOS / Linux / Windows con Python 3.10 o superior.
- mBot encendido y conectado por Bluetooth LE (preferido) o USB.
- Micrófono y altavoces en el ordenador.
- [Ollama](https://ollama.ai) instalado con el modelo `qwen2.5:7b` descargado.
- Dependencias Python listadas en `requirements.txt` (incluyen PyAudio, SpeechRecognition, Bleak, etc.).

## Puesta en marcha

```bash
# 1) Clona el repo y entra en la carpeta
git clone <url> mbot_project
cd mbot_project

# 2) Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate      # macOS / Linux
# .\venv\Scripts\activate    # Windows

# 3) Instala las dependencias
pip install -r requirements.txt

# 4) Copia y ajusta la configuración
cp config_example.py config.py
# Edita config.py para poner la voz, tipo de conexión, etc.

# 5) Prepara la IA local una vez
ollama pull qwen2.5:7b
```

## Cómo ejecutarlo

```bash
# Lanza Ollama si no está en marcha (una sola vez por sesión)
ollama serve &

# Activa el entorno virtual si hace falta
source venv/bin/activate

# Arranca el asistente
python main.py
```

1. Enciende el mBot y espera a que Bluetooth/USB se conecte.
2. Di “robot” para activarlo. El asistente responde por voz y muestra LEDs azules.
3. Da comandos cortos como “avanza”, “gira a la derecha”, “baila”, “detente” o conversa brevemente.
4. Di “adiós” o pulsa `Ctrl+C` para salir. Usa `mbot_controller.py` si quieres probar comandos básicos sin voz.

## Pruebas rápidas (opcional)

```bash
python tests/test_stop.py        # Comprueba movimiento básico
python tests/test_dance.py       # Lanza el baile manualmente
python -m pytest tests -k stop   # Ejecuta un subconjunto de tests
```

Listo. Si todo está bien, tendrás un mBot parlante y expresivo con un solo comando: `python main.py`.
