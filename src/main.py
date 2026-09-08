"""Prototype 0B: virtual Xbox pad. Keyboard hero-switch remains diagnostic-only."""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable

from input.gamepad import (
    INSTALL_HELP,
    GamepadUnavailable,
    VGamepadBackend,
    VirtualGamepad,
)
from input.keyboard import Keyboard, PydirectinputBackend

COUNTDOWN_SECONDS = 3
SELECT_KEY = "f3"
SELECT_TAP_SECONDS = 0.05
SELECT_PAUSE_SECONDS = 0.4
MOVE_KEY = "w"
MOVE_HOLD_SECONDS = 1.0

JOIN_WAIT_SECONDS = 12
STICK_FORWARD_Y = 1.0
STICK_HOLD_SECONDS = 1.0
JUMP_BUTTON = "a"
JUMP_TAP_SECONDS = 0.2


def run_player2_move_sequence(
    keyboard: Keyboard,
    sleep: Callable[[float], None] | None = None,
) -> None:
    """Diagnostic only: F3 then hold W. Steals human control of Hero 1."""
    pause = sleep or keyboard.sleep
    try:
        keyboard.tap_key(SELECT_KEY, duration=SELECT_TAP_SECONDS)
        pause(SELECT_PAUSE_SECONDS)
        keyboard.tap_key(MOVE_KEY, duration=MOVE_HOLD_SECONDS)
    finally:
        keyboard.release_held()


def run_gamepad_move_sequence(
    gamepad: VirtualGamepad,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Left stick forward, stop, tap jump (A). No F2-F5."""
    try:
        gamepad.set_left_stick(0.0, STICK_FORWARD_Y)
        sleep(STICK_HOLD_SECONDS)
        gamepad.set_left_stick(0.0, 0.0)
        gamepad.press_button(JUMP_BUTTON)
        sleep(JUMP_TAP_SECONDS)
        gamepad.release_button(JUMP_BUTTON)
    finally:
        gamepad.reset()


def _countdown(seconds: int, sleep: Callable[[float], None] = time.sleep) -> None:
    for remaining in range(seconds, 0, -1):
        print(f"{remaining}...")
        sleep(1)


def cmd_test_player2() -> None:
    print("DIAGNOSTIC ONLY - not the companion control path.")
    print("F3 switches the active hero, so the human loses Hero 1.")
    print("WARNING: Dungeon Defenders 1 must already be running.")
    print("This will send F3, then hold W for about one second.")
    print("Focus the Dungeon Defenders window now.")
    _countdown(COUNTDOWN_SECONDS)

    with Keyboard(PydirectinputBackend()) as keyboard:
        run_player2_move_sequence(keyboard)

    print("Done (diagnostic): sent F3 and held W.")


def cmd_test_gamepad() -> None:
    print("Prototype 0B: virtual Xbox 360 controller.")
    print("This does NOT press F2-F5. Hero 1 should stay under your control.")
    print("Dungeon Defenders must already be running. Spawn Hero 2 with F6 if needed.")
    print("When the pad appears, assign it to Hero 2 in-game (do not use F2-F5).")
    print("If Steam remaps the pad, disable Steam Input for Dungeon Defenders and retry.")
    print()
    try:
        with VirtualGamepad(VGamepadBackend()) as gamepad:
            print("Virtual controller is connected. Assign it to Hero 2 now.")
            print(f"Waiting {JOIN_WAIT_SECONDS} seconds...")
            _countdown(JOIN_WAIT_SECONDS)
            print("Sending left-stick forward, then jump.")
            run_gamepad_move_sequence(gamepad)
    except GamepadUnavailable as exc:
        print(exc)
        print()
        print(INSTALL_HELP)
        raise SystemExit(1) from exc
    print("Done: reset and disconnected the virtual controller.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "DD1 AI Companion - Prototype 0B: independent virtual-controller feasibility"
        ),
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["test-gamepad", "test-player2"],
        help=(
            "test-gamepad: preferred Prototype 0B pad test; "
            "test-player2: rejected keyboard switch (diagnostic only)"
        ),
    )
    args = parser.parse_args(argv)

    print("DD1 AI Companion - Prototype 0B: virtual-controller feasibility")
    if args.command is None:
        parser.print_help(sys.stderr)
        return 0
    if args.command == "test-gamepad":
        cmd_test_gamepad()
    elif args.command == "test-player2":
        cmd_test_player2()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
