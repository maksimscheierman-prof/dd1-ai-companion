"""Prototype 1: persistent companion control. Older input tests stay as diagnostics."""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable

from control.companion import CompanionManager
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

COMPANION_ASSIGN_SECONDS = 12
COMPANION_HOLD_SECONDS = 10
COMPANION_MOVE_SECONDS = 1.0
COMPANION_PAUSE_SECONDS = 0.4
THREE_ASSIGN_SECONDS = 20
THREE_ACTION_SECONDS = 1.0
THREE_HOLD_SECONDS = 8

MOVEMENT_ASSIGN_SECONDS = 12
MOVEMENT_NEUTRAL_SECONDS = 1.0
MOVEMENT_FORWARD_SECONDS = 2.0
MOVEMENT_LOOK_SECONDS = 1.0
MOVEMENT_LOOK_X = 0.5
MOVEMENT_FORWARD_25 = 0.25
MOVEMENT_FORWARD_50 = 0.5
MOVEMENT_FORWARD_100 = 1.0


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


def run_companion_demo_sequence(
    bot,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Obvious pad sequence on one persistent companion. Controller stays connected."""
    bot.move_forward(duration=COMPANION_MOVE_SECONDS)
    sleep(COMPANION_PAUSE_SECONDS)
    bot.move_backward(duration=COMPANION_MOVE_SECONDS)
    sleep(COMPANION_PAUSE_SECONDS)
    bot.move_left(duration=COMPANION_MOVE_SECONDS)
    sleep(COMPANION_PAUSE_SECONDS)
    bot.move_right(duration=COMPANION_MOVE_SECONDS)
    sleep(COMPANION_PAUSE_SECONDS)
    bot.jump()


def run_three_companion_probe(
    bot2,
    bot3,
    bot4,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    """Different inputs on three pads at the same time, then release."""
    try:
        bot2.set_move(0.0, 1.0)
        bot3.set_move(-1.0, 0.0)
        bot4.press_button("a")
        sleep(THREE_ACTION_SECONDS)
    finally:
        bot2.stop_movement()
        bot3.stop_movement()
        bot4.release_button("a")


def run_movement_characterization_sequence(
    bot,
    sleep: Callable[[float], None] = time.sleep,
    log: Callable[[str], None] = print,
) -> None:
    """Time-based stick steps for observation only. Not a navigation system."""
    def hold_move(x: float, y: float, duration: float, label: str) -> None:
        log(f"[movement] {label} ({duration:.1f}s)")
        try:
            bot.set_move(x, y)
            sleep(duration)
        finally:
            bot.stop_movement()

    def hold_look(x: float, y: float, duration: float, label: str) -> None:
        log(f"[movement] {label} ({duration:.1f}s)")
        try:
            bot.set_look(x, y)
            sleep(duration)
        finally:
            bot.stop_look()

    def hold_neutral(duration: float, label: str) -> None:
        log(f"[movement] {label} ({duration:.1f}s)")
        bot.stop_movement()
        bot.stop_look()
        sleep(duration)

    try:
        hold_neutral(MOVEMENT_NEUTRAL_SECONDS, "left+right sticks neutral")
        hold_move(0.0, MOVEMENT_FORWARD_25, MOVEMENT_FORWARD_SECONDS, "left stick forward 25%")
        hold_neutral(MOVEMENT_NEUTRAL_SECONDS, "neutral")
        hold_move(0.0, MOVEMENT_FORWARD_50, MOVEMENT_FORWARD_SECONDS, "left stick forward 50%")
        hold_neutral(MOVEMENT_NEUTRAL_SECONDS, "neutral")
        hold_move(0.0, MOVEMENT_FORWARD_100, MOVEMENT_FORWARD_SECONDS, "left stick forward 100%")
        hold_neutral(MOVEMENT_NEUTRAL_SECONDS, "neutral")
        hold_look(MOVEMENT_LOOK_X, 0.0, MOVEMENT_LOOK_SECONDS, "right stick X=50% (not an angle)")
        log("[movement] right stick neutral")
        bot.stop_look()
        hold_move(0.0, MOVEMENT_FORWARD_100, MOVEMENT_FORWARD_SECONDS, "left stick forward 100%")
        log("[movement] stop")
        bot.stop_movement()
        log("[movement] jump once")
        bot.jump()
    finally:
        bot.reset()


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
    print("Legacy Prototype 0B pad smoke test.")
    print("This does NOT press F2-F5. Hero 1 should stay under your control.")
    print("Dungeon Defenders must already be running. Spawn Hero 2 with F6 if needed.")
    print("When the pad appears, assign it to Hero 2 in-game (do not use F2-F5).")
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


def cmd_test_companion() -> None:
    print("Prototype 1: one persistent companion (Bot 2).")
    print("The controller stays connected for the whole run. No F2-F5.")
    print("DD1 must already be running. Keep Hero 1 on keyboard/mouse.")
    print("Spawn Hero 2 with F6 if needed, then assign this pad to Hero 2.")
    print()
    try:
        with CompanionManager() as manager:
            bot = manager.create_companion(2)
            print("Bot 2 virtual controller is connected. Assign it to Hero 2 now.")
            print(f"Waiting {COMPANION_ASSIGN_SECONDS} seconds...")
            _countdown(COMPANION_ASSIGN_SECONDS)
            print("Running forward, back, left, right, jump. Pad stays plugged in.")
            run_companion_demo_sequence(bot)
            print()
            print("Sequence finished. Controller is still connected.")
            print("Move Hero 1 yourself. Companion should stay still.")
            print(f"Holding for {COMPANION_HOLD_SECONDS} seconds...")
            _countdown(COMPANION_HOLD_SECONDS)
    except GamepadUnavailable as exc:
        print(exc)
        print()
        print(INSTALL_HELP)
        raise SystemExit(1) from exc
    print("Done: Bot 2 controller reset and disconnected.")


def cmd_test_three_companions() -> None:
    print("Three persistent companions (Bot 2, 3, 4). Assignments were verified once;")
    print("still assign each new Xbox pad to the matching hero. Do not use F2-F5.")
    print("Keep Hero 1 on keyboard/mouse. Spawn extras with F6 if needed.")
    print()
    try:
        with CompanionManager() as manager:
            bot2 = manager.create_companion(2)
            bot3 = manager.create_companion(3)
            bot4 = manager.create_companion(4)
            print("Three virtual controllers are connected.")
            print(f"Assign them now. Waiting {THREE_ASSIGN_SECONDS} seconds...")
            _countdown(THREE_ASSIGN_SECONDS)
            print("Together: Bot 2 forward, Bot 3 left, Bot 4 jump.")
            run_three_companion_probe(bot2, bot3, bot4)
            print()
            print("Check whether each hero did a different action.")
            print("Hero 1 should still be yours. Holding briefly...")
            _countdown(THREE_HOLD_SECONDS)
    except GamepadUnavailable as exc:
        print(exc)
        print()
        print(INSTALL_HELP)
        raise SystemExit(1) from exc
    print("Done: all three controllers reset and disconnected.")


def cmd_test_movement() -> None:
    print("Movement characterization: one persistent Bot 2 pad.")
    print("This is NOT navigation. Distances and turn angles are not measured here.")
    print("Watch relative speed at 25% / 50% / 100% and what the right stick does.")
    print("Record notes in docs/movement-characterization.md. Do not use F2-F5.")
    print()
    try:
        with CompanionManager() as manager:
            bot = manager.create_companion(2)
            print("Bot 2 virtual controller is connected. Assign it to Hero 2 now.")
            print(f"Waiting {MOVEMENT_ASSIGN_SECONDS} seconds...")
            _countdown(MOVEMENT_ASSIGN_SECONDS)
            print("Starting logged stick sequence.")
            run_movement_characterization_sequence(bot)
    except GamepadUnavailable as exc:
        print(exc)
        print()
        print(INSTALL_HELP)
        raise SystemExit(1) from exc
    print("Done: Bot 2 controller reset and disconnected.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="DD1 AI Companion - Prototype 1: companion control + movement check",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "test-movement",
            "test-companion",
            "test-three-companions",
            "test-gamepad",
            "test-player2",
        ],
        help=(
            "test-movement: analog stick characterization; "
            "test-companion / test-three-companions: control checks; "
            "test-gamepad / test-player2: older diagnostics"
        ),
    )
    args = parser.parse_args(argv)

    print("DD1 AI Companion - Prototype 1: companion control + movement check")
    if args.command is None:
        parser.print_help(sys.stderr)
        return 0
    commands = {
        "test-movement": cmd_test_movement,
        "test-companion": cmd_test_companion,
        "test-three-companions": cmd_test_three_companions,
        "test-gamepad": cmd_test_gamepad,
        "test-player2": cmd_test_player2,
    }
    commands[args.command]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
