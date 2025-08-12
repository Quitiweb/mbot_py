import threading
import time
from config import *

class GestureEngine:
    def __init__(self, mbot_controller):
        self.mbot_controller = mbot_controller
        self.current_emotion = "neutral"
        self.emotion_duration = 0
        self.emotion_start_time = 0

        # Cola de emociones para transiciones suaves
        self.emotion_queue = []
        self.is_transitioning = False

    def set_emotion(self, emotion, duration=3):
        """Establece una nueva emoción por un tiempo determinado"""
        if emotion not in GESTURES:
            emotion = "neutral"

        print(f"😊 Cambiando emoción a: {emotion} (duración: {duration}s)")

        self.current_emotion = emotion
        self.emotion_duration = duration
        self.emotion_start_time = time.time()

        # Ejecutar gesto inmediatamente
        self.mbot_controller.perform_gesture(emotion)

        # Programar vuelta a neutral si no es ya neutral
        if emotion != "neutral" and duration > 0:
            threading.Timer(duration, self._return_to_neutral).start()

    def _return_to_neutral(self):
        """Vuelve a estado neutral después del tiempo especificado"""
        if time.time() - self.emotion_start_time >= self.emotion_duration:
            print("😐 Volviendo a estado neutral")
            self.current_emotion = "neutral"
            self.mbot_controller.perform_gesture("neutral")

    def queue_emotion(self, emotion, duration=2):
        """Añade una emoción a la cola para ejecutar secuencialmente"""
        self.emotion_queue.append({"emotion": emotion, "duration": duration})

        if not self.is_transitioning:
            self._process_emotion_queue()

    def _process_emotion_queue(self):
        """Procesa la cola de emociones"""
        if not self.emotion_queue:
            return

        self.is_transitioning = True

        def process_next():
            while self.emotion_queue:
                emotion_data = self.emotion_queue.pop(0)
                self.set_emotion(emotion_data["emotion"], emotion_data["duration"])
                time.sleep(emotion_data["duration"])

            self.is_transitioning = False
            self.set_emotion("neutral", 0)

        threading.Thread(target=process_next, daemon=True).start()

    def express_while_speaking(self, text, base_emotion="neutral"):
        """Expresiones gestuales mientras habla basadas en el contenido"""

        # Análizar texto para determinar intensidad gestual
        exclamations = text.count('!')
        questions = text.count('?')
        text_length = len(text.split())

        # Determinar duración basada en longitud del texto (estimación)
        speaking_duration = max(2, text_length * 0.4)  # ~0.4 segundos por palabra

        if exclamations > 1 or "increíble" in text.lower() or "genial" in text.lower():
            self.set_emotion("excited", speaking_duration)

        elif questions > 0 or "qué" in text.lower() or "cómo" in text.lower():
            self.set_emotion("thinking", speaking_duration)

        elif "lo siento" in text.lower() or "disculpa" in text.lower():
            self.set_emotion("sad", speaking_duration)

        elif exclamations > 0 or "bien" in text.lower() or "perfecto" in text.lower():
            self.set_emotion("happy", speaking_duration)

        else:
            # Gesto sutil para mostrar que está "hablando"
            self.set_emotion(base_emotion, speaking_duration)

    def listening_mode(self):
        """Modo de escucha activa"""
        print("👂 Activando modo escucha")
        self.set_emotion("listening", 0)  # Sin límite de tiempo

    def thinking_mode(self, duration=2):
        """Modo pensando (procesando respuesta)"""
        print("🤔 Modo pensando...")
        self.set_emotion("thinking", duration)

    def get_current_emotion(self):
        """Obtiene la emoción actual"""
        return self.current_emotion

    def is_expressing_emotion(self):
        """Verifica si está expresando una emoción activa (no neutral)"""
        return self.current_emotion != "neutral" or self.mbot_controller.is_performing_gesture

    def emergency_stop(self):
        """Detiene todas las expresiones inmediatamente"""
        print("🛑 Deteniendo todas las expresiones")
        self.emotion_queue.clear()
        self.is_transitioning = False
        self.current_emotion = "neutral"
        self.mbot_controller.stop_gesture()

    def create_emotion_sequence(self, emotions_and_durations):
        """Crea una secuencia compleja de emociones

        Args:
            emotions_and_durations: Lista de tuplas (emotion, duration)
            Ejemplo: [("happy", 2), ("excited", 1), ("neutral", 1)]
        """
        for emotion, duration in emotions_and_durations:
            self.queue_emotion(emotion, duration)

if __name__ == "__main__":
    # Test del motor de gestos
    from src.core.mbot_controller import MBotController

    controller = MBotController()
    gesture_engine = GestureEngine(controller)

    if controller.mbot:
        print("🧪 Probando motor de gestos...")

        # Probar expresión mientras habla
        gesture_engine.express_while_speaking("¡Hola! ¡Qué genial verte hoy!", "happy")
        time.sleep(4)

        # Probar secuencia de emociones
        gesture_engine.create_emotion_sequence([
            ("thinking", 2),
            ("happy", 2),
            ("excited", 3)
        ])

        time.sleep(10)

        controller.cleanup()
    else:
        print("❌ No se pudo conectar al mBot para las pruebas")
