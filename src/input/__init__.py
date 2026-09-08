"""External input for extra local heroes (keyboard diagnostic + virtual pad)."""

from input.gamepad import GamepadUnavailable, VirtualGamepad, VGamepadBackend
from input.keyboard import Keyboard, KeyboardBackend, PydirectinputBackend

__all__ = [
    "GamepadUnavailable",
    "Keyboard",
    "KeyboardBackend",
    "PydirectinputBackend",
    "VGamepadBackend",
    "VirtualGamepad",
]
