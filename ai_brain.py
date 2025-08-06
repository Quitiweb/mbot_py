import openai
from config import *

class AIBrain:
    def __init__(self):
        # Configurar OpenAI
        openai.api_key = OPENAI_API_KEY

        # Historial de conversación
        self.conversation_history = [
            {"role": "system", "content": ROBOT_PERSONALITY}
        ]

        # Patrones para detectar emociones en respuestas
        self.emotion_patterns = {
            "happy": ["genial", "excelente", "fantástico", "me encanta", "perfecto", "increíble"],
            "excited": ["¡", "wow", "amazing", "emocionante", "súper", "guay"],
            "thinking": ["hmm", "veamos", "pensando", "analizar", "considerar"],
            "confused": ["no entiendo", "confuso", "extraño", "raro", "qué"],
            "sad": ["lo siento", "triste", "pena", "lamento", "desafortunadamente"],
            "neutral": []
        }

    def process_input(self, user_text):
        """Procesa la entrada del usuario y determina la respuesta y emoción"""

        # 1. Verificar si es un comando directo
        direct_command = self._check_direct_command(user_text)
        if direct_command:
            return self._handle_direct_command(direct_command, user_text)

        # 2. Procesar con ChatGPT
        response = self._get_chatgpt_response(user_text)
        emotion = self._detect_emotion(response)

        return {
            "type": "conversation",
            "response": response,
            "emotion": emotion,
            "gesture": GESTURES.get(emotion, GESTURES["neutral"])
        }

    def _check_direct_command(self, text):
        """Verifica si el texto contiene un comando directo"""
        text_lower = text.lower()

        for spanish_cmd, english_cmd in DIRECT_COMMANDS.items():
            if spanish_cmd in text_lower:
                return english_cmd
        return None

    def _handle_direct_command(self, command, original_text):
        """Maneja comandos directos del mBot"""
        responses = {
            "forward": "¡Adelante vamos! Me muevo hacia delante.",
            "backward": "Entendido, retrocediendo con cuidado.",
            "right": "Girando a la derecha, como usted ordene.",
            "left": "Virando a la izquierda, ¡allá voy!",
            "stop": "Deteniéndome inmediatamente. ¡Quieto parado!",
            "spin": "¡Hora de girar! ¿Les gusta mi baile?",
            "dance": "¡Música, maestro! ¡Es hora de bailar!",
            "light_show": "¡Preparando espectáculo de luces! ¡Qué bonito!"
        }

        emotion = "excited" if command in ["dance", "spin", "light_show"] else "happy"

        return {
            "type": "command",
            "command": command,
            "response": responses.get(command, "Comando ejecutado."),
            "emotion": emotion,
            "gesture": GESTURES.get(emotion, GESTURES["neutral"])
        }

    def _get_chatgpt_response(self, user_text):
        """Obtiene respuesta de ChatGPT"""
        try:
            # Añadir mensaje del usuario al historial
            self.conversation_history.append({"role": "user", "content": user_text})

            # Llamar a la API de OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=150,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content.strip()

            # Añadir respuesta al historial
            self.conversation_history.append({"role": "assistant", "content": ai_response})

            # Mantener historial limitado
            if len(self.conversation_history) > 10:
                # Mantener system message y últimos 8 mensajes
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-8:]

            return ai_response

        except Exception as e:
            print(f"❌ Error con ChatGPT: {e}")
            return "Lo siento, tengo un pequeño problema técnico. ¿Puedes repetir?"

    def _detect_emotion(self, text):
        """Detecta la emoción basada en el texto de respuesta"""
        text_lower = text.lower()

        # Contar coincidencias por emoción
        emotion_scores = {}

        for emotion, patterns in self.emotion_patterns.items():
            score = 0
            for pattern in patterns:
                score += text_lower.count(pattern.lower())
            emotion_scores[emotion] = score

        # Detectar emociones por patrones especiales
        if "!" in text and any(word in text_lower for word in ["genial", "excelente", "increíble"]):
            emotion_scores["excited"] = emotion_scores.get("excited", 0) + 2

        if "?" in text:
            emotion_scores["confused"] = emotion_scores.get("confused", 0) + 1

        if any(word in text_lower for word in ["hmm", "veamos", "pensemos"]):
            emotion_scores["thinking"] = emotion_scores.get("thinking", 0) + 1

        # Retornar la emoción con mayor puntaje
        if max(emotion_scores.values()) > 0:
            return max(emotion_scores, key=emotion_scores.get)

        return "neutral"

    def get_conversation_summary(self):
        """Obtiene un resumen de la conversación actual"""
        if len(self.conversation_history) <= 1:
            return "Sin conversación previa"

        messages = [msg["content"] for msg in self.conversation_history[1:]]  # Skip system message
        return " | ".join(messages[-4:])  # Últimos 4 mensajes

if __name__ == "__main__":
    # Test del cerebro de IA
    brain = AIBrain()

    # Simular algunas interacciones
    test_inputs = [
        "Hola robot",
        "muévete hacia adelante",
        "¿cómo te sientes hoy?",
        "puedes bailar para mí",
        "para ahora mismo"
    ]

    for test_input in test_inputs:
        print(f"\n👤 Usuario: {test_input}")
        result = brain.process_input(test_input)
        print(f"🤖 Respuesta: {result['response']}")
        print(f"😊 Emoción: {result['emotion']}")
        print(f"🎭 Gesto: {result['gesture']}")
