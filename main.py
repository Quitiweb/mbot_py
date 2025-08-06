#!/usr/bin/env python3
"""
mBot Asistente de Voz
Sistema de conversación natural con el robot mBot usando IA
"""

import threading
import time
import signal
import sys
from audio_handler import AudioHandler
from ai_brain import AIBrain
from mbot_controller import MBotController
from gesture_engine_fixed import GestureEngineFixed
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
        """Maneja una sesión de conversación completa"""
        self.is_conversation_active = True

        # Indicar que está escuchando
        self.gesture_engine.listening_mode()
        self.audio_handler.speak("¿Sí? ¿En qué puedo ayudarte?")

        conversation_start_time = time.time()

        while self.is_conversation_active and self.is_running:
            try:
                # Escuchar comando/pregunta del usuario
                user_input = self.audio_handler.listen_for_command(timeout=10)

                if not user_input:
                    # Timeout o no se entendió
                    if time.time() - conversation_start_time > self.conversation_timeout:
                        self._end_conversation("timeout")
                        break
                    else:
                        self.audio_handler.speak("¿Puedes repetir? No te escuché bien.")
                        self.gesture_engine.set_emotion("confused", 2)
                        continue

                # Verificar comandos de salida
                if any(word in user_input.lower() for word in ["adiós", "hasta luego", "chao", "bye", "salir"]):
                    self._end_conversation("goodbye")
                    break

                # Procesar entrada con la IA
                self.gesture_engine.thinking_mode(1)
                result = self.ai_brain.process_input(user_input)

                # Ejecutar respuesta
                self._execute_ai_response(result)

                # Actualizar tiempo de conversación
                conversation_start_time = time.time()

                # Pequeña pausa antes de escuchar de nuevo
                time.sleep(0.5)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error en conversación: {e}")
                self.audio_handler.speak("Disculpa, tuve un pequeño problema. ¿Puedes intentar de nuevo?")
                self.gesture_engine.set_emotion("confused", 2)

    def _execute_ai_response(self, ai_result):
        """Ejecuta la respuesta de la IA con gestos y acciones"""
        response_type = ai_result["type"]
        response_text = ai_result["response"]
        emotion = ai_result["emotion"]

        if DEBUG_MODE:
            print(f"🧠 Tipo: {response_type}")
            print(f"😊 Emoción: {emotion}")
            print(f"🤖 Respuesta: {response_text}")

        if response_type == "command":
            # Comando directo - ejecutar acción en el mBot
            command = ai_result["command"]

            # Hablar y gesticular en paralelo
            speak_thread = threading.Thread(
                target=self.audio_handler.speak,
                args=(response_text,),
                daemon=True
            )

            gesture_thread = threading.Thread(
                target=self.gesture_engine.express_while_speaking,
                args=(response_text, emotion),
                daemon=True
            )

            command_thread = threading.Thread(
                target=self.mbot_controller.execute_command,
                args=(command,),
                daemon=True
            )

            # Ejecutar todo en paralelo para mayor realismo
            speak_thread.start()
            gesture_thread.start()
            time.sleep(0.5)  # Pequeño delay antes del comando físico
            command_thread.start()

            # Esperar a que termine de hablar
            speak_thread.join()

        else:
            # Conversación normal - solo hablar con gestos
            speak_thread = threading.Thread(
                target=self.audio_handler.speak,
                args=(response_text,),
                daemon=True
            )

            gesture_thread = threading.Thread(
                target=self.gesture_engine.express_while_speaking,
                args=(response_text, emotion),
                daemon=True
            )

            speak_thread.start()
            gesture_thread.start()
            speak_thread.join()

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
