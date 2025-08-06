#!/usr/bin/env python3
"""
Investigación profunda del bucle infinito - Comando por comando
"""

import time
import asyncio
import threading
from mbot_final import MBotFinal

def test_each_command_individually():
    """Prueba cada comando individual para encontrar el culpable"""
    print("🔍 INVESTIGACIÓN COMANDO POR COMANDO")
    print("=" * 50)
    
    try:
        mbot = MBotFinal(connection_type="auto")
        print(f"✅ Conectado por: {mbot.connection_type}")
        
        commands_to_test = [
            ("LED Rojo", lambda: mbot.doRGBLedOnBoard(0, 255, 0, 0)),
            ("LED Verde", lambda: mbot.doRGBLedOnBoard(0, 0, 255, 0)),
            ("LED Azul", lambda: mbot.doRGBLedOnBoard(0, 0, 0, 255)),
            ("LED Apagar", lambda: mbot.doRGBLedOnBoard(0, 0, 0, 0)),
            ("Mover Adelante", lambda: mbot.doMove(100, 100)),
            ("Mover Atrás", lambda: mbot.doMove(-100, -100)),
            ("Parar", lambda: mbot.doMove(0, 0)),
            ("Giro Derecha", lambda: mbot.doMove(100, -100)),
            ("Giro Izquierda", lambda: mbot.doMove(-100, 100)),
            ("Buzzer 440Hz", lambda: mbot.doBuzzer(440, 300)),
            ("Buzzer 880Hz", lambda: mbot.doBuzzer(880, 300)),
            ("Motor Izq Solo", lambda: mbot.doMotor(9, 100)),
            ("Motor Der Solo", lambda: mbot.doMotor(10, 100)),
        ]
        
        for i, (name, cmd_func) in enumerate(commands_to_test):
            print(f"\n🧪 {i+1}/{len(commands_to_test)}: {name}")
            print("   Ejecutando comando...")
            
            try:
                cmd_func()
                print("   ✅ Comando enviado")
                
                print("   ⏳ Esperando 2 segundos...")
                time.sleep(2)
                
                print("   🛑 Enviando STOP...")
                mbot.doMove(0, 0)  # Parar movimiento
                mbot.doRGBLedOnBoard(0, 0, 0, 0)  # Apagar LEDs
                
                print("   ✅ Comando completado sin problemas")
                
            except Exception as e:
                print(f"   ❌ ERROR en comando {name}: {e}")
            
            # Pausa entre comandos
            print("   ⏸️  Pausa de seguridad...")
            time.sleep(1)
        
        print("\n🏁 TODOS LOS COMANDOS INDIVIDUALES PROBADOS")
        mbot.close()
        
    except Exception as e:
        print(f"❌ Error general: {e}")

