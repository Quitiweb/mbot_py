# mBot Explorer

Versión mínima del proyecto mBot enfocada en un flujo robótico sencillo:

- **Modo exploración** siempre activo (estilo Roomba): el robot avanza, detecta obstáculos con el ultrasonido y gira cuando algo se interpone.
- **Biblioteca de sonidos**: emite pitidos cortos tipo R2-D2 mientras se mueve para mostrar “vida”.
- **Modo seguir**: al recibir la orden adecuada, mantiene una distancia segura con la persona/objeto delante usando el mismo sensor.
- **Comandos por voz súper simples** (opcional): di “EME BOT” para que se detenga y, acto seguido, da una instrucción corta (explorar, seguir, parar o bailar).

## Requisitos

- macOS, Linux o Windows con Python 3.10+.
- mBot encendido y conectado preferiblemente por USB (la lectura de sensores solo está soportada así de momento).
- Módulo ultrasónico conectado al puerto/slot indicado en `config.py` (por defecto puerto 1, slot 3).
- Micrófono si quieres usar los comandos de voz (PyAudio + SpeechRecognition).
- Dependencias listadas en `requirements.txt` (`pyserial`, `pyaudio`, `SpeechRecognition`, `bleak`).

## Configuración rápida

```bash
git clone <url> mbot_project
cd mbot_project

python -m venv venv
source venv/bin/activate      # macOS / Linux
# .\venv\Scripts\activate   # Windows

pip install -r requirements.txt
cp config_example.py config.py   # Si lo necesitas como plantilla
```

Edita `config.py` para ajustar:

- `SENSOR_PORTS`: puerto/slot del ultrasonido frontal (y opcionales left/right si tienes más sensores).
- `EXPLORATION_SETTINGS`: velocidades, tiempos de giro y distancia a la que se considera obstáculo.
- `FOLLOW_SETTINGS`: ventana de distancia aceptable en modo seguir.
- Parámetros de voz (`VOICE_ENABLED`, `WAKE_WORD`, idioma, etc.) si quieres usar el micrófono.

## Ejecución

```bash
source venv/bin/activate
python main.py
```

1. El robot entra automáticamente en **modo exploración**.
2. Opcional: di “EME BOT” → el robot se detendrá, hará un destello azul y escuchará la orden.
3. Ordena una de las cuatro acciones soportadas:
	- **“explora”**: vuelve al modo por defecto.
	- **“sígueme” / “seguir”**: activa el modo seguimiento.
	- **“para” / “detente”**: se queda quieto hasta nueva orden.
	- **“baila”**: ejecuta el mini baile incorporado y luego retoma la exploración.
4. Pulsa `Ctrl+C` para salir y cerrar la conexión.

## Pruebas

Incluimos un test rápido para la lógica del parser de comandos:

```bash
python -m pytest tests -v
```

El resto del comportamiento depende del hardware, así que se prueba directamente con el robot encendido.

## Qué quedó fuera del alcance

- Conversaciones largas, IA conversacional, TTS, gestos complejos, etc. fueron eliminados para mantener el proyecto ligero.
- Solo usamos el sensor ultrasónico frontal por USB. Añadir BLE o más sensores requerirá trabajo adicional, pero la estructura ya está limpia para seguir iterando poco a poco.

Con esto tienes una base sencilla sobre la que seguir construyendo modos autónomos más avanzados.
