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
        distance = self.controller.read_distance("front")

        if distance is None:
            self.controller.drive_forward(settings["forward_speed"])
            time.sleep(0.2)
            return

        if distance < settings["obstacle_distance_cm"]:
            self.controller.stop()
            self.controller.play_random_sound()
            self.controller.drive_backward(settings["turn_speed"])
            time.sleep(settings["reverse_time"])
            direction = self._random_turn_direction()
            if direction == "left":
                self.controller.turn_left(settings["turn_speed"])
            else:
                self.controller.turn_right(settings["turn_speed"])
            time.sleep(settings["turn_time"])
            self.controller.stop()
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
            self.controller.stop()
        else:
            self.controller.drive_forward(settings["forward_speed"])

        if left and not right:
            self.controller.turn_left(settings["turn_speed"])
            time.sleep(0.1)
        elif right and not left:
            self.controller.turn_right(settings["turn_speed"])
            time.sleep(0.1)
        time.sleep(0.1)

    def _random_turn_direction(self):
        return random.choice(["left", "right"])

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
