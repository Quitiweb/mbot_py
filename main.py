#!/usr/bin/env python3
"""
mBot Asistente de Voz
Sistema de conversación natural con el robot mBot usando IA
"""

import threading
import time
import signal
import sys
from src.core.audio_handler import AudioHandler
from src.core.ai_brain import AIBrain
from src.core.mbot_controller import MBotController
from src.engines.gesture_engine_fixed import GestureEngineFixed
from config import *

class MBotAssistant:
    def __init__(self):
        print("🤖 Iniciando Asistente mBot...")
        print("=" * 50)

        # Inicializar componentes
        self.audio_handler = AudioHandler()
        self.ai_brain = AIBrain()
        self.mbot_controller = MBotController(
            connection_type=MBOT_CONNECTION_TYPE,
            bluetooth_address=MBOT_BLUETOOTH_ADDRESS
        )
        self.gesture_engine = GestureEngineFixed(self.mbot_controller)

        # Estado del sistema
        self.is_running = False
        self.is_conversation_active = False
        self.conversation_timeout = 30  # segundos sin actividad

        # Configurar señales de sistema
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        print("✅ Todos los componentes inicializados")

    def _signal_handler(self, signum, frame):
        """Maneja señales del sistema para cierre limpio"""
        print(f"\\n🛑 Señal {signum} recibida. Cerrando sistema...")
        self.stop()
        sys.exit(0)

    def start(self):
        """Inicia el asistente"""
        self.is_running = True

        print("\\n🎉 ¡Asistente mBot listo!")
        print(f"🎤 Di '{ROBOT_NAME}' o 'robot' para activarme")
        print("💡 O presiona Ctrl+C para salir\\n")

        # Saludo inicial
        self.audio_handler.speak(f"¡Hola! Soy {ROBOT_NAME}, tu robot asistente. Di 'robot' para hablar conmigo.")
        self.gesture_engine.set_emotion("happy", 3)

        try:
            self._main_loop()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"❌ Error crítico: {e}")
        finally:
            self.stop()

    def _main_loop(self):
        """Bucle principal del asistente"""
        while self.is_running:
            try:
                # Escuchar palabra de activación
                if self.audio_handler.listen_for_wake_word("robot"):
                    self._handle_conversation()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error en bucle principal: {e}")
                time.sleep(1)

    def _handle_conversation(self):
        """Maneja una sesión de conversación mejorada con mejor feedback"""
        self.is_conversation_active = True

        # Activación: respuesta de la IA para determinar modo escucha
        listening_response = self.ai_brain.get_listening_response()

        # Decir la frase de activación con gesto apropiado
        self.audio_handler.speak(listening_response["response"])
        self.gesture_engine.set_emotion(listening_response["emotion"], 3)

        # MODO ESCUCHA ACTIVA - Robot "vivo" esperando
        self.gesture_engine.listening_mode()

        conversation_start_time = time.time()
        idle_start = time.time()

        while self.is_conversation_active and self.is_running:
            try:
                # Escuchar comando con timeout más largo para mejor UX
                user_input = self.audio_handler.listen_for_command(timeout=15)

                if not user_input:
                    # Si lleva mucho tiempo sin actividad, mostrar que sigue escuchando
                    idle_time = time.time() - idle_start

                    if idle_time > 10:  # Cada 10 segundos sin audio
                        # Pequeño movimiento para mostrar que está vivo
                        self.gesture_engine.idle_movement()
                        idle_start = time.time()

                    # Timeout completo de conversación
                    if time.time() - conversation_start_time > self.conversation_timeout:
                        self._end_conversation("timeout")
                        break
                    else:
                        # Mensaje de no entendido más simple
                        self.audio_handler.speak("¿Puedes repetir? No te escuché bien.")
                        self.gesture_engine.set_emotion("confused", 2)
                        continue

                # Resetear tiempo de inactividad al recibir input
                idle_start = time.time()

                # Verificar comandos de salida
                if any(word in user_input.lower() for word in ["adiós", "hasta luego", "chao", "bye", "salir"]):
                    self._end_conversation("goodbye")
                    break

                # Procesar entrada con la IA mejorada
                print(f"📝 Escuchado: {user_input}")

                # Modo pensando corto
                self.gesture_engine.thinking_mode(1)
                result = self.ai_brain.process_input(user_input)

                # Ejecutar respuesta
                self._execute_ai_response(result)

                # Actualizar tiempo de conversación
                conversation_start_time = time.time()

                # Volver a modo escucha después de responder
                time.sleep(0.5)
                self.gesture_engine.listening_mode()

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error en conversación: {e}")
                self.audio_handler.speak("Disculpa, tuve un pequeño problema. ¿Puedes intentar de nuevo?")
                self.gesture_engine.set_emotion("confused", 2)

    def _execute_ai_response(self, ai_result):
        """Ejecuta la respuesta de la IA mejorada con comportamientos"""
        response_type = ai_result["type"]
        response_text = ai_result["response"]
        emotion = ai_result["emotion"]

        if DEBUG_MODE:
            print(f"🧠 Tipo: {response_type}")
            print(f"😊 Emoción: {emotion}")
            print(f"🤖 Respuesta: {response_text}")

        # Hablar primero
        self.audio_handler.speak(response_text)

        if response_type == "command":
            # Comando directo - acción física inmediata
            command = ai_result["command"]
            print(f"🤖 Ejecutando comando: {command}")

            # Acción inmediata en paralelo al habla
            if hasattr(ai_result, 'immediate') and ai_result['immediate']:
                action_thread = threading.Thread(
                    target=self.gesture_engine.immediate_action,
                    args=(command,)
                )
                action_thread.daemon = True
                action_thread.start()
            else:
                # Comando normal
                self.mbot_controller.execute_command(command)

            # Emoción del comando
            self.gesture_engine.set_emotion(emotion, 2)

        elif response_type == "behavior":
            # Comportamiento predefinido con acción específica
            behavior_name = ai_result["behavior"]
            action = ai_result["action"]

            print(f"🎭 Ejecutando comportamiento: {behavior_name}")

            # Ejecutar acción del comportamiento
            self._execute_behavior_action(action, emotion)

        else:
            # Conversación normal - solo gesto emocional
            self.gesture_engine.set_emotion(emotion, len(response_text) * 0.3)

    def _execute_behavior_action(self, action, emotion):
        """Ejecuta acciones específicas de comportamientos"""
        action_type = action["type"]
        leds = action["leds"]
        sound = action["sound"]

        try:
            if action_type == "wave_hello":
                self._do_wave_hello()
            elif action_type == "dance_despacito":
                self._do_dance_despacito()
            elif action_type == "dance_robot":
                self._do_dance_robot()
            elif action_type == "approach_carefully":
                self._do_approach()
            elif action_type == "back_away_polite":
                self._do_polite_retreat()
            elif action_type == "light_show":
                self._do_light_show()
            else:
                # Comportamiento genérico
                self.gesture_engine.set_emotion(emotion, 3)

        except Exception as e:
            print(f"❌ Error ejecutando comportamiento: {e}")
            self.gesture_engine.set_emotion(emotion, 2)

    def _do_wave_hello(self):
        """Saludo con movimiento de ola"""
        for _ in range(3):
            self.mbot_controller.mbot.doMove(50, -50)  # Giro derecha
            self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 255, 0)  # Verde
            time.sleep(0.3)
            self.mbot_controller.mbot.doMove(-50, 50)  # Giro izquierda
            self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 255, 0)
            time.sleep(0.3)
        self.mbot_controller.mbot.doMove(0, 0)
        self.mbot_controller.mbot.doBuzzer(523, 200)  # Beep amigable

    def _do_dance_despacito(self):
        """Baile estilo despacito"""
        # Secuencia de baile latina
        moves = [
            (80, 80, 0.4),    # Adelante
            (-80, -80, 0.3),  # Atrás
            (100, -100, 0.5), # Giro derecha
            (-100, 100, 0.5), # Giro izquierda
        ]

        colors = [(255, 165, 0), (255, 0, 0), (255, 255, 0), (0, 255, 0)]
        tones = [523, 659, 784, 659]  # Do, Mi, Sol, Mi

        for i, (left, right, duration) in enumerate(moves):
            color = colors[i % len(colors)]
            tone = tones[i % len(tones)]

            self.mbot_controller.mbot.doMove(left, right)
            self.mbot_controller.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
            self.mbot_controller.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
            self.mbot_controller.mbot.doBuzzer(tone, int(duration * 300))
            time.sleep(duration)

        self.mbot_controller.mbot.doMove(0, 0)

    def _do_dance_robot(self):
        """Baile robótico"""
        # Movimientos mecánicos precisos
        for _ in range(2):
            # Secuencia robótica
            self.mbot_controller.mbot.doMove(100, 100)  # Adelante preciso
            self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 0, 255)  # Azul
            self.mbot_controller.mbot.doBuzzer(800, 200)
            time.sleep(0.6)

            self.mbot_controller.mbot.doMove(0, 0)  # Parada precisa
            time.sleep(0.2)

            self.mbot_controller.mbot.doMove(100, -100)  # Giro 90°
            self.mbot_controller.mbot.doRGBLedOnBoard(1, 255, 255, 255)  # Blanco
            self.mbot_controller.mbot.doBuzzer(600, 200)
            time.sleep(0.4)

        self.mbot_controller.mbot.doMove(0, 0)

    def _do_approach(self):
        """Acercarse cuidadosamente"""
        self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 255, 0)  # Verde: seguro
        self.mbot_controller.mbot.doMove(60, 60)  # Velocidad moderada
        time.sleep(2)
        self.mbot_controller.mbot.doMove(0, 0)
        self.mbot_controller.mbot.doBuzzer(440, 150)  # Beep suave

    def _do_polite_retreat(self):
        """Retroceder educadamente"""
        self.mbot_controller.mbot.doRGBLedOnBoard(0, 255, 255, 0)  # Amarillo: precaución
        self.mbot_controller.mbot.doRGBLedOnBoard(1, 255, 255, 0)
        self.mbot_controller.mbot.doBuzzer(300, 200)  # Beep de disculpa
        self.mbot_controller.mbot.doMove(-80, -80)
        time.sleep(1.5)
        self.mbot_controller.mbot.doMove(0, 0)

    def _do_light_show(self):
        """Espectáculo de luces"""
        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (255, 255, 0), (255, 0, 255), (0, 255, 255),
            (255, 255, 255)
        ]

        for color in colors:
            self.mbot_controller.mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
            self.mbot_controller.mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
            time.sleep(0.3)

        # Apagar
        self.mbot_controller.mbot.doRGBLedOnBoard(0, 0, 0, 0)
        self.mbot_controller.mbot.doRGBLedOnBoard(1, 0, 0, 0)

    def _end_conversation(self, reason="goodbye"):
        """Termina la conversación actual"""
        self.is_conversation_active = False

        if reason == "goodbye":
            farewell_messages = [
                "¡Hasta luego! Fue un placer hablar contigo.",
                "¡Adiós! Di 'robot' cuando quieras hablar de nuevo.",
                "¡Nos vemos! Estaré aquí cuando me necesites."
            ]
            import random
            message = random.choice(farewell_messages)
            self.audio_handler.speak(message)
            self.gesture_engine.set_emotion("happy", 3)

        elif reason == "timeout":
            self.audio_handler.speak("Me quedo esperando. Di 'robot' si quieres hablar conmigo.")
            self.gesture_engine.set_emotion("neutral", 1)

        print("💭 Conversación terminada. Esperando nueva activación...")

    def stop(self):
        """Detiene el asistente de forma limpia"""
        print("\\n🛑 Deteniendo asistente...")

        self.is_running = False
        self.is_conversation_active = False

        # Detener componentes
        if hasattr(self, 'gesture_engine'):
            self.gesture_engine.stop_all()

        if hasattr(self, 'audio_handler'):
            self.audio_handler.stop_speaking()

        if hasattr(self, 'mbot_controller'):
            self.mbot_controller.cleanup()

        print("✅ Sistema detenido correctamente")

    def get_status(self):
        """Obtiene el estado actual del sistema"""
        return {
            "running": self.is_running,
            "conversation_active": self.is_conversation_active,
            "current_emotion": self.gesture_engine.get_current_emotion() if hasattr(self, 'gesture_engine') else "unknown",
            "speaking": self.audio_handler.is_currently_speaking() if hasattr(self, 'audio_handler') else False,
            "listening": self.audio_handler.is_currently_listening() if hasattr(self, 'audio_handler') else False,
            "mbot_connected": self.mbot_controller.mbot is not None if hasattr(self, 'mbot_controller') else False
        }

def main():
    """Función principal"""
    print("🚀 Iniciando mBot Asistente de Voz v1.0")
    print("Desarrollado para hacer el mBot más humano y amigable")
    print("=" * 60)

    # Verificar configuración
    if OPENAI_API_KEY == "tu-api-key-aqui":
        print("⚠️  ADVERTENCIA: No se ha configurado OPENAI_API_KEY")
        print("   Edita config.py y añade tu clave de OpenAI")
        print("   O configura la variable de entorno OPENAI_API_KEY")

    try:
        # Crear y iniciar asistente
        assistant = MBotAssistant()
        assistant.start()

    except Exception as e:
        print(f"💥 Error crítico al iniciar: {e}")
        print("Verifica que:")
        print("- El mBot esté conectado por USB")
        print("- Tengas micrófono y altavoces funcionando")
        print("- Las dependencias estén instaladas (pip install -r requirements.txt)")
        return 1

    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
