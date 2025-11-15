#!/usr/bin/env python3
"""
Gesture Engine mejorado - Sin bucles infinitos
"""

import time
import threading
from config import GESTURES

class GestureEngineFixed:
    def __init__(self, mbot_controller):
        self.mbot_controller = mbot_controller
        self.current_emotion = "neutral"
        self.emotion_start_time = 0
        self.emotion_duration = 0
        self.emotion_queue = []
        self.is_transitioning = False

        # Control de hilos y timers
        self.active_timers = []
        self.gesture_lock = threading.Lock()
        self.should_stop = False

    def set_emotion(self, emotion, duration=3):
        """Establece una nueva emoción - VERSIÓN SEGURA"""
        with self.gesture_lock:
            # Cancelar cualquier timer pendiente
            self._cancel_all_timers()

            # Parar cualquier gesto activo
            self.mbot_controller.stop_current_gesture()

            if emotion not in GESTURES:
                emotion = "neutral"

            print(f"😊 Cambiando emoción a: {emotion} (duración: {duration}s)")

            self.current_emotion = emotion
            self.emotion_duration = duration
            self.emotion_start_time = time.time()

            # Ejecutar gesto de forma segura
            try:
                self.mbot_controller.perform_gesture(emotion)
            except Exception as e:
                print(f"❌ Error ejecutando gesto: {e}")

            # Programar vuelta a neutral si corresponde
            if emotion != "neutral" and duration > 0:
                timer = threading.Timer(duration, self._return_to_neutral_safe)
                timer.daemon = True  # Timer daemon para que se cierre con el programa
                timer.start()
                self.active_timers.append(timer)

    def _return_to_neutral_safe(self):
        """Vuelve a estado neutral de forma segura"""
        with self.gesture_lock:
            if self.should_stop:
                return

            if time.time() - self.emotion_start_time >= self.emotion_duration:
                print("😐 Volviendo a estado neutral de forma segura")
                try:
                    self.mbot_controller.stop_current_gesture()
                    time.sleep(0.1)  # Pequeña pausa para asegurar parada
                    self.current_emotion = "neutral"
                    self.mbot_controller.perform_gesture("neutral")
                except Exception as e:
                    print(f"❌ Error volviendo a neutral: {e}")

    def _cancel_all_timers(self):
        """Cancela todos los timers activos"""
        for timer in self.active_timers:
            if timer.is_alive():
                timer.cancel()
        self.active_timers.clear()

    def express_while_speaking(self, text, base_emotion="neutral"):
        """Expresión durante el habla - VERSIÓN SIMPLIFICADA"""
        # Análisis simple del texto
        exclamations = text.count('!')
        questions = text.count('?')
        text_length = len(text.split())
        speaking_duration = max(2, text_length * 0.4)

        # Determinizar emoción basada en texto
        if exclamations > 1 or "increíble" in text.lower() or "genial" in text.lower():
            target_emotion = "excited"
        elif questions > 0 or "qué" in text.lower() or "cómo" in text.lower():
            target_emotion = "thinking"
        elif "lo siento" in text.lower() or "disculpa" in text.lower():
            target_emotion = "sad"
        elif exclamations > 0 or "bien" in text.lower() or "perfecto" in text.lower():
            target_emotion = "happy"
        else:
            target_emotion = base_emotion

        # Aplicar emoción de forma segura
        self.set_emotion(target_emotion, speaking_duration)

    def listening_mode(self):
        """Modo escucha - Robot atento y vivo"""
        with self.gesture_lock:
            print("👂 Modo escucha activado")
            self._cancel_all_timers()
            self.mbot_controller.stop_current_gesture()

            # Gesto de escucha: LEDs azules pulsantes, leve balanceo
            self.current_emotion = "listening"
            try:
                self.mbot_controller.perform_gesture("listening")
            except Exception as e:
                print(f"❌ Error en modo escucha: {e}")

    def thinking_mode(self, duration=2):
        """Modo pensando - Indica procesamiento"""
        print(f"🤔 Modo pensando...")
        self.set_emotion("thinking", duration)

    def idle_movement(self):
        """Pequeño movimiento para mostrar que está vivo durante la escucha"""
        with self.gesture_lock:
            try:
                if not self.mbot_controller or not self.mbot_controller.mbot:
                    return

                print("🔄 Movimiento de vida...")
                # Pequeño movimiento sutil
                self.mbot_controller.mbot.doMove(20, -20)  # Giro muy leve
                time.sleep(0.3)
                self.mbot_controller.mbot.doMove(0, 0)  # Parar

                # LED azul breathing para mostrar que escucha
                self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 100, 255)
                self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 100, 255)
                time.sleep(0.5)
                self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 50, 150)
                self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 50, 150)

            except Exception as e:
                print(f"❌ Error en movimiento idle: {e}")

    def immediate_action(self, action_type):
        """Ejecuta acción inmediata (para comandos de movimiento)"""
        with self.gesture_lock:
            print(f"⚡ Acción inmediata: {action_type}")
            self._cancel_all_timers()
            self.mbot_controller.stop_current_gesture()

            try:
                if not self.mbot_controller or not self.mbot_controller.mbot:
                    return

                if action_type == "backward":
                    # Retroceder con luces de alerta
                    self.mbot_controller.mbot.doRGBLedOnBoard(0, 255, 255, 0)  # Amarillo
                    self.mbot_controller.mbot.doRGBLedOnBoard(1, 255, 255, 0)
                    self.mbot_controller.mbot.doMove(-100, -100)
                    time.sleep(1.5)
                    self.mbot_controller.mbot.doMove(0, 0)

                elif action_type == "forward":
                    # Avanzar con luces verdes
                    self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 255, 0)  # Verde
                    self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 255, 0)
                    self.mbot_controller.mbot.doMove(100, 100)
                    time.sleep(1.5)
                    self.mbot_controller.mbot.doMove(0, 0)

                elif action_type == "stop":
                    # Parar con luz roja
                    self.mbot_controller.mbot.doMove(0, 0)
                    self.mbot_controller.mbot.doRGBLedOnBoard(0, 255, 0, 0)  # Rojo
                    self.mbot_controller.mbot.doRGBLedOnBoard(1, 255, 0, 0)
                    self.mbot_controller.mbot.doBuzzer(300, 200)  # Beep de parada

                elif action_type == "follow":
                    self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 255, 0)
                    self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 255, 0)
                    self.mbot_controller.mbot.doMove(80, 80)
                    time.sleep(1.0)
                    self.mbot_controller.mbot.doMove(0, 0)

                # Volver a estado neutral después de la acción
                time.sleep(0.5)
                self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 0, 0)

            except Exception as e:
                print(f"❌ Error en acción inmediata: {e}")

    def get_current_emotion(self):
        """Expone la emoción actual para diagnósticos."""
        return self.current_emotion

    def stop_all(self):
        """Parar todo de forma segura"""
        print("🛑 Parando gesture engine...")
        self.should_stop = True

        with self.gesture_lock:
            self._cancel_all_timers()
            self.mbot_controller.stop_current_gesture()

            # Asegurar parada completa
            try:
                if self.mbot_controller.mbot:
                    self.mbot_controller.mbot.doMove(0, 0)
                    self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                    self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 0, 0)
            except Exception as e:
                print(f"⚠️ Error en parada final: {e}")

