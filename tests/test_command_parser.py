from src.core.command_parser import Command, command_from_text


def test_detect_explore_command():
    assert command_from_text("modo exploración") == Command.EXPLORE


def test_detect_follow_command():
    assert command_from_text("sígueme por favor") == Command.FOLLOW


def test_detect_stop_command():
    assert command_from_text("detente ya") == Command.STOP


def test_detect_dance_command():
    assert command_from_text("puedes bailar") == Command.DANCE


def test_unknown_command_returns_none():
    assert command_from_text("haz algo") is None
