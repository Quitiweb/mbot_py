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
                self.mbot.doMove(0, 0)
                self.stop_gesture()

            elif command == "spin":
                self.perform_spin()

            elif command == "dance":
                self.perform_dance()

            elif command == "light_show":
                self.perform_light_show()

        except Exception as e:
            print(f"❌ Error ejecutando comando {command}: {e}")

    def perform_gesture(self, gesture_name):
        """Ejecuta un gesto emocional"""
        if not self.mbot or self.is_performing_gesture:
            return

        if gesture_name not in GESTURES:
            gesture_name = "neutral"

        gesture = GESTURES[gesture_name]
        print(f"🎭 Realizando gesto: {gesture_name}")

        # Detener gesto anterior
        self.stop_gesture()

        # Iniciar nuevo gesto en thread separado
        self.is_performing_gesture = True
        self.current_gesture = gesture_name
        self.gesture_thread = threading.Thread(
            target=self._execute_gesture,
            args=(gesture,),
            daemon=True
        )
        self.gesture_thread.start()

    def _execute_gesture(self, gesture):
        """Ejecuta los componentes de un gesto"""
        try:
            # Ejecutar movimiento, LEDs y sonido en paralelo
            movement_thread = threading.Thread(target=self._do_movement, args=(gesture["movement"],))
            led_thread = threading.Thread(target=self._do_leds, args=(gesture["leds"],))
            sound_thread = threading.Thread(target=self._do_sound, args=(gesture["sound"],))

            movement_thread.start()
            led_thread.start()
            sound_thread.start()

            # Esperar a que terminen
            movement_thread.join()
            led_thread.join()
            sound_thread.join()

        except Exception as e:
            print(f"❌ Error en gesto: {e}")
        finally:
            self.is_performing_gesture = False
            self.current_gesture = None

    def _do_movement(self, movement_type):
        """Ejecuta movimientos específicos"""
        if not self.mbot:
            return

        try:
            if movement_type == "bounce":
                # Pequeños saltos hacia adelante y atrás
                for _ in range(3):
                    self.mbot.doMove(150, 150)
                    time.sleep(0.2)
                    self.mbot.doMove(-100, -100)
                    time.sleep(0.15)
                self.mbot.doMove(0, 0)

            elif movement_type == "spin":
                # Giro completo
                self.mbot.doMove(100, -100)
                time.sleep(2)
                self.mbot.doMove(0, 0)

            elif movement_type == "gentle_sway":
                # Balanceo suave
                for _ in range(4):
                    self.mbot.doMove(50, -50)
                    time.sleep(0.5)
                    self.mbot.doMove(-50, 50)
                    time.sleep(0.5)
                self.mbot.doMove(0, 0)

            elif movement_type == "head_shake":
                # Movimiento de "no" (izquierda-derecha)
                for _ in range(3):
                    self.mbot.doMove(-60, 60)
                    time.sleep(0.3)
                    self.mbot.doMove(60, -60)
                    time.sleep(0.3)
                self.mbot.doMove(0, 0)

            elif movement_type == "back_away":
                # Retroceder lentamente
                self.mbot.doMove(-80, -80)
                time.sleep(1.5)
                self.mbot.doMove(0, 0)

            elif movement_type == "slight_move":
                # Movimiento muy sutil
                self.mbot.doMove(30, 30)
                time.sleep(0.3)
                self.mbot.doMove(0, 0)

        except Exception as e:
            print(f"❌ Error en movimiento {movement_type}: {e}")

    def _do_leds(self, led_pattern):
        """Controla los patrones de LED"""
        if not self.mbot:
            return

        try:
            if led_pattern == "rainbow":
                colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (238, 130, 238)]
                for i in range(10):
                    color = colors[i % len(colors)]
                    self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])  # LED izquierdo
                    time.sleep(0.1)
                    self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])  # LED derecho
                    time.sleep(0.2)

            elif led_pattern == "flash_multicolor":
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
                for _ in range(8):
                    color = random.choice(colors)
                    self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
                    self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
                    time.sleep(0.2)
                    self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                    self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
                    time.sleep(0.1)

            elif led_pattern == "blue_pulse":
                for i in range(15):
                    intensity = int(255 * (0.5 + 0.5 * abs(((i % 10) - 5) / 5)))
                    self.mbot.doRGBLedOnBoard(0, 0, 0, intensity)
                    self.mbot.doRGBLedOnBoard(1, 0, 0, intensity)
                    time.sleep(0.2)

            elif led_pattern == "yellow_blink":
                for _ in range(6):
                    self.mbot.doRGBLedOnBoard(0, 255, 255, 0)
                    self.mbot.doRGBLedOnBoard(1, 255, 255, 0)
                    time.sleep(0.3)
                    self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                    self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
                    time.sleep(0.3)

            elif led_pattern == "red_dim":
                self.mbot.doRGBLedOnBoard(0, 100, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 100, 0, 0)
                time.sleep(2)

            elif led_pattern == "white_steady":
                self.mbot.doRGBLedOnBoard(0, 255, 255, 255)
                self.mbot.doRGBLedOnBoard(1, 255, 255, 255)
                time.sleep(1)

            elif led_pattern == "blue_breathing":
                for cycle in range(3):
                    # Fade in
                    for i in range(0, 255, 15):
                        self.mbot.doRGBLedOnBoard(0, 0, 0, i)
                        self.mbot.doRGBLedOnBoard(1, 0, 0, i)
                        time.sleep(0.05)
                    # Fade out
                    for i in range(255, 0, -15):
                        self.mbot.doRGBLedOnBoard(0, 0, 0, i)
                        self.mbot.doRGBLedOnBoard(1, 0, 0, i)
                        time.sleep(0.05)

            # Apagar LEDs al final
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

        except Exception as e:
            print(f"❌ Error en LEDs {led_pattern}: {e}")

    def _do_sound(self, sound_type):
        """Reproduce sonidos del buzzer"""
        if not self.mbot or not sound_type:
            return

        try:
            if sound_type == "beep_happy":
                notes = [523, 659, 783, 1047]  # Do, Mi, Sol, Do octava
                for note in notes:
                    self.mbot.doBuzzer(note, 200)
                    time.sleep(0.25)

            elif sound_type == "beep_fast":
                for _ in range(5):
                    self.mbot.doBuzzer(800, 100)
                    time.sleep(0.15)

            elif sound_type == "beep_low":
                self.mbot.doBuzzer(200, 500)
                time.sleep(0.6)

            elif sound_type == "beep_confused":
                notes = [400, 350, 300, 250]
                for note in notes:
                    self.mbot.doBuzzer(note, 200)
                    time.sleep(0.1)

            elif sound_type == "beep_sad":
                notes = [400, 350, 300]
                for note in notes:
                    self.mbot.doBuzzer(note, 400)
                    time.sleep(0.3)

        except Exception as e:
            print(f"❌ Error en sonido {sound_type}: {e}")

    def perform_spin(self):
        """Giro completo con efectos"""
        self.perform_gesture("excited")

    def perform_dance(self):
        """Secuencia de baile"""
        if not self.mbot:
            return

        print("💃 ¡Iniciando baile!")
        try:
            # Secuencia de baile
            moves = [
                (100, -100, 0.5),   # Giro derecha
                (-100, 100, 0.5),   # Giro izquierda
                (150, 150, 0.3),    # Adelante rápido
                (-150, -150, 0.3),  # Atrás rápido
                (100, -100, 1.0),   # Giro completo
            ]

            for left, right, duration in moves:
                self.mbot.doMove(left, right)
                # LEDs de colores mientras baila
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
                color = random.choice(colors)
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
        self.perform_gesture("excited")

    def stop_gesture(self):
        """Detiene el gesto actual"""
        if self.is_performing_gesture and self.gesture_thread:
            self.is_performing_gesture = False
            # Detener movimiento inmediatamente
            if self.mbot:
                self.mbot.doMove(0, 0)
                self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

    def cleanup(self):
        """Limpia recursos del mBot"""
        self.stop_gesture()
        if self.mbot:
            self.mbot.doMove(0, 0)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
            self.mbot.close()

if __name__ == "__main__":
    # Test del controlador
    controller = MBotController()

    if controller.mbot:
        print("🧪 Probando gestos...")

        # Probar algunos gestos
        test_gestures = ["happy", "excited", "thinking"]

        for gesture in test_gestures:
            print(f"Probando gesto: {gesture}")
            controller.perform_gesture(gesture)
            time.sleep(3)

        # Probar comandos
        controller.execute_command("forward")
        time.sleep(2)
        controller.execute_command("spin")

        controller.cleanup()
    else:
        print("❌ No se pudo conectar al mBot para las pruebas")
