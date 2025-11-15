"""Implementación mínima de escucha por voz para el modo simplificado."""

import time
from typing import Optional

try:
    import speech_recognition as sr
except ImportError:  # pragma: no cover - solo ocurre si no está instalado
    sr = None


class VoiceInterface:
    def __init__(self, wake_word: str, language: str, poll_interval: float, command_timeout: float):
        if sr is None:
            raise RuntimeError("SpeechRecognition no está instalado; desactiva VOICE_ENABLED en config.py")

        self.wake_word = wake_word.lower()
        self.language = language
        self.poll_interval = poll_interval
        self.command_timeout = command_timeout
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._last_poll = 0.0

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)

    def ready_to_poll(self) -> bool:
        return (time.time() - self._last_poll) >= self.poll_interval

    def listen_for_wake_word(self) -> bool:
        if not self.ready_to_poll():
            return False

        self._last_poll = time.time()
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(source, timeout=0.5, phrase_time_limit=1.5)
            text = self.recognizer.recognize_google(audio, language=self.language).lower()
            return self.wake_word in text
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return False
        except sr.RequestError as exc:
            print(f"⚠️ Error reconociendo voz: {exc}")
            return False

    def listen_for_command(self) -> Optional[str]:
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=self.command_timeout,
                    phrase_time_limit=self.command_timeout,
                )
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text.lower().strip()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except sr.RequestError as exc:
            print(f"⚠️ Error reconociendo orden: {exc}")
            return None

    def close(self):
        # Interface para mantener compatibilidad con el controlador principal
        pass