"""Virtual Xbox/XInput pad. Real ViGEm devices are optional; tests inject a fake backend."""

from __future__ import annotations

import gc
from typing import Protocol

BUTTON_NAMES = {
    "a": "XUSB_GAMEPAD_A",
    "b": "XUSB_GAMEPAD_B",
    "x": "XUSB_GAMEPAD_X",
    "y": "XUSB_GAMEPAD_Y",
    "start": "XUSB_GAMEPAD_START",
    "back": "XUSB_GAMEPAD_BACK",
    "lb": "XUSB_GAMEPAD_LEFT_SHOULDER",
    "rb": "XUSB_GAMEPAD_RIGHT_SHOULDER",
}

INSTALL_HELP = """
ViGEmBus is required (one-time Windows driver, admin install).

1. Download ViGEmBus 1.22.0 from:
   https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0
2. Run ViGEmBus_1.22.0_x64_x86_arm64.exe and finish the installer.
3. Install Python deps without the bundled driver UI:
   cmd:        set VGAMEPAD_SKIP_VIGEMBUS_INSTALL=true
   PowerShell: $env:VGAMEPAD_SKIP_VIGEMBUS_INSTALL = "true"
   then:       pip install -r requirements.txt

If Device Manager has no "Nefarius Virtual Gamepad Emulation Bus", the driver is missing.
""".strip()


class GamepadUnavailable(RuntimeError):
    """Raised when the virtual pad cannot be created (missing driver or library)."""


class GamepadBackend(Protocol):
    def connect(self) -> None:
        """Create and plug in the virtual controller."""

    def press_button(self, button: str) -> None:
        """Hold a named button (a, b, x, y, ...)."""

    def release_button(self, button: str) -> None:
        """Release a named button."""

    def set_left_stick(self, x: float, y: float) -> None:
        """Set left stick in [-1.0, 1.0]. y=+1 is typically forward on X360."""

    def set_right_stick(self, x: float, y: float) -> None:
        """Set right stick in [-1.0, 1.0]. Duration is not an angle."""

    def set_left_trigger(self, value: float) -> None:
        """Set LT in [0.0, 1.0]."""

    def set_right_trigger(self, value: float) -> None:
        """Set RT in [0.0, 1.0]."""

    def reset(self) -> None:
        """Neutral sticks and released buttons."""

    def disconnect(self) -> None:
        """Unplug the virtual controller if the backend supports it."""


class VGamepadBackend:
    """Xbox 360 pad via vgamepad + ViGEmBus. Imported only when connect() runs."""

    def __init__(self) -> None:
        self._pad = None
        self._buttons = None

    def connect(self) -> None:
        if self._pad is not None:
            return
        try:
            import vgamepad as vg
        except Exception as exc:
            raise GamepadUnavailable(
                f"Could not import vgamepad. {INSTALL_HELP}"
            ) from exc
        try:
            self._pad = vg.VX360Gamepad()
            self._buttons = vg.XUSB_BUTTON
        except Exception as exc:
            raise GamepadUnavailable(
                f"Could not create a virtual Xbox 360 controller. {INSTALL_HELP}"
            ) from exc

    def _require_pad(self):
        if self._pad is None or self._buttons is None:
            raise GamepadUnavailable("Virtual controller is not connected.")
        return self._pad, self._buttons

    def _button(self, name: str):
        key = name.lower()
        if key not in BUTTON_NAMES:
            raise ValueError(f"Unknown button {name!r}. Use one of: {sorted(BUTTON_NAMES)}")
        _pad, buttons = self._require_pad()
        return getattr(buttons, BUTTON_NAMES[key])

    def press_button(self, button: str) -> None:
        pad, _buttons = self._require_pad()
        pad.press_button(button=self._button(button))
        pad.update()

    def release_button(self, button: str) -> None:
        pad, _buttons = self._require_pad()
        pad.release_button(button=self._button(button))
        pad.update()

    def set_left_stick(self, x: float, y: float) -> None:
        pad, _buttons = self._require_pad()
        pad.left_joystick_float(x_value_float=x, y_value_float=y)
        pad.update()

    def set_right_stick(self, x: float, y: float) -> None:
        pad, _buttons = self._require_pad()
        pad.right_joystick_float(x_value_float=x, y_value_float=y)
        pad.update()

    def set_left_trigger(self, value: float) -> None:
        pad, _buttons = self._require_pad()
        pad.left_trigger_float(value_float=value)
        pad.update()

    def set_right_trigger(self, value: float) -> None:
        pad, _buttons = self._require_pad()
        pad.right_trigger_float(value_float=value)
        pad.update()

    def reset(self) -> None:
        pad, _buttons = self._require_pad()
        pad.reset()
        pad.update()

    def disconnect(self) -> None:
        pad = self._pad
        self._pad = None
        self._buttons = None
        if pad is None:
            return
        try:
            pad.reset()
            pad.update()
        except Exception:
            pass
        del pad
        gc.collect()


class VirtualGamepad:
    def __init__(self, backend: GamepadBackend) -> None:
        self._backend = backend
        self._connected = False

    def connect(self) -> None:
        self._backend.connect()
        self._connected = True

    def press_button(self, button: str) -> None:
        self._backend.press_button(button)

    def release_button(self, button: str) -> None:
        self._backend.release_button(button)

    def set_left_stick(self, x: float, y: float) -> None:
        self._backend.set_left_stick(x, y)

    def set_right_stick(self, x: float, y: float) -> None:
        self._backend.set_right_stick(x, y)

    def set_left_trigger(self, value: float) -> None:
        self._backend.set_left_trigger(value)

    def set_right_trigger(self, value: float) -> None:
        self._backend.set_right_trigger(value)

    def reset(self) -> None:
        if self._connected:
            self._backend.reset()

    def disconnect(self) -> None:
        if not self._connected:
            return
        try:
            try:
                self._backend.reset()
            except Exception:
                pass
            self._backend.disconnect()
        finally:
            self._connected = False

    def __enter__(self) -> VirtualGamepad:
        self.connect()
        return self

    def __exit__(self, *exc: object) -> None:
        self.disconnect()
