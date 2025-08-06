#!/usr/bin/env python3
"""
Investigación específica del comando de parada
"""

import time
from mbot_final import MBotFinal

def test_stop_command_variations():
    """Prueba diferentes variaciones del comando de parada"""
    print("🛑 INVESTIGACIÓN DEL COMANDO DE PARADA")
    print("=" * 50)
    
    try:
        mbot = MBotFinal(connection_type="auto")
        print(f"✅ Conectado por: {mbot.connection_type}")
        
        # Secuencia problemática identificada
        print("\n🚨 REPRODUCIENDO PROBLEMA...")
        print("1. LED Verde...")
        mbot.doRGBLedOnBoard(0, 0, 255, 0)
        
        print("2. Buzzer...")
        mbot.doBuzzer(523, 500)
        
        print("3. Movimiento...")
        mbot.doMove(80, 80)
        
        print("4. Esperando 2 segundos...")
        time.sleep(2)
        
        print("5. INTENTANDO PARAR - Método 1: doMove(0, 0)")
        mbot.doMove(0, 0)
        time.sleep(1)
        
        print("❓ ¿Se paró? Si no, probando métodos alternativos...")
        
        # Método 2: Múltiples comandos de parada
        print("6. Método 2: Múltiples doMove(0, 0)")
        for i in range(5):
            print(f"   Intento {i+1}/5...")
            mbot.doMove(0, 0)
            time.sleep(0.2)
        
        print("❓ ¿Se paró ahora?")
        time.sleep(1)
        
        # Método 3: Comandos de motor individual
        print("7. Método 3: Parar motores individualmente")
        mbot.doMotor(9, 0)   # Motor izquierdo
        mbot.doMotor(10, 0)  # Motor derecho
        time.sleep(1)
        
        print("❓ ¿Se paró con motores individuales?")
        
        # Método 4: Comando de parada con diferentes valores
        print("8. Método 4: Diferentes valores de parada")
        test_values = [
            (0, 0),
            (128, 128),    # Valor neutro en algunos protocolos
            (255, 255),    # Posible valor de parada
            (1, 1),        # Movimiento mínimo
        ]
        
        for left, right in test_values:
            print(f"   Probando doMove({left}, {right})")
            mbot.doMove(left, right)
            time.sleep(0.5)
            mbot.doMove(0, 0)
            time.sleep(0.5)
        
        print("9. Limpieza final...")
        mbot.doRGBLedOnBoard(0, 0, 0, 0)
        
        print("✅ Test completado")
        mbot.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def test_protocol_variations():
    """Prueba diferentes protocolos de parada"""
    print("\n🔬 PROBANDO PROTOCOLOS DE PARADA ALTERNATIVOS")
    print("=" * 50)
    
    try:
        mbot = MBotFinal(connection_type="auto")
        
        # Reproducir problema
        print("Iniciando movimiento...")
        mbot.doMove(100, 100)
        time.sleep(1)
        
        # Protocolo 1: Parada estándar
        print("Protocolo 1: Estándar")
        cmd1 = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 0, 0])
        result1 = mbot.write(cmd1)
        print(f"  Resultado: {result1}")
        time.sleep(1)
        
        # Protocolo 2: Con valores 128 (neutro)
        print("Protocolo 2: Neutro 128")
        cmd2 = bytes([0xff, 0x55, 0x7, 0x0, 0x2, 0x5, 128, 128])
        result2 = mbot.write(cmd2)
        print(f"  Resultado: {result2}")
        time.sleep(1)
        
        # Protocolo 3: Parada con header diferente
        print("Protocolo 3: Header alternativo")
        cmd3 = bytes([0xA5, 0x5A, 0x09, 0x00, 0x02, 0x05, 0x00, 0x00])
        result3 = mbot.write(cmd3)
        print(f"  Resultado: {result3}")
        time.sleep(1)
        
        # Protocolo 4: Comando de reset/inicialización
        print("Protocolo 4: Reset")
        cmd4 = bytes([0xff, 0x55, 0x4, 0x0, 0x2, 0xff])  # Posible comando de reset
        result4 = mbot.write(cmd4)
        print(f"  Resultado: {result4}")
        time.sleep(1)
        
        print("✅ Protocolos probados")
        mbot.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def manual_stop_test():
    """Test manual para encontrar qué funciona"""
    print("\n👨‍🔧 TEST MANUAL INTERACTIVO")
    print("=" * 50)
    
    try:
        mbot = MBotFinal(connection_type="auto")
        
        while True:
            print("\n¿Qué quieres hacer?")
            print("1. Iniciar movimiento + buzzer + LED")
            print("2. Parar con doMove(0,0)")
            print("3. Parar con motores individuales")
            print("4. Parar con protocolo alternativo")
            print("5. Apagar LEDs")
            print("6. Estado actual")
            print("7. Salir")
            
            choice = input("Elige opción: ").strip()
            
            if choice == "1":
                print("Iniciando secuencia problemática...")
                mbot.doRGBLedOnBoard(0, 0, 255, 0)
                mbot.doBuzzer(440, 1000)
                mbot.doMove(100, 100)
                print("✅ Secuencia iniciada")
                
            elif choice == "2":
                print("Parando con doMove(0,0)...")
                mbot.doMove(0, 0)
                print("✅ Comando enviado")
                
            elif choice == "3":
                print("Parando motores individuales...")
                mbot.doMotor(9, 0)
                mbot.doMotor(10, 0)
                print("✅ Motores parados")
                
            elif choice == "4":
                print("Protocolo alternativo...")
                cmd = bytes([0xA5, 0x5A, 0x09, 0x00, 0x02, 0x05, 0x00, 0x00])
                mbot.write(cmd)
                print("✅ Protocolo alternativo enviado")
                
            elif choice == "5":
                print("Apagando LEDs...")
                mbot.doRGBLedOnBoard(0, 0, 0, 0)
                mbot.doRGBLedOnBoard(1, 0, 0, 0)
                print("✅ LEDs apagados")
                
            elif choice == "6":
                print(f"Estado conexión: {mbot.connection_type}")
                if hasattr(mbot, 'ble_connected'):
                    print(f"BLE conectado: {mbot.ble_connected}")
                    
            elif choice == "7":
                break
                
            else:
                print("Opción no válida")
        
        mbot.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🔍 INVESTIGACIÓN ESPECÍFICA DEL COMANDO DE PARADA")
    print("=" * 60)
    
    tests = [
        ("Variaciones de parada", test_stop_command_variations),
        ("Protocolos alternativos", test_protocol_variations),
        ("Test manual", manual_stop_test),
    ]
    
    for name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"🧪 {name}")
        input("Presiona Enter para continuar...")
        
        try:
            test_func()
        except KeyboardInterrupt:
            print("🛑 Test interrumpido")
            break

if __name__ == "__main__":
    main()
