# Input research

Questions that must be answered before we commit to an architecture. Do not treat anything marked **TO VERIFY** as a fact.

This project will only use an external input path. Process injection, memory reads, DLL hooks, game patches, and Steam/anti-cheat bypass are out of scope.

## Local multiplayer in DD1

Manually verified on the Windows/Steam build:

- DD1 supports multiple local heroes in one session. **VERIFIED**
- Extra configured heroes are spawned with `F6`. **VERIFIED**
- `F7` removes all additional heroes except Player 1. **VERIFIED**
- Hero selection keys: `F2` = Hero 1, `F3` = Hero 2, `F4` = Hero 3, `F5` = Hero 4. **VERIFIED**
- `F8` returns from split-screen to full-screen. **VERIFIED**
- After `F8`, `F2`–`F5` still switch which local hero receives keyboard input. **VERIFIED**
- Upper bound on local heroes in one session. **TO VERIFY** (at least 4 via `F2`–`F5`)

## Keyboard `SendInput` prototype (Prototype 0)

- Synthetic keyboard scan-code `SendInput` is accepted by DD1 (`F3` + `W`). **VERIFIED**
- Player switching through `F2`–`F5` works from an external Python process. **VERIFIED**
- After `F3`, further keyboard input goes to Hero 2. **VERIFIED**
- Main keyboard-switching architecture for companions. **REJECTED**

Reason: selecting Hero 2 with `F3` changes the actively controlled local hero. The human then loses Hero 1. That is technically successful and unusable for the real product.

The keyboard command `python src/main.py test-player2` stays as a **diagnostic only**. Do not use it as the companion control path.

Library used for that test: `pydirectinput-rgx` (scan-code `SendInput`). External process only.

## Preferred architecture

Human Player 1 stays on keyboard/mouse (or a physical pad).

Companions should be additional local heroes, each on its own virtual Xbox / XInput controller.

```text
Python app  →  virtual Xbox 360 pad  →  DD1 local Player 2
```

No DLL injection, memory access, game hooks, packet manipulation, or DD1 file changes.

Still open:

- Can DD1 bind a second local hero to a separate Xbox / XInput controller while Hero 1 stays on keyboard? **TO VERIFY** (Prototype 0B)
- Does DD1 distinguish individual controller devices reliably? **TO VERIFY**
- Does the game bind pads by XInput user index (0–3), connection order, or something else? **TO VERIFY**
- Does a virtual Xbox 360 pad appear as a normal extra player? **TO VERIFY**

## Virtual controller options (Prototype 0B)

Evaluated September 2026. ViGEm was **not** assumed to be the default.

### `vgamepad` + ViGEmBus — chosen for Prototype 0B

- **What it is:** Python library (`vgamepad`) that creates a virtual Xbox 360 controller through the ViGEmBus kernel driver. Windows sees a real XInput device. Games do not need patches.
- **Python:** first-class (`VX360Gamepad`, `press_button`, `left_joystick_float`, `reset`, `update`). Package last pushed mid-2026; latest PyPI release `0.1.0`.
- **Driver:** ViGEmBus (Nefarius). Officially **retired / archived 2023-11-02** after a trademark conflict. Final signed installer is **1.22.0**. Still widely used (DS4Windows, Sunshine fallback). Driver itself is unmaintained; it still works on current Windows 10/11.
- **Windows:** 10/11 x64 (1.17+ is Win10/11 only). Admin install required once.
- **Limitations:** no further ViGEm security/compat updates; `vgamepad` has no public `disconnect()` (removal happens when the pad object is destroyed); XInput is limited to four slots; a global ViGEm bus is created at `import vgamepad`.
- **Why chosen anyway:** it is the only **simple, documented Python → Xbox/XInput** path. Newer stacks are C#/C++ first.

### HIDMaestro / PadForge — fallback if ViGEm fails

- Actively developed user-mode UMDF2 virtual pads. No ViGEm kernel driver.
- API is a .NET SDK (`HIDMaestro.Core.dll`), not a small PyPI package. Python would need `pythonnet` plus their driver bits.
- Better long-term candidate; too much setup for this feasibility test.

### Other options (not used)

- **VIIPER:** USB/IP virtual devices. Active, but a transport stack, not a tiny Python pad API.
- **libvirtualhid / LizardByte Virtual HID Driver:** active; Windows extra profiles may need a paid license; ViGEm remains their free Xbox 360 fallback.
- **WinUHid / DuoController:** C/UMDF SDKs, no small Python wrapper.
- **vJoy / `pyvjoy`:** virtual DirectInput joystick, not a native Xbox/XInput pad. Worse match for DD1 local Player 2.

### Steam Input

- Steam Input can intercept an Xbox pad and present a "Steam Virtual Gamepad", which may collapse or reorder players. **TO VERIFY**
- For Prototype 0B, disable Steam Input for Dungeon Defenders (per-game: disable Steam Input) if the virtual pad does not show up as its own player. **TO VERIFY**

## Isolation from player 1

- Keyboard `F2`–`F5` steals the human's active hero. **VERIFIED** — rejected as the companion path
- Independent virtual-controller control of Hero 2 while Hero 1 stays on keyboard/mouse. **TO VERIFY**
- Whether DD1 must be focused for XInput pad input. **TO VERIFY** (often no for XInput)

## Suggested next experiment (Prototype 0B)

1. Install ViGEmBus 1.22.0 (see README).
2. `pip install -r requirements.txt`
3. Launch DD1. Keep Hero 1 under your keyboard. Spawn Hero 2 (`F6`) if needed.
4. Prefer Steam Input **off** for this game during the first test.
5. `python src/main.py test-gamepad`
6. During the wait, assign the new Xbox 360 controller to Hero 2. Do **not** press `F2`–`F5`.
7. Watch whether Hero 2 walks forward (~1 s) and hops, while you can still move Hero 1.
