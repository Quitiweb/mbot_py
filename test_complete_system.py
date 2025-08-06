#!/usr/bin/env python3
"""
Test completo del sistema mBot Asistente de Voz
Simula el flujo completo sin usar micrófono real
"""

from ai_brain import AIBrain
from mbot_controller import MBotController
from gesture_engine import GestureEngine
import time

def test_complete_system():
    """Prueba el sistema completo simulando conversaciones"""
    print("🎉 PRUEBA COMPLETA DEL SISTEMA MBOT")
    print("=" * 50)

    # Inicializar todos los componentes
    print("🔧 Inicializando componentes...")
    ai_brain = AIBrain()
    mbot_controller = MBotController()
    gesture_engine = GestureEngine(mbot_controller)

    if not mbot_controller.mbot:
        print("❌ mBot no conectado")
        return

    print("✅ Todos los componentes inicializados")

    # Simular el saludo inicial
    print("\n🤖 Simulando saludo inicial...")
    gesture_engine.set_emotion("happy", 3)
    time.sleep(3)

    # Conversaciones de prueba que simulan uso real
    conversations = [
        {
            "user": "Hola robot",
            "description": "Saludo inicial - debe responder amigablemente y hacer gesto alegre"
        },
        {
            "user": "¿cómo estás hoy?",
            "description": "Pregunta sobre estado - debe mostrar emoción y gestos"
        },
        {
            "user": "muévete hacia adelante",
            "description": "Comando directo - debe moverse físicamente hacia adelante"
        },
        {
            "user": "puedes bailar para mí",
            "description": "Solicitud de baile conversacional - debe responder y hacer gesto"
        },
        {
            "user": "baila",
            "description": "Comando directo de baile - debe ejecutar secuencia completa"
        },
        {
            "user": "gira a la derecha",
            "description": "Comando de giro - debe girar físicamente"
        },
        {
            "user": "para ahora",
            "description": "Comando de parada - debe detenerse inmediatamente"
        },
        {
            "user": "¿qué tal si hacemos un espectáculo de luces?",
            "description": "Conversación sobre luces - debe responder y gesticular"
        },
        {
            "user": "luz",
            "description": "Comando directo de luces - debe hacer espectáculo"
        }
    ]

    for i, conv in enumerate(conversations, 1):
        print(f"\n{'='*60}")
        print(f"🎬 ESCENARIO {i}/{len(conversations)}")
        print(f"📝 {conv['description']}")
        print(f"{'='*60}")

        user_input = conv["user"]
        print(f"👤 Usuario: \"{user_input}\"")

        # 1. Modo escucha (simular activación)
        print("👂 Activando modo escucha...")
        gesture_engine.listening_mode()
        time.sleep(1)

        # 2. Modo pensando
        print("🤔 Procesando con IA...")
        gesture_engine.thinking_mode(1)
        time.sleep(1)

        # 3. Procesar con IA
        result = ai_brain.process_input(user_input)

        print(f"🧠 Tipo de respuesta: {result['type']}")
        print(f"🤖 Respuesta: {result['response']}")
        print(f"😊 Emoción detectada: {result['emotion']}")

        # 4. Ejecutar respuesta según tipo
        if result['type'] == 'command':
            print(f"⚡ Ejecutando comando: {result['command']}")

            # Simular habla + gesto + comando en paralelo (como en main.py)
            print("🗣️  Hablando (simulado)...")
            gesture_engine.express_while_speaking(result['response'], result['emotion'])
            time.sleep(1)  # Simular tiempo de habla

            print("🤖 Ejecutando acción física...")
            mbot_controller.execute_command(result['command'])

        else:  # conversación normal
            print("💬 Respuesta conversacional")
            print("🗣️  Hablando (simulado)...")
            gesture_engine.express_while_speaking(result['response'], result['emotion'])
            time.sleep(2)  # Simular tiempo de habla

        # Pausa dramática
        print("✅ Acción completada")
        input(f"⏸️  ¿Funcionó correctamente el escenario {i}? Presiona Enter para continuar...")

    print(f"\n{'🎉'*20}")
    print("¡PRUEBA COMPLETA FINALIZADA!")
    print("Si todos los escenarios funcionaron bien:")
    print("✅ IA local responde naturalmente")
    print("✅ Robot se mueve físicamente")
    print("✅ Gestos emocionales funcionan")
    print("✅ Comandos vs conversación se distinguen correctamente")
    print("✅ LEDs y sonidos acompañan los gestos")
    print("✅ Sistema de parada funciona")
    print("\n🚀 ¡EL ASISTENTE ESTÁ LISTO PARA USO REAL!")
    print("   Ejecuta: python3 main.py")
    print(f"{'🎉'*20}")

if __name__ == "__main__":
    try:
        test_complete_system()
    except KeyboardInterrupt:
        print("\n⏹️  Prueba interrumpida")
    except Exception as e:
        print(f"❌ Error: {e}")
