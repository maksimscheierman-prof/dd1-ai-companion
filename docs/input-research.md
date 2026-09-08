# Input research (Prototype 0)

Questions that must be answered before we pick an input library or write a controller backend. Do not treat anything marked **TO VERIFY** as a fact.

This project will only use an external input path. Process injection, memory reads, DLL hooks, game patches, and Steam/anti-cheat bypass are out of scope.

## Local multiplayer in DD1

Manually verified on the Windows/Steam build (keyboard, no extra controllers):

- DD1 supports multiple local heroes in one session. **VERIFIED**
- Extra configured heroes are spawned with `F6`. **VERIFIED**
- `F7` removes all additional heroes except Player 1. **VERIFIED**
- Hero selection keys: `F2` = Hero 1, `F3` = Hero 2, `F4` = Hero 3, `F5` = Hero 4. **VERIFIED**
- `F8` returns from split-screen to full-screen. **VERIFIED**
- After `F8`, `F2`–`F5` still switch which local hero receives keyboard input. **VERIFIED**

Still open:

- How many local characters can exist in one session (upper bound)? **TO VERIFY**
- What input devices besides the shared keyboard does the Steam Windows build accept for extra local players (XInput gamepad, DirectInput, other)? **TO VERIFY**

## First implementation path: shared keyboard

Virtual gamepads are **not** required for Prototype 0.

The first implementation path is:

1. The user already has Dungeon Defenders running with extra heroes spawned (`F6`).
2. Our program sends `F3` (or `F2`/`F4`/`F5`) to select a local hero.
3. Ordinary keyboard movement (`W`, later other keys) is sent to whichever hero is currently selected.

Implication: this prototype cannot drive two heroes at the same time from one keyboard. It can only prove that an external process can select Hero 2 and move that hero.

Whether synthetic `SendInput` key events are accepted the same way as a physical keyboard is **TO VERIFY** — that is the Prototype 0 input test.

## Chosen library: `pydirectinput-rgx`

Package: `pydirectinput-rgx` (imported as `pydirectinput`).

Why this one:

- External user-mode process only. No injection, hooks, or memory access.
- Sends keyboard events through Windows `SendInput` using **scan codes**, which older / DirectInput-style games (UE3 titles such as DD1) are more likely to accept than virtual-key or `keybd_event` helpers.
- Does not pull in PyAutoGUI or screenshot/computer-vision extras.
- Small API: `keyDown` / `keyUp` for `f3`, `w`, and the other keys we need.

It is still just OS-level input. The focused window receives the keys. We do not attach to the DD1 process.

Virtual gamepad libraries (ViGEm, vJoy, and similar) stay unused and remain a **fallback** only if shared-keyboard control is not enough later.

## Controllers and device identity

Not needed for the current keyboard path. Kept for a later fallback:

- Can multiple local characters be controlled using separate Xbox / XInput controllers? **TO VERIFY**
- Does DD1 distinguish individual controller devices reliably (gamepad A always maps to player 2, gamepad B to player 3, etc.)? **TO VERIFY**
- If two pads are connected, can each pad move only its own character? **TO VERIFY**
- Does the game bind pads by XInput user index (0–3), by connection order, or by some other rule? **TO VERIFY**
- Can player 1 stay on keyboard/mouse while another character is bound to a pad? **TO VERIFY**

## Virtual gamepads (fallback only)

Do not implement until the keyboard path is insufficient.

- Can a virtual controller be exposed to the game as a separate player? **TO VERIFY**
- Does DD1 treat a virtual Xbox-compatible pad the same as a physical one? **TO VERIFY**
- After a virtual pad appears, does the game create or join a new local character without extra manual steps? **TO VERIFY**

Candidate tools if we need this later:

- ViGEmBus and a user-mode client such as `vgamepad` — virtual Xbox 360 / DualShock devices
- vJoy / `pyvjoy` — virtual DirectInput joysticks

## Steam Input

Relevant mainly if we later use pads. For the current keyboard test:

- Are there limitations if Steam Input is enabled? **TO VERIFY**
- Does Steam Input merge or remap pads so DD1 no longer sees distinct devices? **TO VERIFY**
- Do we need to disable or configure Steam Input for reliable per-player control? **TO VERIFY**
- Is the result different for "Dungeon Defenders" specifically vs. Steam's global controller settings? **TO VERIFY**

## Isolation from player 1

- After `F3`, further keyboard input goes to Hero 2 rather than Hero 1. **VERIFIED** (physical keyboard)
- Does our program's `SendInput` stream behave the same as a physical keyboard? **TO VERIFY**
- Does the DD1 window need to be focused for keyboard input? **TO VERIFY** (almost certainly yes for `SendInput`)
- Focusing the DD1 window, overlay, or Steam Big Picture may send our keys to the wrong target. **TO VERIFY**

## Suggested next experiment

1. Launch DD1 yourself. Spawn Hero 2 with `F6` if needed.
2. From a separate terminal: `python src/main.py test-player2`
3. Focus the DD1 window during the countdown.
4. Confirm Hero 2 is selected (`F3`) and walks forward for about one second.
5. Confirm Hero 1 does not move unless you had already selected Hero 1.
