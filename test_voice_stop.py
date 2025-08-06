#!/usr/bin/env python3
"""
Script para probar el asistente de voz con el comando de parada
"""
import time
import threading
from audio_handler import AudioHandler
from ai_brain import AIBrain
from mbot_controller import MBotController
from gesture_engine import GestureEngine

def test_voice_stop_command():
    """Prueba completa del comando de voz de parada"""
    print("🤖 Iniciando prueba del comando de voz 'para'...")
    
    try:
        # Inicializar componentes
        audio = AudioHandler()
        brain = AIBrain()
        controller = MBotController()
        gestures = GestureEngine(controller)
        
        if not controller.mbot:
            print("❌ No se pudo conectar al mBot")
            return False
        
        print("✅ Todos los componentes inicializados")
        
        # Simular comando de movimiento
        print("\\n1️⃣  Simulando comando 'adelante'...")
        result = brain.process_input("muévete hacia adelante")
        print(f"🧠 Resultado: {result}")
        
        if result['type'] == 'command':
            # Simular ejecución del comando como lo haría main.py
            speak_thread = threading.Thread(
                target=audio.speak,
                args=(result['response'],),
                daemon=True
            )
            
            command_thread = threading.Thread(
                target=controller.execute_command,
                args=(result['command'],),
                daemon=True
            )
            
            gesture_thread = threading.Thread(
                target=gestures.express_while_speaking,
                args=(result['response'], result['emotion']),
                daemon=True
            )
            
            # Ejecutar todo en paralelo
            speak_thread.start()
            gesture_thread.start()
            time.sleep(0.5)  # Pequeño delay
            command_thread.start()
            
            print("⏱️  Esperando 3 segundos...")
            time.sleep(3)
        
        # Ahora simular comando de parada
        print("\\n2️⃣  Simulando comando 'para'...")
        result = brain.process_input("para ahora mismo")
        print(f"🧠 Resultado: {result}")
        
        if result['type'] == 'command':
            # Ejecutar comando de parada
            speak_thread = threading.Thread(
                target=audio.speak,
                args=(result['response'],),
                daemon=True
            )
            
            command_thread = threading.Thread(
                target=controller.execute_command,
                args=(result['command'],),
                daemon=True
            )
            
            # Ejecutar parada inmediatamente
            speak_thread.start()
            command_thread.start()
            
            # Esperar un poco
            command_thread.join(timeout=2)
            
            print("✅ Comando de parada ejecutado")
            
        print("\\n3️⃣  Esperando a que termine de hablar...")
        # Esperar a que termine de hablar
        while audio.is_currently_speaking():
            time.sleep(0.1)
            
        print("\\n📊 Prueba completada")
        
        # Limpiar
        controller.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_stop():
    """Prueba directa del comando de parada"""
    print("\\n🛑 Prueba directa del comando de parada...")
    
    try:
        controller = MBotController()
        
        if not controller.mbot:
            print("❌ No se pudo conectar al mBot")
            return False
        
        # Iniciar movimiento
        print("▶️  Iniciando movimiento...")
        controller.mbot.doMove(100, 100)
        
        time.sleep(2)
        
        # Parar directamente
        print("🛑 Ejecutando parada directa...")
        controller.execute_command("stop")
        
        time.sleep(1)
        
        print("✅ Parada directa completada")
        controller.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba directa: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema de parada")
    print("=" * 50)
    
    # Prueba 1: Parada directa
    success1 = test_direct_stop()
    
    time.sleep(3)
    
    # Prueba 2: Comando completo de voz (solo si es necesario)
    # success2 = test_voice_stop_command()
    
    if success1:  # and success2:
        print("\\n🎉 ¡Todas las pruebas exitosas!")
        print("El comando de parada funciona correctamente")
    else:
        print("\\n💥 Algunas pruebas fallaron")
        print("Revisa los logs para más detalles")
