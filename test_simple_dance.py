#!/usr/bin/env python3
"""
Test de baile simple y robusto para mBot
Versión que debería funcionar sin colgarse
"""

from mbot_py.lib.mBot import mBot
import time

def simple_robust_dance():
    """Baile simple pero efectivo que no se cuelga"""
    print("💃 Baile simple y robusto")
    
    try:
        mbot = mBot()
        print("✅ mBot conectado")
        
        # Secuencia de baile muy simple
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
            (100, -100, 255, 0, 255, 784, 1.0),  # giro rápido + morado + Sol
            (0, 0, 255, 255, 255, 0, 0.3),       # pausa final
        ]
        
        print("🎵 Empezando baile...")
        
        for i, (left, right, r, g, b, freq, duration) in enumerate(dance_steps):
            print(f"🎶 Paso {i+1}: mov=({left},{right}), color=({r},{g},{b}), freq={freq}")
            
            try:
                # 1. LEDs primero
                mbot.doRGBLedOnBoard(0, r, g, b)
                mbot.doRGBLedOnBoard(1, r, g, b)
                
                # 2. Movimiento
                mbot.doMove(left, right)
                
                # 3. Sonido (solo si no es 0)
                if freq > 0:
                    mbot.doBuzzer(freq, int(duration * 800))  # duración en ms
                
                # 4. Esperar
                time.sleep(duration)
                
                # 5. Parar movimiento
                mbot.doMove(0, 0)
                
                print(f"✅ Paso {i+1} completado")
                
            except Exception as e:
                print(f"❌ Error en paso {i+1}: {e}")
                # Forzar parada y continuar
                try:
                    mbot.doMove(0, 0)
                except:
                    pass
                continue
        
        # Gran final simple
        print("🎉 Gran final...")
        try:
            # Luces intermitentes
            for i in range(6):
                color = [255, 0, 0] if i % 2 == 0 else [0, 0, 255]
                mbot.doRGBLedOnBoard(0, color[0], color[1], color[2])
                mbot.doRGBLedOnBoard(1, color[0], color[1], color[2])
                
                direction = 100 if i % 2 == 0 else -100
                mbot.doMove(direction, -direction)
                time.sleep(0.3)
            
            # Parada final
            mbot.doMove(0, 0)
            mbot.doRGBLedOnBoard(0, 0, 0, 0)
            mbot.doRGBLedOnBoard(1, 0, 0, 0)
            
            # Acorde final
            mbot.doBuzzer(523, 1000)  # Do final
            
        except Exception as e:
            print(f"❌ Error en gran final: {e}")
        
        print("🎉 ¡Baile completado!")
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")
    finally:
        # Asegurar que todo esté parado
        try:
            mbot.doMove(0, 0)
            mbot.doRGBLedOnBoard(0, 0, 0, 0)
            mbot.doRGBLedOnBoard(1, 0, 0, 0)
        except:
            pass

def test_individual_components():
    """Prueba cada componente por separado para debug"""
    print("🔍 PRUEBA DE COMPONENTES INDIVIDUALES")
    
    try:
        mbot = mBot()
        print("✅ Conexión OK")
        
        # Test 1: Solo buzzer
        print("🎵 Test 1: Solo buzzer...")
        mbot.doBuzzer(523, 500)
        time.sleep(1)
        print("✅ Buzzer OK")
        
        # Test 2: Solo LEDs
        print("💡 Test 2: Solo LEDs...")
        mbot.doRGBLedOnBoard(0, 255, 0, 0)
        mbot.doRGBLedOnBoard(1, 255, 0, 0)
        time.sleep(1)
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)
        print("✅ LEDs OK")
        
        # Test 3: Solo movimiento
        print("🚗 Test 3: Solo movimiento...")
        mbot.doMove(80, -80)
        time.sleep(1)
        mbot.doMove(0, 0)
        print("✅ Movimiento OK")
        
        # Test 4: Combinación simple
        print("🎭 Test 4: Combinación simple...")
        mbot.doRGBLedOnBoard(0, 0, 255, 0)
        mbot.doRGBLedOnBoard(1, 0, 255, 0)
        mbot.doMove(60, 60)
        mbot.doBuzzer(659, 800)
        time.sleep(0.8)
        mbot.doMove(0, 0)
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)
        print("✅ Combinación OK")
        
        print("🎉 Todos los componentes funcionan correctamente")
        
    except Exception as e:
        print(f"❌ Error en componente: {e}")

if __name__ == "__main__":
    print("🤖 TEST DE BAILE ROBUSTO")
    print("=" * 30)
    
    while True:
        print("\n¿Qué quieres probar?")
        print("1. 🎵 Baile simple y robusto")
        print("2. 🔍 Test de componentes individuales")
        print("3. 🚪 Salir")
        
        choice = input("Elige (1-3): ").strip()
        
        if choice == "1":
            simple_robust_dance()
        elif choice == "2":
            test_individual_components()
        elif choice == "3":
            break
        else:
            print("❌ Opción no válida")
