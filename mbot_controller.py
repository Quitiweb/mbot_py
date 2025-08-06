import threading
import time
import random
from mbot_py.lib.mBot import mBot
from config import *

class MBotController:
    def __init__(self):
        try:
            self.mbot = mBot()
            print("✅ mBot conectado correctamente")
        except Exception as e:
            print(f"❌ Error conectando mBot: {e}")
            self.mbot = None

        # Estado del robot
        self.current_gesture = None
        self.is_performing_gesture = False
        self.gesture_thread = None
        self._stop_requested = False  # Flag para parar gestos

    def execute_command(self, command):
        """Ejecuta un comando directo en el mBot"""
        if not self.mbot:
            return

        print(f"🤖 Ejecutando comando: {command}")

        try:
            if command == "forward":
                self.mbot.doMove(100, 100)
                time.sleep(1)
                self.mbot.doMove(0, 0)

            elif command == "backward":
                self.mbot.doMove(-100, -100)
                time.sleep(1)
                self.mbot.doMove(0, 0)

            elif command == "right":
                self.mbot.doMove(80, -80)  # Giro a la derecha
                time.sleep(0.8)
                self.mbot.doMove(0, 0)

            elif command == "left":
                self.mbot.doMove(-80, 80)  # Giro a la izquierda
                time.sleep(0.8)
                self.mbot.doMove(0, 0)

            elif command == "stop":
                print("🛑 COMANDO STOP - Deteniendo todas las actividades...")
                # Marcar que debe pararse
                self._stop_requested = True
                # Detener inmediatamente todos los movimientos
                self.mbot.doMove(0, 0)
                # Detener todos los gestos
                self.stop_gesture()
                # Apagar todos los LEDs
                self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
                print("✅ Robot detenido completamente")

            elif command == "spin":
                self.perform_spin()

            elif command == "dance":
                self.perform_dance()

            elif command == "light_show":
                self.perform_light_show()

        except Exception as e:
            print(f"❌ Error ejecutando comando {command}: {e}")

    def perform_gesture(self, gesture_name):
        """Ejecuta un gesto emocional (versión simplificada)"""
        if not self.mbot:
            return

        if gesture_name not in GESTURES:
            gesture_name = "neutral"

        gesture = GESTURES[gesture_name]
        print(f"🎭 Realizando gesto: {gesture_name}")

        # Detener gesto anterior (solo físicamente, no cambiar flags)
        if self.mbot:
            self.mbot.doMove(0, 0)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

        # Resetear flag de parada DESPUÉS de limpiar estado anterior
        self._stop_requested = False
        self.is_performing_gesture = True

        # Iniciar nuevo gesto de forma simple
        self._execute_simple_gesture(gesture)

        # Marcar que terminó el gesto
        self.is_performing_gesture = False

    def _execute_simple_gesture(self, gesture):
        """Ejecuta un gesto de forma simple sin hilos"""
        try:
            movement = gesture["movement"]
            leds = gesture["leds"]
            sound = gesture["sound"]

            # Ejecutar movimiento
            if movement == "bounce":
                self._simple_bounce()
            elif movement == "gentle_sway":
                self._simple_sway()
            elif movement == "slight_move":
                self._simple_move()
            elif movement == "spin":
                self._simple_spin()
            elif movement == "head_shake":
                self._simple_head_shake()
            elif movement == "back_away":
                self._simple_back_away()
            elif movement == "stop":
                self._simple_stop()

            # Ejecutar LEDs
            self._simple_leds(leds)

            # Ejecutar sonido
            if sound:
                self._simple_sound(sound)

        except Exception as e:
            print(f"❌ Error en gesto simple: {e}")

    def _simple_bounce(self):
        """Movimiento de rebote simple"""
        if self._stop_requested or not self.mbot:
            return
        self.mbot.doMove(100, 100)
        time.sleep(0.3)
        if self._stop_requested:
            self.mbot.doMove(0, 0)
            return
        self.mbot.doMove(-80, -80)
        time.sleep(0.2)
        self.mbot.doMove(0, 0)

    def _simple_sway(self):
        """Balanceo simple"""
        if self._stop_requested or not self.mbot:
            return
        self.mbot.doMove(50, -50)
        time.sleep(0.5)
        if self._stop_requested:
            self.mbot.doMove(0, 0)
            return
        self.mbot.doMove(-50, 50)
        time.sleep(0.5)
        self.mbot.doMove(0, 0)

    def _simple_move(self):
        """Movimiento muy sutil"""
        if self._stop_requested or not self.mbot:
            return
        self.mbot.doMove(30, 30)
        time.sleep(0.3)
        self.mbot.doMove(0, 0)

    def _simple_spin(self):
        """Giro completo emocionado"""
        if self._stop_requested or not self.mbot:
            return
        # Giro rápido a la derecha
        self.mbot.doMove(100, -100)
        time.sleep(1.2)  # Tiempo suficiente para giro completo
        self.mbot.doMove(0, 0)

    def _simple_head_shake(self):
        """Movimiento de "no" (confusión)"""
        if self._stop_requested or not self.mbot:
            return
        # Pequeños giros alternados
        for _ in range(3):  # 3 sacudidas
            if self._stop_requested:
                break
            self.mbot.doMove(40, -40)
            time.sleep(0.2)
            if self._stop_requested:
                break
            self.mbot.doMove(-40, 40)
            time.sleep(0.2)
        self.mbot.doMove(0, 0)

    def _simple_back_away(self):
        """Retroceder tristemente"""
        if self._stop_requested or not self.mbot:
            return
        # Retroceso lento y triste
        self.mbot.doMove(-60, -60)
        time.sleep(0.8)
        self.mbot.doMove(0, 0)

    def _simple_stop(self):
        """Permanecer quieto (modo escucha)"""
        if self._stop_requested or not self.mbot:
            return
        # Solo asegurarse que esté parado
        self.mbot.doMove(0, 0)

    def _simple_leds(self, led_pattern):
        """LEDs simples"""
        if self._stop_requested or not self.mbot:
            return

        try:
            if led_pattern == "rainbow":
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
                for color in colors:
                    if self._stop_requested:
                        break
                    self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
                    self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
                    time.sleep(0.5)

            elif led_pattern == "flash_multicolor":
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
                for _ in range(3):  # 3 cycles of flashing
                    for color in colors:
                        if self._stop_requested:
                            break
                        self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
                        self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
                        time.sleep(0.2)

            elif led_pattern == "blue_pulse":
                self.mbot.doRGBLedOnBoard(0, 0, 0, 255)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 255)
                time.sleep(1)

            elif led_pattern == "blue_breathing":
                # Efecto de "respiración" azul
                for intensity in [50, 100, 150, 255, 150, 100, 50]:
                    if self._stop_requested:
                        break
                    self.mbot.doRGBLedOnBoard(0, 0, 0, intensity)
                    self.mbot.doRGBLedOnBoard(1, 0, 0, intensity)
                    time.sleep(0.3)

            elif led_pattern == "yellow_blink":
                # Parpadeo amarillo (confusión)
                for _ in range(6):
                    if self._stop_requested:
                        break
                    self.mbot.doRGBLedOnBoard(0, 255, 255, 0)
                    self.mbot.doRGBLedOnBoard(1, 255, 255, 0)
                    time.sleep(0.2)
                    self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                    self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
                    time.sleep(0.2)

            elif led_pattern == "red_dim":
                # Rojo tenue (tristeza)
                self.mbot.doRGBLedOnBoard(0, 80, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 80, 0, 0)
                time.sleep(1.5)

            elif led_pattern == "white_steady":
                self.mbot.doRGBLedOnBoard(0, 255, 255, 255)
                self.mbot.doRGBLedOnBoard(1, 255, 255, 255)
                time.sleep(1)

            # Apagar LEDs al final
            if not self._stop_requested:
                time.sleep(0.5)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

        except Exception as e:
            print(f"❌ Error en LEDs: {e}")

    def _simple_sound(self, sound_type):
        """Sonidos simples"""
        if self._stop_requested or not self.mbot:
            return

        try:
            if sound_type == "beep_happy":
                self.mbot.doBuzzer(523, 200)  # Do
                if not self._stop_requested:
                    time.sleep(0.3)
                    self.mbot.doBuzzer(659, 200)  # Mi

            elif sound_type == "beep_fast":
                # Pitidos rápidos de emoción
                frequencies = [523, 659, 784, 1047]  # Do, Mi, Sol, Do alto
                for freq in frequencies:
                    if self._stop_requested:
                        break
                    self.mbot.doBuzzer(freq, 150)
                    time.sleep(0.1)

            elif sound_type == "beep_confused":
                # Sonido de confusión (tonos discordantes)
                self.mbot.doBuzzer(400, 300)
                if not self._stop_requested:
                    time.sleep(0.1)
                    self.mbot.doBuzzer(300, 300)

            elif sound_type == "beep_sad":
                # Sonido triste (tono descendente)
                self.mbot.doBuzzer(523, 400)  # Do
                if not self._stop_requested:
                    time.sleep(0.2)
                    self.mbot.doBuzzer(392, 400)  # Sol bajo

            elif sound_type == "beep_low":
                self.mbot.doBuzzer(200, 300)

        except Exception as e:
            print(f"❌ Error en sonido: {e}")

    def perform_spin(self):
        """Giro completo"""
        if not self.mbot:
            return
        print("🔄 Girando...")
        self.mbot.doMove(100, -100)
        time.sleep(1.5)
        self.mbot.doMove(0, 0)

    def perform_dance(self):
        """Secuencia de baile"""
        if not self.mbot:
            return

        print("💃 ¡Iniciando baile!")
        try:
            # Secuencia simple de baile
            moves = [
                (100, -100, 0.5),   # Giro derecha
                (-100, 100, 0.5),   # Giro izquierda
                (150, 150, 0.3),    # Adelante
                (-100, -100, 0.3),  # Atrás
            ]

            for left, right, duration in moves:
                if self._stop_requested:
                    break
                self.mbot.doMove(left, right)
                # LED aleatorio
                color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
                self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
                self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
                time.sleep(duration)

            self.mbot.doMove(0, 0)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

        except Exception as e:
            print(f"❌ Error en baile: {e}")

    def perform_light_show(self):
        """Espectáculo de luces"""
        if not self.mbot:
            return

        print("✨ Espectáculo de luces!")
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

        for i in range(10):
            if self._stop_requested:
                break
            color = random.choice(colors)
            self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
            self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
            time.sleep(0.3)

        self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
        self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

    def stop_gesture(self):
        """Detiene el gesto actual inmediatamente"""
        print("🛑 Deteniendo gesto actual...")

        # Marcar que debe detenerse
        self._stop_requested = True
        self.is_performing_gesture = False

        # Detener movimiento inmediatamente
        if self.mbot:
            self.mbot.doMove(0, 0)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
            print("✅ mBot detenido")

    def cleanup(self):
        """Limpia recursos del mBot"""
        self.stop_gesture()
        if self.mbot:
            self.mbot.doMove(0, 0)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
            self.mbot.close()

if __name__ == "__main__":
    # Test del controlador simplificado
    controller = MBotController()

    if controller.mbot:
        print("🧪 Probando controlador simplificado...")

        # Probar comando de parada
        print("1. Probando movimiento y parada...")
        controller.execute_command("forward")
        time.sleep(1)
        controller.execute_command("stop")

        time.sleep(2)

        # Probar gesto y parada
        print("2. Probando gesto y parada...")
        controller.perform_gesture("happy")
        time.sleep(1)
        controller.stop_gesture()

        controller.cleanup()
    else:
        print("❌ No se pudo conectar al mBot para las pruebas")
