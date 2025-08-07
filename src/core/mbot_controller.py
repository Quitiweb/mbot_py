import threading
import time
import random
from ..protocols.mbot_original_protocol import MBotOriginalProtocol
from config import *

class MBotController:
    def __init__(self, connection_type="auto", bluetooth_address=None):
        """
        Inicializa el controlador mBot con soporte Bluetooth y USB

        Args:
            connection_type: "auto", "usb", "bluetooth"
            bluetooth_address: Dirección MAC del mBot (opcional)
        """
        try:
            print(f"🔗 Intentando conectar mBot ({connection_type})...")
            self.mbot = MBotOriginalProtocol(connection_type)
            print(f"✅ mBot conectado correctamente via {self.mbot.connection_type}")
        except Exception as e:
            print(f"❌ Error conectando mBot: {e}")
            print("💡 Sugerencias:")
            print("   - Para Bluetooth: Asegúrate de que el mBot esté emparejado")
            print("   - Para USB: Verifica la conexión USB y drivers CH340")
            print("   - Prueba con: python3 test_connection.py")
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
