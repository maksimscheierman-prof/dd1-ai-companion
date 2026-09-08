"""Persistent companion control. Higher layers should not import vgamepad."""

from control.companion import (
    COMPANION_PLAYERS,
    CompanionController,
    CompanionError,
    CompanionManager,
)

__all__ = [
    "COMPANION_PLAYERS",
    "CompanionController",
    "CompanionError",
    "CompanionManager",
]
