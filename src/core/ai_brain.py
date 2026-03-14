import requests
from config import *
from .mbot_behaviors import MBotBehaviors

class AIBrain:
    def __init__(self):
        # Configurar Ollama local
        self.ollama_url = OLLAMA_URL
        self.model_name = OLLAMA_MODEL_NAME

        # Sistema de comportamientos
        self.behaviors = MBotBehaviors()

        # Historial de conversación (más corto)
        self.conversation_history = [
            {"role": "system", "content": ROBOT_PERSONALITY}
        ]

        # Mantener solo los últimos 4 intercambios para respuestas más cortas
        self.max_history = 4

        # Comandos de movimiento físico inmediato
        self.movement_commands = {
            "echa patrás": "backward",
            "retrocede": "backward",
            "aléjate": "backward",
            "no te acerques": "backward",
            "para": "stop",
            "detente": "stop",
            "quédate ahí": "stop",
            "ven aquí": "forward",
            "acércate": "forward",
            "sígueme": "follow"
        }

    def process_input(self, user_text):
        """
        Procesamiento inteligente: Comportamientos -> Comandos -> IA Fallback
        """

        # 1️⃣ PRIORIDAD: Comandos de movimiento físico inmediato
        movement_cmd = self._check_movement_command(user_text)
        if movement_cmd:
            return self._handle_movement_command(movement_cmd, user_text)

        # 2️⃣ COMPORTAMIENTOS PREDEFINIDOS (más natural)
        behavior = self.behaviors.detect_behavior(user_text)
        if behavior:
            return self.behaviors.get_behavior_response(behavior)

        # 3️⃣ IA como FALLBACK (respuestas cortas garantizadas)
        return self._get_ai_response(user_text)

    def _check_movement_command(self, text):
        """Detecta comandos de movimiento que requieren acción física inmediata"""
        text_lower = text.lower().strip()

        for command_phrase, action in self.movement_commands.items():
            if command_phrase in text_lower:
                return action
        return None

    def _handle_movement_command(self, action, original_text):
        """Maneja comandos de movimiento con respuestas cortas y apropiadas"""

        responses_by_action = {
            "backward": [
                "¡Uy, perdona! Me voy patrás",
                "¡Vale! Me alejo",
                "¡Perdón! Retrocedo",
                "¡Ups! Para atrás voy"
            ],
            "stop": [
                "¡Parado!",
                "¡Vale! Me quedo aquí",
                "¡Listo! Quieto como una estatua",
                "¡Perfecto! No me muevo"
            ],
            "forward": [
                "¡Allá voy!",
                "¡Ya llegando!",
                "¡Enseguida!",
                "¡Por supuesto!"
            ],
            "follow": [
                "¡Te sigo!",
                "¡Vamos!",
                "¡Tras de ti!",
                "¡A por ello!"
            ]
        }

        import random
        response = random.choice(responses_by_action.get(action, ["¡Vale!"]))

        return {
            "type": "command",
            "command": action,
            "response": response,
            "emotion": "happy",
            "immediate": True  # Acción inmediata
        }

    def _get_ai_response(self, user_text):
        """IA como último recurso - garantiza respuestas cortas"""

        # Prompt específico para forzar respuestas cortas
        short_prompt = f"""
Contexto: Eres mBot, robot de Makeblock. El usuario dice: "{user_text}"

RESPONDE EN MÁXIMO 8 PALABRAS. Sin emoticonos. Sé amigable pero directo.

Si hablan de:
- Saludar: "¡Hola! ¿Qué hacemos?"
- Bailar: "¡A bailar se ha dicho!"
- Jugar: "¡Qué divertido! ¡Vamos!"
- Estado: "¡Genial! Todo funcionando"
- Otros: Respuesta corta apropiada

Respuesta:"""

        try:
            # Limpiar historial si está muy largo
            if len(self.conversation_history) > self.max_history * 2:
                self.conversation_history = [
                    {"role": "system", "content": ROBOT_PERSONALITY}
                ]

            response = self._call_ollama(short_prompt)

            # Limpiar respuesta de emoticonos y hacer más corta
            clean_response = self._clean_response(response)

            # Detectar emoción simple
            emotion = self._detect_simple_emotion(clean_response)

            return {
                "type": "conversation",
                "response": clean_response,
                "emotion": emotion
            }

        except Exception as e:
            print(f"Error en IA: {e}")
            # Respuesta de emergencia
            return {
                "type": "conversation",
                "response": "¡Hola! ¿Qué necesitas?",
                "emotion": "neutral"
            }

    def _clean_response(self, response):
        """Limpia la respuesta de emoticonos y la hace más corta"""

        # Eliminar emoticonos y símbolos comunes
        emoji_patterns = [
            '👤', '🤖', '😊', '😄', '🎵', '🚀', '✨', '🎭', '🕺', '💃',
            '🎉', '🎊', '⚡', '🔥', '💫', '🌟', '❤️', '💙', '💚', '💛',
            '🧠', '👋', '🎮', '🎯', '📱', '💻', '🔧', '⚙️'
        ]

        for emoji in emoji_patterns:
            response = response.replace(emoji, '')

        # Eliminar descripciones de emoticonos en texto
        response = response.replace('cohete que despega', '')
        response = response.replace('robot bailando', '')
        response = response.replace('caras sonrientes', '')

        # Limpiar espacios extra
        response = ' '.join(response.split())

        # Forzar máximo 15 palabras
        words = response.split()
        if len(words) > 15:
            response = ' '.join(words[:15])

        return response.strip()

    def _detect_simple_emotion(self, response):
        """Detección simple de emociones"""
        response_lower = response.lower()

        if any(word in response_lower for word in ["genial", "fantástico", "perfecto", "excelente"]):
            return "happy"
        elif any(word in response_lower for word in ["vamos", "bailar", "divertido", "jugar"]):
            return "excited"
        elif any(word in response_lower for word in ["perdona", "sorry", "ups"]):
            return "confused"
        else:
            return "neutral"

    def get_listening_response(self):
        """Respuesta especial para modo escucha"""
        return self.behaviors.get_listening_behavior()

    def _call_ollama(self, prompt):
        """Llamada optimizada a Ollama"""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "max_tokens": 30,  # Forzar respuestas muy cortas
                "top_p": 0.9
            }
        }

        response = requests.post(
            self.ollama_url,
            json=payload,
            timeout=5  # Timeout más corto
        )

        if response.status_code == 200:
            return response.json()["response"].strip()
        else:
            raise Exception(f"Error Ollama: {response.status_code}")

    # Método heredado para compatibilidad
    def _check_direct_command(self, text):
        return self._check_movement_command(text)

    def _handle_direct_command(self, command, text):
        return self._handle_movement_command(command, text)

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
        """Obtiene respuesta de Ollama (IA local)"""
        try:
            # Añadir mensaje del usuario al historial
            self.conversation_history.append({"role": "user", "content": user_text})

            # Crear el prompt con el contexto de la conversación
            prompt = f"{ROBOT_PERSONALITY}\n\n"
            for msg in self.conversation_history[-5:]:  # Últimos 5 mensajes para contexto
                if msg["role"] == "system":
                    continue
                elif msg["role"] == "user":
                    prompt += f"Usuario: {msg['content']}\n"
                elif msg["role"] == "assistant":
                    prompt += f"mBot: {msg['content']}\n"

            prompt += "mBot:"

            # Llamar a Ollama
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "max_tokens": 150
                }
            }

            response = requests.post(self.ollama_url, json=payload, timeout=30)

            if response.status_code == 200:
                ai_response = response.json().get("response", "").strip()

                # Añadir respuesta al historial
                self.conversation_history.append({"role": "assistant", "content": ai_response})

                # Mantener historial limitado
                if len(self.conversation_history) > 10:
                    # Mantener system message y últimos 8 mensajes
                    self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-8:]

                return ai_response
            else:
                print(f"❌ Error de Ollama: {response.status_code} - {response.text}")
                return "Lo siento, tengo un pequeño problema técnico. ¿Puedes repetir?"

        except requests.exceptions.Timeout:
            print("❌ Timeout en Ollama")
            return "Disculpa, estoy pensando muy lentamente. ¿Puedes repetir?"
        except requests.exceptions.ConnectionError:
            print("❌ No se puede conectar a Ollama")
            return "Lo siento, no puedo procesar tu mensaje ahora. ¿Está Ollama ejecutándose?"
        except Exception as e:
            print(f"❌ Error con Ollama: {e}")
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
        if result["type"] == "command":
            print(f"� Comando: {result['command']}")
        elif result["type"] == "behavior":
            print(f"�🎭 Comportamiento: {result['behavior']}")
