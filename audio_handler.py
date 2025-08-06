import speech_recognition as sr
import pyttsx3
import threading
import time
from config import *

class AudioHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Inicializar TTS
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', TTS_VOICE_RATE)
        self.tts_engine.setProperty('volume', TTS_VOICE_VOLUME)

        # Configurar voz española
        self._setup_spanish_voice()

        # Estado
        self.is_listening = False
        self.is_speaking = False

        # Calibrar microfono
        self._calibrate_microphone()

    def _setup_spanish_voice(self):
        """Configura la voz 97 Mónica (español España)"""
        voices = self.tts_engine.getProperty('voices')

        # Buscar específicamente la voz Mónica por ID o nombre
        monica_voice = None

        print(f"🔍 Buscando voz Mónica (ID: {TTS_VOICE_ID if 'TTS_VOICE_ID' in globals() else '97'})...")

        # Método 1: Buscar por ID específico
        if hasattr(self, 'TTS_VOICE_ID') or 'TTS_VOICE_ID' in globals():
            voice_id = globals().get('TTS_VOICE_ID', 97)
            if len(voices) > voice_id:
                monica_voice = voices[voice_id].id
                print(f"🎤 Encontrada voz por ID {voice_id}: {voices[voice_id].name}")

        # Método 2: Buscar por nombre exacto "Monica" o "Mónica"
        if not monica_voice:
            for voice in voices:
                if any(name in voice.name for name in ["Monica", "Mónica"]):
                    monica_voice = voice.id
                    print(f"🎤 Encontrada voz Mónica: {voice.name}")
                    break

        # Método 3: Buscar por patrones específicos de español España
        if not monica_voice:
            preferred_patterns = [
                "es_ES",
                "Spanish (Spain)",
                "Español (España)",
                "com.apple.ttsbundle.Monica-compact",
                "com.apple.voice.compact.es-ES.Monica"
            ]

            for pattern in preferred_patterns:
                for voice in voices:
                    if pattern in voice.id or pattern in voice.name:
                        monica_voice = voice.id
                        print(f"🎤 Encontrada voz española por patrón '{pattern}': {voice.name}")
                        break
                if monica_voice:
                    break

        # Aplicar la voz si se encontró
        if monica_voice:
            try:
                self.tts_engine.setProperty('voice', monica_voice)
                print("✅ Voz Mónica configurada correctamente")
            except Exception as e:
                print(f"⚠️  Error configurando voz Mónica: {e}")
                print("   Usando voz por defecto")
        else:
            print("❌ No se encontró la voz Mónica")
            print("   Voces disponibles:")
            for i, voice in enumerate(voices[:10]):  # Mostrar solo las primeras 10
                print(f"     {i}: {voice.name} ({voice.id})")
            print("   ...")
            print("   Para instalar más voces: Configuración > Accesibilidad > Contenido Hablado")

    def _calibrate_microphone(self):
        """Calibra el micrófono para ruido ambiente"""
        print("🎤 Calibrando micrófono... Mantén silencio por 2 segundos.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        print("✅ Micrófono calibrado.")

    def listen_for_wake_word(self, wake_word="robot"):
        """Escucha continuamente por la palabra de activación"""
        print(f"👂 Escuchando palabra de activación: '{wake_word}'...")

        while True:
            try:
                with self.microphone as source:
                    # Escuchar con timeout corto para no bloquear
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)

                # Reconocer usando whisper local o Google
                try:
                    text = self.recognizer.recognize_google(audio, language="es-ES").lower()
                    if wake_word.lower() in text:
                        print(f"🔥 Palabra de activación detectada: {text}")
                        return True

                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print("❌ Error con el servicio de reconocimiento")
                    time.sleep(1)

            except sr.WaitTimeoutError:
                continue
            except KeyboardInterrupt:
                break

        return False

    def listen_for_command(self, timeout=5):
        """Escucha un comando del usuario"""
        self.is_listening = True
        print("👂 Escuchando comando...")

        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)

            # Usar Google Speech Recognition (puedes cambiarlo por Whisper)
            text = self.recognizer.recognize_google(audio, language="es-ES")
            print(f"📝 Escuchado: {text}")
            self.is_listening = False
            return text.lower()

        except sr.WaitTimeoutError:
            print("⏰ Timeout - no se detectó audio")
        except sr.UnknownValueError:
            print("❓ No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"❌ Error del servicio de reconocimiento: {e}")

        self.is_listening = False
        return None

    def speak(self, text, blocking=False):
        """Convierte texto a voz"""
        if self.is_speaking:
            return

        def _speak():
            self.is_speaking = True
            print(f"🤖 mBot dice: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            self.is_speaking = False

        if blocking:
            _speak()
        else:
            threading.Thread(target=_speak, daemon=True).start()

    def is_currently_speaking(self):
        """Verifica si está hablando actualmente"""
        return self.is_speaking

    def is_currently_listening(self):
        """Verifica si está escuchando actualmente"""
        return self.is_listening

    def stop_speaking(self):
        """Detiene el TTS"""
        self.tts_engine.stop()
        self.is_speaking = False

if __name__ == "__main__":
    # Test del sistema de audio
    audio = AudioHandler()

    print("🧪 Probando sistema de audio...")
    audio.speak("Hola, soy tu robot mBot. Estoy probando mi voz.", blocking=True)

    print("🎤 Di algo...")
    command = audio.listen_for_command()
    if command:
        audio.speak(f"Escuché: {command}")
