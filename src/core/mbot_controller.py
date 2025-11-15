import threading
import time
import random
from ..protocols.mbot_original_protocol import MBotOriginalProtocol
from config import *


class _SimulatedMBot:
    """Implementación mínima para ejecutar en modo simulación."""

    def __init__(self):
        self.connection_type = "simulation"

    def doMove(self, left_speed, right_speed):
        print(f"[SIM] Move L:{left_speed} R:{right_speed}")

    def doRGBLedOnBoard(self, index, red, green, blue):
        print(f"[SIM] LED index={index} rgb=({red},{green},{blue})")

    def doBuzzer(self, frequency, duration=0):
        print(f"[SIM] Buzzer freq={frequency} duration={duration}ms")

    def doMotor(self, port, speed):
        print(f"[SIM] Motor port={port} speed={speed}")

    def doServo(self, port, slot, angle):
        print(f"[SIM] Servo port={port} slot={slot} angle={angle}")

    def forceStop(self):
        print("[SIM] forceStop")

    def emergencyCleanup(self):
        print("[SIM] emergencyCleanup")

    def close(self):
        print("[SIM] close")

class MBotController:
    def __init__(self, connection_type="auto", bluetooth_address=None):
        """
        Inicializa el controlador mBot con soporte Bluetooth y USB

        Args:
            connection_type: "auto", "usb", "bluetooth"
            bluetooth_address: Dirección MAC del mBot (opcional)
        """
        self.is_simulation = False

        try:
            print(f"🔗 Intentando conectar mBot ({connection_type})...")
            self.mbot = MBotOriginalProtocol(connection_type)
            print(f"✅ mBot conectado correctamente via {self.mbot.connection_type}")
        except Exception as e:
            print(f"❌ Error conectando mBot: {e}")
            print("💡 Activando modo simulación: el robot real no está disponible.")
            self.mbot = _SimulatedMBot()
            self.is_simulation = True

        # Estado del robot
        self.current_gesture = None
        self.is_performing_gesture = False
        self.gesture_thread = None
        self._stop_requested = False  # Flag para parar gestos

    def execute_command(self, command):
        """Ejecuta un comando directo en el mBot"""
        if not self.mbot:
            return

        mode = "simulación" if self.is_simulation else "hardware"
        print(f"🤖 Ejecutando comando: {command} ({mode})")

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

            elif command == "follow":
                self.perform_follow()

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
            movement = gesture.get("movement", "stop")
            leds = gesture.get("leds")
            sound = gesture.get("sound")

            movement_map = {
                "attentive_pose": "stop",
                "wave_motion": "wave",
                "dance_sequence": "spin",
                "follow_mode": "slight_move",
                "happy_bounce": "bounce",
                "ready_stance": "slight_move",
                "approach_carefully": "slight_move",
                "back_away_polite": "back_away",
                "listening_pose": "stop",
            }

            movement = movement_map.get(movement, movement)

            # Ejecutar movimiento
            if movement == "bounce":
                self._simple_bounce()
            elif movement == "gentle_sway":
                self._simple_sway()
            elif movement == "slight_move":
                self._simple_move()
            elif movement == "spin":
                self._simple_spin()
            elif movement == "wave":
                self._simple_wave()
            elif movement == "head_shake":
                self._simple_head_shake()
            elif movement == "back_away":
                self._simple_back_away()
            elif movement == "stop":
                self._simple_stop()
            else:
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

    def _simple_wave(self):
        """Movimiento tipo ola con pequeños giros"""
        if self._stop_requested or not self.mbot:
            return
        for _ in range(3):
            if self._stop_requested:
                break
            self.mbot.doMove(60, -60)
            time.sleep(0.2)
            if self._stop_requested:
                break
            self.mbot.doMove(-60, 60)
            time.sleep(0.2)
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
            if not led_pattern:
                self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
                return

            palette_map = {
                "rainbow": [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
                "rainbow_wave": [(255, 0, 0), (255, 80, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255)],
                "rainbow_explosion": [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)],
                "latino_colors": [(255, 140, 0), (255, 0, 0), (255, 215, 0)],
                "electronic_flash": [(0, 255, 255), (0, 0, 255), (255, 0, 255)],
                "robotic_sequence": [(255, 255, 255), (0, 0, 255)],
                "warm_colors": [(255, 69, 0), (255, 165, 0)],
                "street_colors": [(255, 0, 255), (0, 255, 255)],
                "system_green": [(0, 255, 0)],
                "battery_indicator": [(0, 255, 0), (255, 255, 0), (255, 0, 0)],
                "ready_blue": [(0, 100, 255)],
                "listening_pulse": [(0, 120, 255)],
                "attention_blue": [(0, 0, 255)],
                "ear_mode": [(0, 180, 255)],
                "goodbye_fade": [(255, 100, 0), (0, 0, 0)],
                "sleep_dim": [(20, 20, 50)],
                "welcome_colors": [(0, 255, 120), (0, 120, 255)],
                "party_lights": [(255, 0, 255), (0, 255, 255), (255, 255, 0)],
                "follow_green": [(0, 255, 0)],
                "approach_blue": [(0, 120, 255)],
                "retreat_yellow": [(255, 255, 0)],
                "stay_white": [(255, 255, 255)],
            }

            if led_pattern == "flash_multicolor":
                colors = palette_map.get("party_lights")
                for _ in range(3):
                    for color in colors:
                        if self._stop_requested:
                            break
                        self.mbot.doRGBLedOnBoard(0, *color)
                        self.mbot.doRGBLedOnBoard(1, *color)
                        time.sleep(0.2)

            elif led_pattern == "blue_pulse":
                self.mbot.doRGBLedOnBoard(0, 0, 0, 255)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 255)
                time.sleep(1)

            elif led_pattern == "blue_breathing":
                for intensity in [50, 100, 150, 255, 150, 100, 50]:
                    if self._stop_requested:
                        break
                    self.mbot.doRGBLedOnBoard(0, 0, 0, intensity)
                    self.mbot.doRGBLedOnBoard(1, 0, 0, intensity)
                    time.sleep(0.3)

            elif led_pattern == "yellow_blink":
                for _ in range(6):
                    if self._stop_requested:
                        break
                    self.mbot.doRGBLedOnBoard(0, 255, 255, 0)
                    self.mbot.doRGBLedOnBoard(1, 255, 255, 0)
                    time.sleep(0.2)
                    self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                    self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
                    time.sleep(0.2)

            else:
                colors = palette_map.get(led_pattern, [(255, 255, 255)])
                for color in colors:
                    if self._stop_requested:
                        break
                    self.mbot.doRGBLedOnBoard(0, *color)
                    self.mbot.doRGBLedOnBoard(1, *color)
                    time.sleep(0.3)

            if not self._stop_requested:
                time.sleep(0.2)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

        except Exception as e:
            print(f"❌ Error en LEDs: {e}")

    def _simple_sound(self, sound_type):
        """Sonidos simples"""
        if self._stop_requested or not self.mbot:
            return

        try:
            sound_map = {
                "greeting_beep": "beep_happy",
                "friendly_chirp": "beep_happy",
                "hello_melody": "beep_fast",
                "despacito_beat": "beep_fast",
                "electronic_beat": "beep_fast",
                "robot_dance_beat": "beep_fast",
                "salsa_rhythm": "beep_fast",
                "hip_hop_beat": "beep_fast",
                "gentle_beep": "beep_low",
                "sorry_beep": "beep_confused",
                "follow_chirp": "beep_happy",
                "confirm_beep": "beep_happy",
                "show_music": "beep_fast",
                "playful_beep": "beep_happy",
                "party_mix": "beep_fast",
                "playful_chirp": "beep_happy",
                "healthy_beep": "beep_happy",
                "power_up": "beep_fast",
                "ready_chirp": "beep_happy",
                "farewell_melody": "beep_sad",
                "sleepy_beep": "beep_low",
                "greeting_melody": "beep_happy",
                "music_beat": "beep_fast",
                "follow_beep": "beep_happy",
            }

            mapped = sound_map.get(sound_type, sound_type)

            if mapped == "beep_happy":
                self.mbot.doBuzzer(523, 200)
                if not self._stop_requested:
                    time.sleep(0.3)
                    self.mbot.doBuzzer(659, 200)

            elif mapped == "beep_fast":
                for freq in [523, 659, 784, 1047]:
                    if self._stop_requested:
                        break
                    self.mbot.doBuzzer(freq, 150)
                    time.sleep(0.1)

            elif mapped == "beep_confused":
                self.mbot.doBuzzer(400, 300)
                if not self._stop_requested:
                    time.sleep(0.1)
                    self.mbot.doBuzzer(300, 300)

            elif mapped == "beep_sad":
                self.mbot.doBuzzer(523, 400)
                if not self._stop_requested:
                    time.sleep(0.2)
                    self.mbot.doBuzzer(392, 400)

            elif mapped == "beep_low":
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
        """Secuencia de baile simple pero espectacular (versión robusta)"""
        if not self.mbot:
            return

        print("💃 ¡Iniciando baile espectacular!")
        try:
            # Secuencia de baile robusta - basada en la versión que funciona
            dance_steps = [
                # (movimiento_izq, movimiento_der, led_r, led_g, led_b, buzzer_freq, duración)
                (60, -60, 255, 0, 0, 523, 0.8),      # giro derecha + rojo + Do
                (0, 0, 255, 100, 0, 0, 0.2),         # pausa
                (-60, 60, 0, 255, 0, 587, 0.8),      # giro izquierda + verde + Re
                (0, 0, 100, 255, 0, 0, 0.2),         # pausa
                (80, 80, 0, 0, 255, 659, 0.6),       # adelante + azul + Mi
                (0, 0, 0, 100, 255, 0, 0.2),         # pausa
                (-60, -60, 255, 255, 0, 698, 0.6),   # atrás + amarillo + Fa
                (0, 0, 255, 255, 100, 0, 0.2),       # pausa
                (80, -80, 255, 0, 255, 784, 0.8),    # giro + morado + Sol
                (0, 0, 255, 255, 255, 0, 0.2),       # pausa
                (-80, 80, 0, 255, 255, 880, 0.8),    # giro contrario + cian + La
                (0, 0, 255, 0, 100, 0, 0.2),         # pausa
                (100, 100, 255, 100, 0, 988, 0.6),   # adelante rápido + naranja + Si
                (0, 0, 100, 255, 255, 0, 0.2),       # pausa
                (-80, -80, 0, 255, 100, 523, 0.6),   # atrás + verde claro + Do
                (0, 0, 255, 255, 255, 0, 0.3),       # pausa final
            ]

            print("🎵 ¡Empezando la música y el baile!")

            for i, (left, right, r, g, b, freq, duration) in enumerate(dance_steps):
                if self._stop_requested:
                    break

                print(f"🎶 Paso {i+1}: mov=({left},{right}), color=({r},{g},{b}), freq={freq}")

                try:
                    # 1. LEDs primero
                    self.mbot.doRGBLedOnBoard(0, r, g, b)
                    self.mbot.doRGBLedOnBoard(1, r, g, b)

                    # 2. Movimiento
                    self.mbot.doMove(left, right)

                    # 3. Sonido (solo si no es 0)
                    if freq > 0:
                        self.mbot.doBuzzer(freq, int(duration * 800))  # duración en ms

                    # 4. Esperar
                    time.sleep(duration)

                    # 5. Parar movimiento
                    self.mbot.doMove(0, 0)

                    print(f"✅ Paso {i+1} completado")

                except Exception as e:
                    print(f"❌ Error en paso {i+1}: {e}")
                    # Forzar parada y continuar
                    try:
                        self.mbot.doMove(0, 0)
                    except:
                        pass
                    continue

            # Gran final simple pero efectivo
            print("� ¡Gran final!")
            try:
                # Luces intermitentes con giros
                for i in range(8):
                    if self._stop_requested:
                        break

                    color = [255, 0, 0] if i % 2 == 0 else [0, 0, 255]
                    self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
                    self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])

                    direction = 120 if i % 2 == 0 else -120
                    self.mbot.doMove(direction, -direction)
                    time.sleep(0.25)

                # Parada final
                self.mbot.doMove(0, 0)

                # Acorde final
                finale_notes = [523, 659, 784, 1047]  # Do, Mi, Sol, Do alto
                for note in finale_notes:
                    if self._stop_requested:
                        break
                    self.mbot.doBuzzer(note, 150)
                    time.sleep(0.1)

                # Nota final larga
                self.mbot.doBuzzer(523, 800)  # Do final

            except Exception as e:
                print(f"❌ Error en gran final: {e}")

            # Asegurar que todo esté parado
            self.mbot.doMove(0, 0)
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
            print("💃 ¡Baile completado!")

        except Exception as e:
            print(f"❌ Error crítico en baile: {e}")
            # Forzar parada en caso de error
            try:
                self.mbot.doMove(0, 0)
                self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 0)
            except:
                pass
                self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

    def _execute_dance_move(self, move_type, led_color):
        """Ejecuta un movimiento específico de baile"""
        if self._stop_requested or not self.mbot:
            return

        # Aplicar color de LEDs
        self.mbot.doRGBLedOnBoard(0, led_color[0], led_color[1], led_color[2])
        self.mbot.doRGBLedOnBoard(1, led_color[0], led_color[1], led_color[2])

        # Ejecutar movimiento
        if move_type == "wiggle":
            # Pequeños movimientos de lado a lado
            self.mbot.doMove(40, -40)
            time.sleep(0.15)
            self.mbot.doMove(-40, 40)
            time.sleep(0.15)
            self.mbot.doMove(0, 0)

        elif move_type == "spin_right":
            # Giro hacia la derecha
            self.mbot.doMove(80, -80)

        elif move_type == "spin_left":
            # Giro hacia la izquierda
            self.mbot.doMove(-80, 80)

        elif move_type == "full_spin":
            # Giro completo rápido
            self.mbot.doMove(120, -120)

        elif move_type == "forward":
            # Avanzar con energía
            self.mbot.doMove(100, 100)

        elif move_type == "backward":
            # Retroceder
            self.mbot.doMove(-80, -80)

        elif move_type == "back_forth":
            # Adelante y atrás rápido
            self.mbot.doMove(60, 60)
            time.sleep(0.2)
            self.mbot.doMove(-60, -60)
            time.sleep(0.2)
            self.mbot.doMove(0, 0)

        elif move_type == "celebration":
            # Movimiento de celebración
            for _ in range(3):
                self.mbot.doMove(100, -100)
                time.sleep(0.1)
                self.mbot.doMove(-100, 100)
                time.sleep(0.1)
            self.mbot.doMove(0, 0)

        elif move_type == "final_pose":
            # Pose final dramática
            self.mbot.doMove(0, 0)  # Parar en pose

        elif move_type == "pause":
            # Pausa musical
            self.mbot.doMove(0, 0)

    def _grand_finale(self):
        """Gran final espectacular"""
        if self._stop_requested or not self.mbot:
            return

        # Secuencia de luces y sonidos finales
        finale_colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)
        ]

        finale_notes = [523, 659, 784, 1047]  # Acorde final

        # Efectos de luces rápidos
        for i in range(8):
            if self._stop_requested:
                break
            color = finale_colors[i % len(finale_colors)]
            self.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
            self.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])

            # Giro rápido
            self.mbot.doMove(150, -150)
            time.sleep(0.1)

        # Acorde final
        for note in finale_notes:
            if self._stop_requested:
                break
            self.mbot.doBuzzer(note, 200)
            time.sleep(0.1)

        # Nota final larga
        self.mbot.doBuzzer(523, 1000)  # Do final largo
        self.mbot.doMove(0, 0)  # Parar en pose final

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

    def perform_follow(self):
        """Modo seguir: pequeños avances y paradas"""
        if not self.mbot:
            return

        print("🚶 Modo seguir activado")
        try:
            for _ in range(3):
                if self._stop_requested:
                    break
                self.mbot.doRGBLedOnBoard(0, 0, 255, 0)
                self.mbot.doRGBLedOnBoard(1, 0, 255, 0)
                self.mbot.doMove(80, 80)
                time.sleep(0.6)
                self.mbot.doMove(0, 0)
                time.sleep(0.2)
        finally:
            self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
            self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

    def stop_gesture(self):
        """Detiene el gesto actual inmediatamente - VERSIÓN MEJORADA"""
        print("🛑 Deteniendo gesto actual...")

        # Marcar que debe detenerse
        self._stop_requested = True
        self.is_performing_gesture = False

        # Detener con el método mejorado
        if self.mbot:
            if hasattr(self.mbot, 'forceStop'):
                self.mbot.forceStop()
            else:
                self.mbot.doMove(0, 0)

            # Limpieza adicional
            if hasattr(self.mbot, 'emergencyCleanup'):
                self.mbot.emergencyCleanup()
            else:
                self.mbot.doRGBLedOnBoard(0, 0, 0, 0)
                self.mbot.doRGBLedOnBoard(1, 0, 0, 0)

            print("✅ mBot detenido con método mejorado")

    def stop_current_gesture(self):
        """Alias para stop_gesture - compatibilidad"""
        self.stop_gesture()

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
