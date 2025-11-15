"""Helpers to map texto libre a los cuatro comandos soportados."""

from enum import Enum
from typing import Optional


class Command(str, Enum):
    EXPLORE = "explore"
    FOLLOW = "follow"
    STOP = "stop"
    DANCE = "dance"


_KEYWORDS = {
    Command.EXPLORE: ["explora", "exploracion", "exploración", "modo exploracion", "modo exploración"],
    Command.FOLLOW: ["sigueme", "sígueme", "seguir", "seguimiento"],
    Command.STOP: ["para", "parate", "párate", "detente", "quieto", "stop"],
    Command.DANCE: ["baila", "baile", "bailar", "dance"],
}


def normalize(text: str) -> str:
    return text.lower().strip()


def command_from_text(text: str) -> Optional[Command]:
    """Devuelve el comando detectado en el texto o None si no coincide."""

    normalized = normalize(text)
    for command, keywords in _KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return command
    return None