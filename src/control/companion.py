"""One companion per virtual pad. Pads stay connected until the manager shuts down."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TYPE_CHECKING

from input.gamepad import VGamepadBackend, VirtualGamepad

if TYPE_CHECKING:
    from input.gamepad import GamepadBackend

COMPANION_PLAYERS = frozenset({2, 3, 4})
MAX_COMPANIONS = 3

# A = jump is verified in DD1. The rest are provisional Xbox labels only.
JUMP_BUTTON = "a"
PRIMARY_ATTACK_BUTTON = "x"  # TO VERIFY in DD1
SECONDARY_ATTACK_BUTTON = "y"  # TO VERIFY in DD1
DEFAULT_TAP_SECONDS = 0.2

_TRIGGER_FULL = {
    "lt": "left",
    "left_trigger": "left",
    "rt": "right",
    "right_trigger": "right",
}


class CompanionError(ValueError):
    """Invalid player number, duplicate companion, or manager is full."""


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, float(value)))


class CompanionController:
    """High-level control for one extra local hero (player 2, 3, or 4)."""

    def __init__(
        self,
        player: int,
        gamepad: VirtualGamepad,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if player not in COMPANION_PLAYERS:
            raise CompanionError(
                f"Companion player must be one of {sorted(COMPANION_PLAYERS)}, got {player}."
            )
        self.player = player
        self._gamepad = gamepad
        self._sleep = sleep

    def set_move(self, x: float, y: float) -> None:
        self._gamepad.set_left_stick(_clamp(x, -1.0, 1.0), _clamp(y, -1.0, 1.0))

    def stop_movement(self) -> None:
        self.set_move(0.0, 0.0)

    def set_look(self, x: float, y: float) -> None:
        """Right stick. Values are normalized; duration is not degrees."""
        self._gamepad.set_right_stick(_clamp(x, -1.0, 1.0), _clamp(y, -1.0, 1.0))

    def stop_look(self) -> None:
        self.set_look(0.0, 0.0)

    def move_forward(self, duration: float | None = None) -> None:
        self._hold_move(0.0, 1.0, duration)

    def move_backward(self, duration: float | None = None) -> None:
        self._hold_move(0.0, -1.0, duration)

    def move_left(self, duration: float | None = None) -> None:
        self._hold_move(-1.0, 0.0, duration)

    def move_right(self, duration: float | None = None) -> None:
        self._hold_move(1.0, 0.0, duration)

    def _hold_move(self, x: float, y: float, duration: float | None) -> None:
        try:
            self.set_move(x, y)
            if duration is None:
                return
            self._sleep(duration)
        finally:
            if duration is not None:
                self.stop_movement()

    def set_left_trigger(self, value: float) -> None:
        self._gamepad.set_left_trigger(_clamp(value, 0.0, 1.0))

    def set_right_trigger(self, value: float) -> None:
        self._gamepad.set_right_trigger(_clamp(value, 0.0, 1.0))

    def press_button(self, button: str) -> None:
        trigger = _TRIGGER_FULL.get(button.lower())
        if trigger == "left":
            self.set_left_trigger(1.0)
            return
        if trigger == "right":
            self.set_right_trigger(1.0)
            return
        self._gamepad.press_button(button.lower())

    def release_button(self, button: str) -> None:
        trigger = _TRIGGER_FULL.get(button.lower())
        if trigger == "left":
            self.set_left_trigger(0.0)
            return
        if trigger == "right":
            self.set_right_trigger(0.0)
            return
        self._gamepad.release_button(button.lower())

    def tap_button(self, button: str, duration: float = DEFAULT_TAP_SECONDS) -> None:
        try:
            self.press_button(button)
            if duration > 0:
                self._sleep(duration)
        finally:
            self.release_button(button)

    def jump(self, duration: float = DEFAULT_TAP_SECONDS) -> None:
        self.tap_button(JUMP_BUTTON, duration=duration)

    def primary_attack(self, duration: float = DEFAULT_TAP_SECONDS) -> None:
        # Button mapping is unverified in DD1.
        self.tap_button(PRIMARY_ATTACK_BUTTON, duration=duration)

    def secondary_attack(self, duration: float = DEFAULT_TAP_SECONDS) -> None:
        # Button mapping is unverified in DD1.
        self.tap_button(SECONDARY_ATTACK_BUTTON, duration=duration)

    def reset(self) -> None:
        try:
            self.stop_movement()
            self.stop_look()
        finally:
            self._gamepad.reset()

    def close(self) -> None:
        try:
            self.reset()
        finally:
            self._gamepad.disconnect()


class CompanionManager:
    """Owns up to three persistent virtual pads for players 2, 3, and 4."""

    def __init__(
        self,
        backend_factory: Callable[[], GamepadBackend] | None = None,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._backend_factory = backend_factory or VGamepadBackend
        self._sleep = sleep
        self._companions: dict[int, CompanionController] = {}

    def create_companion(self, player: int) -> CompanionController:
        if player not in COMPANION_PLAYERS:
            raise CompanionError(
                f"Companion player must be one of {sorted(COMPANION_PLAYERS)}, got {player}."
            )
        if player in self._companions:
            raise CompanionError(f"Companion for player {player} already exists.")
        if len(self._companions) >= MAX_COMPANIONS:
            raise CompanionError(f"At most {MAX_COMPANIONS} companions are allowed.")

        gamepad = VirtualGamepad(self._backend_factory())
        gamepad.connect()
        companion = CompanionController(player, gamepad, sleep=self._sleep)
        self._companions[player] = companion
        return companion

    def get(self, player: int) -> CompanionController:
        try:
            return self._companions[player]
        except KeyError as exc:
            raise CompanionError(f"No companion for player {player}.") from exc

    @property
    def players(self) -> tuple[int, ...]:
        return tuple(sorted(self._companions))

    def shutdown(self) -> None:
        for companion in list(self._companions.values()):
            try:
                companion.close()
            except Exception:
                pass
        self._companions.clear()

    def __enter__(self) -> CompanionManager:
        return self

    def __exit__(self, *exc: object) -> None:
        self.shutdown()
