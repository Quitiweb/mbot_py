#!/usr/bin/env python3
"""
Script para probar y listar las voces disponibles en el sistema
"""
import pyttsx3

def list_available_voices():
    """Lista todas las voces disponibles en el sistema"""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    print("🎤 Voces disponibles en el sistema:")
    print("=" * 50)

    spanish_voices = []

    for i, voice in enumerate(voices):
        voice_info = f"ID: {i}"
        voice_info += f"\nNombre: {voice.name}"
        voice_info += f"\nIdioma: {voice.languages if hasattr(voice, 'languages') else 'N/A'}"
        voice_info += f"\nID del sistema: {voice.id}"

        # Detectar voces en español
        is_spanish = False
        if hasattr(voice, 'languages') and voice.languages:
            for lang in voice.languages:
                if 'es' in lang.lower() or 'spanish' in lang.lower() or 'español' in lang.lower():
                    is_spanish = True
                    break

        # También buscar en el nombre
        if ('spanish' in voice.name.lower() or 'españa' in voice.name.lower() or
            'spain' in voice.name.lower() or 'es_' in voice.id.lower() or
            'monica' in voice.name.lower() or 'jorge' in voice.name.lower()):
            is_spanish = True

        if is_spanish:
            voice_info += " ⭐ ESPAÑOL"
            spanish_voices.append((i, voice))

        print(voice_info)
        print("-" * 30)

    return spanish_voices

def test_voice(voice_id, text="Hola, soy tu robot mBot. ¿Cómo estás hoy?"):
    """Prueba una voz específica"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        if voice_id < len(voices):
            engine.setProperty('voice', voices[voice_id].id)
            engine.setProperty('rate', 180)  # Velocidad
            engine.setProperty('volume', 0.8)  # Volumen

            print(f"🎵 Probando voz {voice_id}: {voices[voice_id].name}")
            print(f"💬 Texto: {text}")

            engine.say(text)
            engine.runAndWait()
            return True
        else:
            print("❌ ID de voz inválido")
            return False

    except Exception as e:
        print(f"❌ Error probando voz: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Configurador de Voz para mBot")
    print("=" * 40)

    # Listar voces
    spanish_voices = list_available_voices()

    if spanish_voices:
        print("\n🇪🇸 Voces en español encontradas:")
        for i, (voice_id, voice) in enumerate(spanish_voices):
            print(f"  {i+1}. ID {voice_id}: {voice.name}")

        print("\n🎧 Probando voces en español...")
        for voice_id, voice in spanish_voices:
            input(f"Presiona Enter para probar: {voice.name}")
            test_voice(voice_id)
    else:
        print("\n⚠️  No se encontraron voces en español instaladas.")
        print("En macOS puedes instalar voces en Configuración > Accesibilidad > Contenido Hablado")

    print("\n🔧 También puedes probar manualmente:")
    print("Ejemplo: test_voice(2) para probar la voz con ID 2")