def test_fixed_gesture_engine():
    """Test del gesture engine arreglado"""
    print("🧪 PROBANDO GESTURE ENGINE ARREGLADO")
    print("=" * 50)

    # Importar después para evitar dependencias circulares
    from legacy.mbot_final import MBotFinal

    try:
        # Mock del controlador para testing
        class MockController:
            def __init__(self):
                self.mbot = MBotFinal(connection_type="auto")
                self.gesture_active = False

            def perform_gesture(self, emotion):
                print(f"🎭 Ejecutando gesto: {emotion}")
                self.gesture_active = True

                # Simular gesto corto y seguro
                if emotion == "happy":
                    self.mbot.doRGBLedOnBoard(0, 0, 255, 0)  # Verde
                    self.mbot.doMove(50, 50)
                    time.sleep(0.5)
                    self.mbot.doMove(0, 0)
                    self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                elif emotion == "neutral":
                    self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                    self.mbot.doMove(0, 0)

                self.gesture_active = False
                print(f"✅ Gesto {emotion} completado")

            def stop_current_gesture(self):
                print("🛑 Parando gesto actual")
                self.gesture_active = False
                if hasattr(self, 'mbot') and self.mbot:
                    self.mbot.doMove(0, 0)
                    self.mbot.doRGBLedOnBoard(0, 0, 0, 0)

        controller = MockController()
        gesture_engine = GestureEngineFixed(controller)

        print("✅ Gesture engine creado")

        # Prueba 1: Emoción simple
        print("\n1️⃣ Probando emoción simple...")
        gesture_engine.set_emotion("happy", 2)
        time.sleep(3)  # Debe volver a neutral automáticamente

        # Prueba 2: Cambio rápido de emociones
        print("\n2️⃣ Probando cambios rápidos...")
        gesture_engine.set_emotion("happy", 5)
        time.sleep(1)
        gesture_engine.set_emotion("excited", 3)  # Debe cancelar el anterior
        time.sleep(4)

        # Prueba 3: Parada forzada
        print("\n3️⃣ Probando parada forzada...")
        gesture_engine.set_emotion("happy", 10)
        time.sleep(1)
        gesture_engine.stop_all()

        print("\n✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("Si no hubo bucles infinitos, el problema está resuelto")

        controller.mbot.close()

    except Exception as e:
        print(f"❌ Error en test: {e}")

if __name__ == "__main__":
    test_fixed_gesture_engine()
