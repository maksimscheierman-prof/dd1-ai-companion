"""Minimal keyboard sender. Real input is optional; tests inject a fake backend."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Protocol


class KeyboardBackend(Protocol):
    def key_down(self, key: str) -> None:
        """Hold a key down."""

    def key_up(self, key: str) -> None:
        """Release a key."""


class PydirectinputBackend:
    """Windows SendInput via pydirectinput-rgx (scan codes)."""

    def __init__(self) -> None:
        import pydirectinput

        pydirectinput.PAUSE = 0
        pydirectinput.FAILSAFE = False
        self._lib = pydirectinput

    def key_down(self, key: str) -> None:
        self._lib.keyDown(key, _pause=False)

    def key_up(self, key: str) -> None:
        self._lib.keyUp(key, _pause=False)


class Keyboard:
    def __init__(
        self,
        backend: KeyboardBackend,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._backend = backend
        self._sleep = sleep
        self._held: set[str] = set()

    def key_down(self, key: str) -> None:
        self._backend.key_down(key)
        self._held.add(key)

    def key_up(self, key: str) -> None:
        try:
            self._backend.key_up(key)
        finally:
            self._held.discard(key)

    def press_key(self, key: str) -> None:
        self.tap_key(key, duration=0.0)

    def sleep(self, seconds: float) -> None:
        self._sleep(seconds)

    def tap_key(self, key: str, duration: float = 0.05) -> None:
        try:
            self.key_down(key)
            if duration > 0:
                self.sleep(duration)
        finally:
            self.key_up(key)

    def release_held(self) -> None:
        for key in list(self._held):
            try:
                self.key_up(key)
            except Exception:
                self._held.discard(key)

    def __enter__(self) -> Keyboard:
        return self

    def __exit__(self, *exc: object) -> None:
        self.release_held()
