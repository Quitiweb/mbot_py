import pyaudio
import wave
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

        # Estado
        self.is_listening = False
        self.is_speaking = False

        # Calibrar microfono
        self._calibrate_microphone()

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
