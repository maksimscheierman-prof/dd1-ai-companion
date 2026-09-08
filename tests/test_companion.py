"""Companion control tests that never create a real virtual controller."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from control.companion import (  # noqa: E402
    CompanionController,
    CompanionError,
    CompanionManager,
)
from input.gamepad import VirtualGamepad  # noqa: E402
from main import (  # noqa: E402
    THREE_ACTION_SECONDS,
    run_companion_demo_sequence,
    run_three_companion_probe,
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

    def set_left_trigger(self, value: float) -> None:
        self.events.append(("lt", value))

    def set_right_trigger(self, value: float) -> None:
        self.events.append(("rt", value))

    def reset(self) -> None:
        self.events.append(("reset",))

    def disconnect(self) -> None:
        self.events.append(("disconnect",))


def _manager_with_recorders() -> tuple[CompanionManager, list[list[tuple]]]:
    logs: list[list[tuple]] = []

    def factory() -> RecordingGamepadBackend:
        events: list[tuple] = []
        logs.append(events)
        return RecordingGamepadBackend(events)

    def sleep(_seconds: float) -> None:
        return

    manager = CompanionManager(backend_factory=factory, sleep=sleep)
    return manager, logs


class CompanionPlayerTests(unittest.TestCase):
    def test_valid_players_2_3_4(self) -> None:
        manager, logs = _manager_with_recorders()
        for player in (2, 3, 4):
            bot = manager.create_companion(player)
            self.assertEqual(bot.player, player)
        self.assertEqual(manager.players, (2, 3, 4))
        self.assertEqual(len(logs), 3)
        for events in logs:
            self.assertEqual(events[0], ("connect",))
        manager.shutdown()

    def test_invalid_player_numbers_rejected(self) -> None:
        manager, _logs = _manager_with_recorders()
        for player in (0, 1, 5, -1):
            with self.assertRaises(CompanionError):
                manager.create_companion(player)
        self.assertEqual(manager.players, ())

    def test_duplicate_companions_rejected(self) -> None:
        manager, logs = _manager_with_recorders()
        manager.create_companion(2)
        with self.assertRaises(CompanionError):
            manager.create_companion(2)
        self.assertEqual(len(logs), 1)
        manager.shutdown()


class CompanionMovementTests(unittest.TestCase):
    def test_movement_is_normalized(self) -> None:
        events: list[tuple] = []
        bot = CompanionController(2, VirtualGamepad(RecordingGamepadBackend(events)))
        bot._gamepad.connect()
        bot.set_move(2.5, -4.0)
        self.assertEqual(events[-1], ("stick", 1.0, -1.0))
        bot.set_move(-9.0, 0.25)
        self.assertEqual(events[-1], ("stick", -1.0, 0.25))

    def test_movement_reset(self) -> None:
        events: list[tuple] = []
        bot = CompanionController(2, VirtualGamepad(RecordingGamepadBackend(events)))
        bot._gamepad.connect()
        bot.move_forward()
        bot.reset()
        self.assertEqual(events[-2], ("stick", 0.0, 1.0))
        self.assertEqual(events[-1], ("reset",))


class CompanionButtonTests(unittest.TestCase):
    def test_button_press_and_release(self) -> None:
        events: list[tuple] = []
        bot = CompanionController(3, VirtualGamepad(RecordingGamepadBackend(events)))
        bot._gamepad.connect()
        bot.press_button("lb")
        bot.release_button("lb")
        bot.press_button("rt")
        bot.release_button("rt")
        self.assertIn(("press", "lb"), events)
        self.assertIn(("release", "lb"), events)
        self.assertIn(("rt", 1.0), events)
        self.assertIn(("rt", 0.0), events)


class CompanionTimedTests(unittest.TestCase):
    def test_timed_movement_returns_to_neutral(self) -> None:
        events: list[tuple] = []
        sleeps: list[float] = []

        def sleep(seconds: float) -> None:
            sleeps.append(seconds)

        bot = CompanionController(
            2,
            VirtualGamepad(RecordingGamepadBackend(events)),
            sleep=sleep,
        )
        bot._gamepad.connect()
        bot.move_right(duration=0.75)
        self.assertEqual(events[-2], ("stick", 1.0, 0.0))
        self.assertEqual(events[-1], ("stick", 0.0, 0.0))
        self.assertEqual(sleeps, [0.75])

    def test_exception_during_timed_move_stops_stick(self) -> None:
        events: list[tuple] = []

        def sleep(_seconds: float) -> None:
            raise RuntimeError("interrupted")

        bot = CompanionController(
            2,
            VirtualGamepad(RecordingGamepadBackend(events)),
            sleep=sleep,
        )
        bot._gamepad.connect()
        with self.assertRaises(RuntimeError):
            bot.move_forward(duration=1.0)
        self.assertEqual(events[-1], ("stick", 0.0, 0.0))
        self.assertIn(("stick", 0.0, 1.0), events)

    def test_jump_releases_on_exception(self) -> None:
        events: list[tuple] = []

        def sleep(_seconds: float) -> None:
            raise RuntimeError("interrupted jump")

        bot = CompanionController(
            4,
            VirtualGamepad(RecordingGamepadBackend(events)),
            sleep=sleep,
        )
        bot._gamepad.connect()
        with self.assertRaises(RuntimeError):
            bot.jump()
        self.assertEqual(events.count(("press", "a")), 1)
        self.assertEqual(events.count(("release", "a")), 1)


class CompanionManagerTests(unittest.TestCase):
    def test_shutdown_resets_and_disconnects(self) -> None:
        manager, logs = _manager_with_recorders()
        manager.create_companion(2)
        manager.create_companion(3)
        manager.shutdown()
        self.assertEqual(manager.players, ())
        for events in logs:
            self.assertIn(("reset",), events)
            self.assertEqual(events[-1], ("disconnect",))

    def test_three_independent_companion_instances(self) -> None:
        manager, logs = _manager_with_recorders()
        bot2 = manager.create_companion(2)
        bot3 = manager.create_companion(3)
        bot4 = manager.create_companion(4)
        bot2.move_forward()
        bot3.move_left()
        bot4.jump(duration=0.0)
        self.assertIn(("stick", 0.0, 1.0), logs[0])
        self.assertNotIn(("stick", 0.0, 1.0), logs[1])
        self.assertNotIn(("stick", 0.0, 1.0), logs[2])
        self.assertIn(("stick", -1.0, 0.0), logs[1])
        self.assertNotIn(("stick", -1.0, 0.0), logs[0])
        self.assertIn(("press", "a"), logs[2])
        self.assertNotIn(("press", "a"), logs[0])
        self.assertNotIn(("press", "a"), logs[1])
        manager.shutdown()

    def test_demo_sequence_does_not_disconnect(self) -> None:
        events: list[tuple] = []

        def sleep(_seconds: float) -> None:
            return

        bot = CompanionController(
            2,
            VirtualGamepad(RecordingGamepadBackend(events)),
            sleep=sleep,
        )
        bot._gamepad.connect()
        run_companion_demo_sequence(bot, sleep=sleep)
        self.assertNotIn(("disconnect",), events)
        self.assertIn(("stick", 0.0, 1.0), events)
        self.assertIn(("stick", 0.0, -1.0), events)
        self.assertIn(("stick", -1.0, 0.0), events)
        self.assertIn(("stick", 1.0, 0.0), events)
        self.assertIn(("press", "a"), events)
        self.assertEqual(events[-1], ("release", "a"))

    def test_three_probe_is_simultaneous_then_released(self) -> None:
        manager, logs = _manager_with_recorders()
        bot2 = manager.create_companion(2)
        bot3 = manager.create_companion(3)
        bot4 = manager.create_companion(4)
        sleeps: list[float] = []

        def sleep(seconds: float) -> None:
            sleeps.append(seconds)
            self.assertIn(("stick", 0.0, 1.0), logs[0])
            self.assertIn(("stick", -1.0, 0.0), logs[1])
            self.assertIn(("press", "a"), logs[2])

        run_three_companion_probe(bot2, bot3, bot4, sleep=sleep)
        self.assertEqual(sleeps, [THREE_ACTION_SECONDS])
        self.assertEqual(logs[0][-1], ("stick", 0.0, 0.0))
        self.assertEqual(logs[1][-1], ("stick", 0.0, 0.0))
        self.assertEqual(logs[2][-1], ("release", "a"))
        self.assertNotIn(("disconnect",), logs[0])
        manager.shutdown()


if __name__ == "__main__":
    unittest.main()
