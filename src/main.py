"""Prototype 0: select Hero 2 and walk forward with ordinary keyboard input."""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable

from input.keyboard import Keyboard, PydirectinputBackend

COUNTDOWN_SECONDS = 3
SELECT_KEY = "f3"
SELECT_TAP_SECONDS = 0.05
SELECT_PAUSE_SECONDS = 0.4
MOVE_KEY = "w"
MOVE_HOLD_SECONDS = 1.0


def run_player2_move_sequence(
    keyboard: Keyboard,
    sleep: Callable[[float], None] | None = None,
) -> None:
    """Select Hero 2 (F3), wait, hold W for about one second, then release."""
    pause = sleep or keyboard.sleep
    try:
        keyboard.tap_key(SELECT_KEY, duration=SELECT_TAP_SECONDS)
        pause(SELECT_PAUSE_SECONDS)
        keyboard.tap_key(MOVE_KEY, duration=MOVE_HOLD_SECONDS)
    finally:
        keyboard.release_held()


def _countdown(seconds: int, sleep: Callable[[float], None] = time.sleep) -> None:
    for remaining in range(seconds, 0, -1):
        print(f"Starting in {remaining}...")
        sleep(1)


def cmd_test_player2() -> None:
    print("WARNING: Dungeon Defenders 1 must already be running.")
    print("Heroes 1 and 2 must already be spawned (use F6 in-game if needed).")
    print("This will send F3, then hold W for about one second.")
    print("Focus the Dungeon Defenders window now. Do not switch away.")
    _countdown(COUNTDOWN_SECONDS)

    with Keyboard(PydirectinputBackend()) as keyboard:
        run_player2_move_sequence(keyboard)

    print("Done: sent F3 and held W for about one second.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="DD1 AI Companion - Prototype 0: Input feasibility",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["test-player2"],
        help="test-player2: select Hero 2 and walk forward briefly",
    )
    args = parser.parse_args(argv)

    print("DD1 AI Companion - Prototype 0: Input feasibility")
    if args.command is None:
        parser.print_help(sys.stderr)
        return 0
    if args.command == "test-player2":
        cmd_test_player2()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
