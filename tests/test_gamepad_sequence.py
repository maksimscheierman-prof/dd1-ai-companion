"""Gamepad sequence tests that never create a real virtual controller."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from input.gamepad import VirtualGamepad  # noqa: E402
from main import (  # noqa: E402
    JUMP_BUTTON,
    JUMP_TAP_SECONDS,
    STICK_FORWARD_Y,
    STICK_HOLD_SECONDS,
    run_gamepad_move_sequence,
)


class RecordingGamepadBackend:
    def __init__(self, events: list[tuple]) -> None:
        self.events = events

    def connect(self) -> None:
        self.events.append(("connect",))

    def press_button(self, button: str) -> None:
        self.events.append(("press", button))

    def release_button(self, button: str) -> None:
        self.events.append(("release", button))

    def set_left_stick(self, x: float, y: float) -> None:
        self.events.append(("stick", x, y))

    def reset(self) -> None:
        self.events.append(("reset",))

    def disconnect(self) -> None:
        self.events.append(("disconnect",))


class GamepadSequenceTests(unittest.TestCase):
    def test_sequence_is_stick_then_jump_then_reset(self) -> None:
        events: list[tuple] = []

        def sleep(seconds: float) -> None:
            events.append(("sleep", seconds))

        gamepad = VirtualGamepad(RecordingGamepadBackend(events))
        gamepad.connect()
        run_gamepad_move_sequence(gamepad, sleep=sleep)
        gamepad.disconnect()

        self.assertEqual(events[0], ("connect",))
        self.assertIn(("stick", 0.0, STICK_FORWARD_Y), events)
        self.assertIn(("stick", 0.0, 0.0), events)
        self.assertIn(("press", JUMP_BUTTON), events)
        self.assertIn(("release", JUMP_BUTTON), events)
        self.assertIn(("sleep", STICK_HOLD_SECONDS), events)
        self.assertIn(("sleep", JUMP_TAP_SECONDS), events)
        self.assertGreater(STICK_HOLD_SECONDS, 0.5)
        self.assertAlmostEqual(STICK_HOLD_SECONDS, 1.0, places=1)

        stick_forward = events.index(("stick", 0.0, STICK_FORWARD_Y))
        stick_stop = events.index(("stick", 0.0, 0.0))
        jump_down = events.index(("press", JUMP_BUTTON))
        jump_up = events.index(("release", JUMP_BUTTON))
        self.assertLess(stick_forward, stick_stop)
        self.assertLess(stick_stop, jump_down)
        self.assertLess(jump_down, jump_up)
        self.assertEqual(events[-2], ("reset",))
        self.assertEqual(events[-1], ("disconnect",))
        self.assertNotIn("f2", str(events).lower())
        self.assertNotIn("f3", str(events).lower())

    def test_cleanup_on_interrupt_during_stick_hold(self) -> None:
        events: list[tuple] = []

        def sleep(seconds: float) -> None:
            events.append(("sleep", seconds))
            if seconds == STICK_HOLD_SECONDS:
                raise RuntimeError("interrupted during stick hold")

        backend = RecordingGamepadBackend(events)
        with self.assertRaises(RuntimeError):
            with VirtualGamepad(backend) as gamepad:
                run_gamepad_move_sequence(gamepad, sleep=sleep)

        self.assertEqual(events[0], ("connect",))
        self.assertEqual(events.count(("reset",)), 2)
        self.assertEqual(events[-1], ("disconnect",))
        self.assertIn(("stick", 0.0, STICK_FORWARD_Y), events)
        self.assertNotIn(("press", JUMP_BUTTON), events)


if __name__ == "__main__":
    unittest.main()
