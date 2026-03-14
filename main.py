#!/usr/bin/env python3
"""Nuevo flujo simplificado del mBot."""

import random
import signal
import sys
import time

from config import (
    COMMAND_TIMEOUT,
    EXPLORATION_SETTINGS,
    FOLLOW_SETTINGS,
    VOICE_ENABLED,
    VOICE_LANGUAGE,
    WAKE_POLL_INTERVAL,
    WAKE_WORD,
)
from src.core.command_parser import Command, command_from_text
from src.core.mbot_controller import MBotController

try:
    from src.core.voice_interface import VoiceInterface
except RuntimeError:
    VoiceInterface = None  # type: ignore


class MBotExplorer:
    def __init__(self):
        self.controller = MBotController()
        self.mode = Command.EXPLORE
        self.awaiting_command = False
        self._last_sound = 0.0
        self._last_turn_direction = "left"
        self._corner_recovery_until = 0.0
        self._interaction_counter = 0
        self.voice = None
        if VOICE_ENABLED and VoiceInterface:
            try:
                self.voice = VoiceInterface(WAKE_WORD, VOICE_LANGUAGE, WAKE_POLL_INTERVAL, COMMAND_TIMEOUT)
            except RuntimeError as exc:
                print(f"⚠️ Voz deshabilitada: {exc}")
        else:
            print("ℹ️ Voz deshabilitada por configuración.")

        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, *_):
        self.shutdown()
        sys.exit(0)

    def run(self):
        print("🤖 Iniciando modo exploración autónomo")
        try:
            while True:
                self._maybe_listen()
                self._run_mode_step()
        except KeyboardInterrupt:
            self.shutdown()

    # ------------------------------------------------------------------
    def _maybe_listen(self):
        if not self.voice:
            return

        if self.awaiting_command:
            command_text = self.voice.listen_for_command()
            self._process_command_text(command_text)
            self.awaiting_command = False
            return

        heard = self.voice.listen_for_wake_word()
        if heard:
            print("👂 'EME BOT' detectado. Esperando instrucción...")
            self.controller.stop()
            self.controller.flash_leds((0, 0, 255), 0.2)
            self.awaiting_command = True

    def _process_command_text(self, text):
        if not text:
            print("❓ No entendí la orden. Sigo igual.")
            return

        command = command_from_text(text)
        if not command:
            print(f"❓ Orden desconocida: {text}")
            return

        print(f"🎯 Nuevo modo: {command.value}")
        self.mode = command
        if command == Command.DANCE:
            # Ejecutamos inmediatamente y volvemos a explorar
            self.controller.perform_dance()
            self.mode = Command.EXPLORE

    # ------------------------------------------------------------------
    def _run_mode_step(self):
        if self.mode == Command.EXPLORE:
            self._explore_step()
        elif self.mode == Command.FOLLOW:
            self._follow_step()
        elif self.mode == Command.STOP:
            self.controller.stop()
            time.sleep(0.1)

    def _explore_step(self):
        settings = EXPLORATION_SETTINGS
        front = self.controller.read_distance("front")
        left = self.controller.read_distance("left")
        right = self.controller.read_distance("right")
        down = self.controller.read_distance("down")

        # Seguridad: si el sensor inferior está configurado y no detecta suelo
        # (distancia anormalmente grande), detener motores y avisar.
        if down is not None and down > settings["lift_distance_cm"]:
            self.controller.stop()
            self.controller.flash_leds((255, 120, 0), 0.12)
            self.controller.play_sound_sequence([(880, 120), (660, 140), (880, 120)])
            time.sleep(0.2)
            return

        # Si no hay lectura frontal disponible no hacemos navegación a ciegas.
        if front is None:
            self.controller.stop()
            self.controller.flash_leds((255, 0, 0), 0.08)
            time.sleep(0.15)
            return

        # Gesto de interacción: mano cerca en frente y en ambos laterales.
        if self._is_interaction_gesture(front, left, right):
            self._interaction_counter += 1
            if self._interaction_counter >= FOLLOW_SETTINGS["interaction_hold_steps"]:
                print("🫶 Gesto detectado: pasando a modo seguimiento")
                self.controller.stop()
                self.controller.flash_leds((0, 180, 255), 0.15)
                self.controller.play_sound_sequence([(660, 90), (880, 90)])
                self.mode = Command.FOLLOW
                self._interaction_counter = 0
            time.sleep(0.1)
            return

        self._interaction_counter = 0

        if front < settings["obstacle_distance_cm"]:
            # Bloqueo frontal: retroceder y girar hacia el lado más libre.
            self.controller.stop()
            self.controller.drive_backward(settings["turn_speed"])
            time.sleep(settings["reverse_time"])

            direction = self._choose_turn_direction(left, right)
            self._last_turn_direction = direction

            if direction == "left":
                self.controller.turn_left(settings["turn_speed"])
            else:
                self.controller.turn_right(settings["turn_speed"])

            self._corner_recovery_until = time.time() + settings["corner_recovery_seconds"]
            time.sleep(settings["turn_time"])
            self.controller.stop()
            time.sleep(0.08)
            return

        # Esquina/pared lateral: corrección suave manteniendo avance.
        if right is not None and right < settings["side_obstacle_distance_cm"]:
            self.controller.drive(settings["steer_speed"] - 12, settings["steer_speed"] + 12)
            self._last_turn_direction = "left"
        elif left is not None and left < settings["side_obstacle_distance_cm"]:
            self.controller.drive(settings["steer_speed"] + 12, settings["steer_speed"] - 12)
            self._last_turn_direction = "right"
        elif time.time() < self._corner_recovery_until:
            # Tras rodear una esquina, compensamos en dirección contraria
            # para no quedarse pegado a la pared.
            if self._last_turn_direction == "left":
                self.controller.drive(settings["steer_speed"] + 10, settings["steer_speed"] - 10)
            else:
                self.controller.drive(settings["steer_speed"] - 10, settings["steer_speed"] + 10)
        else:
            self.controller.drive_forward(settings["forward_speed"])

        now = time.time()
        if now - self._last_sound > settings["sound_every_seconds"]:
            self.controller.play_random_sound()
            self._last_sound = now
        time.sleep(0.1)

    def _follow_step(self):
        settings = FOLLOW_SETTINGS
        front = self.controller.read_distance("front")
        left = self.controller.read_distance("left")
        right = self.controller.read_distance("right")

        if front is None:
            self.controller.stop()
            time.sleep(0.2)
            return

        if front < settings["min_distance_cm"]:
            self.controller.stop()
        elif front > settings["max_distance_cm"]:
            self.controller.drive_forward(settings["forward_speed"])
        else:
            self.controller.drive_forward(settings["forward_speed"])

        # Corrección de rumbo hacia el objetivo usando sensores laterales.
        if left is not None and right is not None:
            if left + settings["distance_tolerance_cm"] < right:
                self.controller.turn_left(settings["turn_speed"])
                time.sleep(0.08)
            elif right + settings["distance_tolerance_cm"] < left:
                self.controller.turn_right(settings["turn_speed"])
                time.sleep(0.08)
        elif left is not None and right is None:
            self.controller.turn_left(settings["turn_speed"])
            time.sleep(0.1)
        elif right is not None and left is None:
            self.controller.turn_right(settings["turn_speed"])
            time.sleep(0.1)
        time.sleep(0.1)

    def _choose_turn_direction(self, left, right):
        if left is None and right is None:
            return random.choice(["left", "right"])
        if left is None:
            return "left"
        if right is None:
            return "right"
        return "left" if left >= right else "right"

    def _is_interaction_gesture(self, front, left, right):
        settings = FOLLOW_SETTINGS
        in_range = settings["interaction_min_cm"] <= front <= settings["interaction_max_cm"]
        if not in_range:
            return False
        if left is None or right is None:
            return False
        return (
            settings["interaction_min_cm"] <= left <= settings["interaction_max_cm"]
            and settings["interaction_min_cm"] <= right <= settings["interaction_max_cm"]
        )

    def shutdown(self):
        print("� Apagando mBot...")
        self.controller.shutdown()
        if self.voice:
            self.voice.close()


def main():
    explorer = MBotExplorer()
    explorer.run()


if __name__ == "__main__":
    main()
