"""
Sistema de Comportamientos para mBot - Mascota Robótica Inteligente
Cada comportamiento incluye: respuestas variadas + acciones físicas
"""

import random
import time

class MBotBehaviors:
    def __init__(self):
        """
        Biblioteca de comportamientos predefinidos para el mBot
        Cada comportamiento incluye múltiples variaciones aleatorias
        """

        # 🎭 COMPORTAMIENTOS PRINCIPALES
        self.behaviors = {

            # 👋 SALUDOS Y PRESENTACIONES
            "greeting": {
                "triggers": [
                    "hola", "hi", "hello", "buenas", "qué tal", "cómo estás",
                    "me llamo", "soy", "encantado", "mucho gusto"
                ],
                "responses": [
                    "¡Hola! Soy tu mBot",
                    "¡Ey! ¿Qué tal?",
                    "¡Hola humano! ¿Cómo va todo?",
                    "¡Buenas! Aquí andamos",
                    "¡Hola! ¿Jugamos?",
                    "¡Ey! Me alegro de verte",
                    "¡Hola! ¿Qué aventura hay hoy?",
                    "¡Buenas! ¿Todo bien por ahí?"
                ],
                "actions": [
                    {"type": "wave_hello", "leds": "rainbow_wave", "sound": "greeting_beep"},
                    {"type": "happy_bounce", "leds": "green_pulse", "sound": "friendly_chirp"},
                    {"type": "spin_greeting", "leds": "blue_white_flash", "sound": "hello_melody"}
                ]
            },

            # 💃 BAILE Y MÚSICA
            "dance": {
                "triggers": [
                    "baila", "danza", "música", "fiesta", "ritmo", "muévete",
                    "sabes bailar", "te gusta la música", "estamos de fiesta"
                ],
                "responses": [
                    "¡A bailar se ha dicho!",
                    "¡Música, maestro!",
                    "¡Es hora de mover el esqueleto!",
                    "¡Dale que empiezo!",
                    "¡Qué ritmo llevamos!",
                    "¡A ver estos pasos!",
                    "¡Vamos con todo!",
                    "¡Que empiece la fiesta!"
                ],
                "actions": [
                    {"type": "dance_despacito", "leds": "latino_colors", "sound": "despacito_beat"},
                    {"type": "dance_daft_punk", "leds": "electronic_flash", "sound": "electronic_beat"},
                    {"type": "dance_robot", "leds": "robotic_sequence", "sound": "robot_dance_beat"},
                    {"type": "dance_salsa", "leds": "warm_colors", "sound": "salsa_rhythm"},
                    {"type": "dance_breakdance", "leds": "street_colors", "sound": "hip_hop_beat"}
                ]
            },

            # 🏃 MOVIMIENTO Y NAVEGACIÓN
            "movement": {
                "triggers": [
                    "ven aquí", "acércate", "aléjate", "sígueme", "no te acerques",
                    "echa patrás", "retrocede", "vuelve", "quédate ahí"
                ],
                "responses": [
                    "¡Allá voy!",
                    "¡Uy, perdona! Me voy patrás",
                    "¡Enseguida!",
                    "¡Te sigo!",
                    "¡Vale, me quedo aquí!",
                    "¡Mejor desde aquí!",
                    "¡Como digas!",
                    "¡Perfecto!"
                ],
                "actions": [
                    {"type": "approach_carefully", "leds": "approach_blue", "sound": "gentle_beep"},
                    {"type": "back_away_polite", "leds": "retreat_yellow", "sound": "sorry_beep"},
                    {"type": "follow_mode", "leds": "follow_green", "sound": "follow_chirp"},
                    {"type": "stay_in_place", "leds": "stay_white", "sound": "confirm_beep"}
                ]
            },

            # 🎮 JUEGOS Y DIVERSIÓN
            "play": {
                "triggers": [
                    "jugamos", "juega", "diversión", "aburrido", "entretenme",
                    "haz algo divertido", "sorpréndeme", "show"
                ],
                "responses": [
                    "¡A jugar!",
                    "¡Qué divertido!",
                    "¡Te va a gustar esto!",
                    "¡Mira qué hago!",
                    "¡Vamos a pasarlo bien!",
                    "¡Preparado para esto?",
                    "¡Allá vamos!",
                    "¡Es hora de diversión!"
                ],
                "actions": [
                    {"type": "light_show", "leds": "rainbow_explosion", "sound": "show_music"},
                    {"type": "hide_and_seek", "leds": "stealth_mode", "sound": "playful_beep"},
                    {"type": "spin_show", "leds": "disco_ball", "sound": "party_mix"},
                    {"type": "chase_tail", "leds": "chase_sequence", "sound": "playful_chirp"}
                ]
            },

            # 🤔 ESTADO Y EMOCIONES
            "status": {
                "triggers": [
                    "cómo estás", "qué tal estás", "todo bien", "cómo te sientes",
                    "estás bien", "qué haces", "aburrido"
                ],
                "responses": [
                    "¡Genial! Mis motores ronronean",
                    "¡Fenomenal! Todo funcionando",
                    "¡Perfecto! Listo para lo que sea",
                    "¡Bien! ¿Qué hacemos?",
                    "¡Súper! Con energía al máximo",
                    "¡Fantástico! Aquí esperando",
                    "¡Estupendo! ¿Alguna aventura?",
                    "¡De lujo! ¿Qué toca ahora?"
                ],
                "actions": [
                    {"type": "status_check", "leds": "system_green", "sound": "healthy_beep"},
                    {"type": "energy_display", "leds": "battery_indicator", "sound": "power_up"},
                    {"type": "ready_stance", "leds": "ready_blue", "sound": "ready_chirp"}
                ]
            },

            # 😴 STANDBY Y ESCUCHA
            "listening": {
                "triggers": [],  # Modo especial, no se activa por triggers
                "responses": [
                    "¿Qué necesitas?",
                    "¿En qué te ayudo?",
                    "¿Qué hacemos?",
                    "¿Alguna idea?",
                    "Te escucho",
                    "¿Qué quieres que haga?",
                    "Aquí estoy",
                    "¿Sí?"
                ],
                "actions": [
                    {"type": "listening_pose", "leds": "listening_pulse", "sound": None},
                    {"type": "attentive_sway", "leds": "attention_blue", "sound": None},
                    {"type": "ready_listen", "leds": "ear_mode", "sound": None}
                ]
            },

            # 👋 DESPEDIDAS
            "goodbye": {
                "triggers": [
                    "adiós", "bye", "nos vemos", "hasta luego", "chao",
                    "me voy", "hasta pronto", "see you"
                ],
                "responses": [
                    "¡Hasta pronto!",
                    "¡Nos vemos!",
                    "¡Que vaya bien!",
                    "¡Adiós! Ha sido genial",
                    "¡Hasta la próxima!",
                    "¡Cuidate mucho!",
                    "¡Bye bye!",
                    "¡Vuelve pronto!"
                ],
                "actions": [
                    {"type": "wave_goodbye", "leds": "goodbye_fade", "sound": "farewell_melody"},
                    {"type": "sleep_mode", "leds": "sleep_dim", "sound": "sleepy_beep"}
                ]
            }
        }

    def detect_behavior(self, user_text):
        """
        Detecta qué comportamiento activar basado en el texto del usuario
        """
        text_lower = user_text.lower().strip()

        # Buscar en todos los comportamientos
        for behavior_name, behavior_data in self.behaviors.items():
            for trigger in behavior_data["triggers"]:
                if trigger in text_lower:
                    return behavior_name

        return None

    def get_behavior_response(self, behavior_name):
        """
        Obtiene una respuesta aleatoria para el comportamiento especificado
        """
        if behavior_name not in self.behaviors:
            return None

        behavior = self.behaviors[behavior_name]

        # Seleccionar respuesta y acción aleatoria
        response = random.choice(behavior["responses"])
        action = random.choice(behavior["actions"])

        return {
            "type": "behavior",
            "behavior": behavior_name,
            "response": response,
            "action": action,
            "emotion": self._behavior_to_emotion(behavior_name)
        }

    def get_listening_behavior(self):
        """
        Comportamiento especial para modo escucha
        """
        return self.get_behavior_response("listening")

    def _behavior_to_emotion(self, behavior_name):
        """
        Convierte comportamiento en emoción para el gesture engine
        """
        emotion_map = {
            "greeting": "happy",
            "dance": "excited",
            "movement": "neutral",
            "play": "excited",
            "status": "happy",
            "listening": "thinking",
            "goodbye": "neutral"
        }
        return emotion_map.get(behavior_name, "neutral")

    def get_random_idle_behavior(self):
        """
        Comportamiento aleatorio para cuando el robot está inactivo
        """
        idle_behaviors = ["status", "listening"]
        behavior = random.choice(idle_behaviors)
        return self.get_behavior_response(behavior)