def test_problematic_combinations():
    """Prueba combinaciones específicas que podrían causar problemas"""
    print("\n🚨 PROBANDO COMBINACIONES PROBLEMÁTICAS")
    print("=" * 50)
    
    try:
        mbot = MBotFinal(connection_type="auto")
        
        test_cases = [
            {
                "name": "LEDs + Movimiento simultáneo",
                "commands": [
                    lambda: mbot.doRGBLedOnBoard(0, 255, 0, 0),
                    lambda: mbot.doMove(100, 100),
                ]
            },
            {
                "name": "Buzzer + Movimiento simultáneo", 
                "commands": [
                    lambda: mbot.doBuzzer(440, 1000),  # 1 segundo
                    lambda: mbot.doMove(100, 100),
                ]
            },
            {
                "name": "Todo simultáneo",
                "commands": [
                    lambda: mbot.doRGBLedOnBoard(0, 0, 255, 0),
                    lambda: mbot.doBuzzer(523, 500),
                    lambda: mbot.doMove(80, 80),
                ]
            },
            {
                "name": "Comandos rápidos consecutivos",
                "commands": [
                    lambda: mbot.doMove(100, 100),
                    lambda: mbot.doMove(-100, -100),
                    lambda: mbot.doMove(100, -100),
                    lambda: mbot.doMove(-100, 100),
                    lambda: mbot.doMove(0, 0),
                ]
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            print(f"\n🧪 CASO {i+1}: {test_case['name']}")
            
            try:
                # Ejecutar comandos
                for cmd in test_case['commands']:
                    cmd()
                    time.sleep(0.1)  # Pequeña pausa entre comandos
                
                print("   ⏳ Esperando 3 segundos para ver efectos...")
                time.sleep(3)
                
                print("   🛑 Limpiando estado...")
                mbot.doMove(0, 0)
                mbot.doRGBLedOnBoard(0, 0, 0, 0)
                
                print("   ✅ Caso completado")
                
            except Exception as e:
                print(f"   ❌ ERROR en caso {test_case['name']}: {e}")
            
            time.sleep(1)  # Pausa entre casos
        
        print("\n✅ TODAS LAS COMBINACIONES PROBADAS")
        mbot.close()
        
    except Exception as e:
        print(f"❌ Error en combinaciones: {e}")

def test_with_monitoring():
    """Test con monitoreo de la conexión BLE"""
    print("\n📡 TEST CON MONITOREO BLE")
    print("=" * 50)
    
    try:
        mbot = MBotFinal(connection_type="auto")
        
        # Verificar estado de la conexión
        print(f"🔗 Estado de conexión: {mbot.connection_type}")
        if hasattr(mbot, 'ble_client'):
            print(f"🔵 Cliente BLE: {mbot.ble_client}")
            print(f"🔵 Conectado: {mbot.ble_connected}")
        
        # Secuencia de prueba con monitoreo
        print("\n🎭 Ejecutando secuencia de prueba...")
        
        # Paso 1
        print("1️⃣ LED Verde...")
        mbot.doRGBLedOnBoard(0, 0, 255, 0)
        time.sleep(1)
        print(f"   Estado conexión: {mbot.ble_connected if hasattr(mbot, 'ble_connected') else 'N/A'}")
        
        # Paso 2
        print("2️⃣ Movimiento adelante...")
        mbot.doMove(100, 100)
        time.sleep(0.5)
        print(f"   Estado conexión: {mbot.ble_connected if hasattr(mbot, 'ble_connected') else 'N/A'}")
        
        # Paso 3
        print("3️⃣ Buzzer...")
        mbot.doBuzzer(440, 500)
        time.sleep(0.8)
        print(f"   Estado conexión: {mbot.ble_connected if hasattr(mbot, 'ble_connected') else 'N/A'}")
        
        # Paso 4 - CRÍTICO
        print("4️⃣ Movimiento atrás...")
        mbot.doMove(-80, -80)
        time.sleep(0.3)
        print(f"   Estado conexión: {mbot.ble_connected if hasattr(mbot, 'ble_connected') else 'N/A'}")
        
        # Paso 5 - PARADA
        print("5️⃣ PARADA...")
        mbot.doMove(0, 0)
        time.sleep(0.2)
        print(f"   Estado conexión: {mbot.ble_connected if hasattr(mbot, 'ble_connected') else 'N/A'}")
        
        # Verificación final
        print("6️⃣ Limpieza final...")
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        
        print("✅ Secuencia completada")
        print("🔍 ¿El robot se quedó en bucle? ¿En qué paso?")
        
        mbot.close()
        
    except Exception as e:
        print(f"❌ Error en monitoreo: {e}")

def emergency_stop_test():
    """Test de parada de emergencia"""
    print("\n🚨 TEST DE PARADA DE EMERGENCIA")
    print("=" * 50)
    
    try:
        mbot = MBotFinal(connection_type="auto")
        
        print("🚀 Iniciando secuencia que podría causar bucle...")
        mbot.doRGBLedOnBoard(0, 255, 0, 0)
        mbot.doMove(100, 100)
        mbot.doBuzzer(440, 2000)  # Buzzer largo
        
        time.sleep(2)
        
        print("🛑 PARADA DE EMERGENCIA...")
        # Múltiples comandos de parada
        for _ in range(3):
            mbot.doMove(0, 0)
            time.sleep(0.1)
        
        # Apagar todo
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        mbot.doRGBLedOnBoard(1, 0, 0, 0)
        
        print("✅ Parada de emergencia completada")
        
        mbot.close()
        
    except Exception as e:
        print(f"❌ Error en parada de emergencia: {e}")

def main():
    print("🔬 INVESTIGACIÓN PROFUNDA DEL BUCLE INFINITO")
    print("=" * 60)
    print("Este test probará cada comando individualmente")
    print("para encontrar exactamente qué causa el bucle infinito.")
    print()
    
    tests = [
        ("Comandos individuales", test_each_command_individually),
        ("Combinaciones problemáticas", test_problematic_combinations), 
        ("Monitoreo BLE", test_with_monitoring),
        ("Parada de emergencia", emergency_stop_test),
    ]
    
    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 {name}")
        input("Presiona Enter para continuar (o Ctrl+C para salir)...")
        
        try:
            test_func()
        except KeyboardInterrupt:
            print("🛑 Test interrumpido por usuario")
            break
        except Exception as e:
            print(f"❌ Error en {name}: {e}")
        
        input("¿Hubo bucle infinito en este test? Presiona Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Investigación interrumpida")
    finally:
        print("\n🏁 FIN DE LA INVESTIGACIÓN")
