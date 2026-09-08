"""Sequence tests that never send real Windows keyboard input."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from input.keyboard import Keyboard  # noqa: E402
from main import (  # noqa: E402
    MOVE_HOLD_SECONDS,
    SELECT_KEY,
    SELECT_PAUSE_SECONDS,
    SELECT_TAP_SECONDS,
    MOVE_KEY,
    run_player2_move_sequence,
)


class RecordingBackend:
    def __init__(self, events: list[tuple[str, object]]) -> None:
        self.events = events

    def key_down(self, key: str) -> None:
        self.events.append(("down", key))

    def key_up(self, key: str) -> None:
        self.events.append(("up", key))


class Player2SequenceTests(unittest.TestCase):
    def test_sequence_is_f3_then_hold_w(self) -> None:
        events: list[tuple[str, object]] = []

        def sleep(seconds: float) -> None:
            events.append(("sleep", seconds))

        keyboard = Keyboard(RecordingBackend(events), sleep=sleep)
        run_player2_move_sequence(keyboard, sleep=sleep)

        key_events = [item for item in events if item[0] in ("down", "up")]
        self.assertEqual(
            key_events,
            [
                ("down", SELECT_KEY),
                ("up", SELECT_KEY),
                ("down", MOVE_KEY),
                ("up", MOVE_KEY),
            ],
        )

        sleeps = [item[1] for item in events if item[0] == "sleep"]
        self.assertIn(SELECT_TAP_SECONDS, sleeps)
        self.assertIn(SELECT_PAUSE_SECONDS, sleeps)
        self.assertIn(MOVE_HOLD_SECONDS, sleeps)
        self.assertGreaterEqual(SELECT_PAUSE_SECONDS, 0.3)
        self.assertLessEqual(SELECT_PAUSE_SECONDS, 0.5)
        self.assertAlmostEqual(MOVE_HOLD_SECONDS, 1.0, places=1)

    def test_w_is_released_if_hold_is_interrupted(self) -> None:
        events: list[tuple[str, object]] = []

        def sleep(seconds: float) -> None:
            events.append(("sleep", seconds))
            if seconds == MOVE_HOLD_SECONDS:
                raise RuntimeError("interrupted during W hold")

        keyboard = Keyboard(RecordingBackend(events), sleep=sleep)
        with self.assertRaises(RuntimeError):
            run_player2_move_sequence(keyboard, sleep=sleep)

        self.assertEqual(events.count(("down", MOVE_KEY)), 1)
        self.assertEqual(events.count(("up", MOVE_KEY)), 1)
        self.assertIn(("up", MOVE_KEY), events)
        down_at = events.index(("down", MOVE_KEY))
        up_at = events.index(("up", MOVE_KEY))
        self.assertGreater(up_at, down_at)
        self.assertEqual(keyboard._held, set())


if __name__ == "__main__":
    unittest.main()
