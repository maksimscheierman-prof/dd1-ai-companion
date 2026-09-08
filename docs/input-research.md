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
- At least four local heroes (human + three virtual pads). **VERIFIED**

## Keyboard `SendInput` (early Prototype 0)

- Synthetic keyboard scan-code `SendInput` is accepted by DD1 (`F3` + `W`). **VERIFIED**
- Player switching through `F2`–`F5` works from an external Python process. **VERIFIED**
- After `F3`, further keyboard input goes to Hero 2. **VERIFIED**
- Main keyboard-switching architecture for companions. **REJECTED**

Reason: selecting Hero 2 with `F3` changes the actively controlled local hero. The human then loses Hero 1.

`python src/main.py test-player2` stays as a **diagnostic only**.

## Virtual controllers — PASSED

- ViGEmBus + `vgamepad` creates a virtual Xbox 360 / XInput controller. **VERIFIED**
- DD1 recognizes that pad as an independent local player. **VERIFIED**
- Hero 2 can move and jump (`A`) from a virtual pad. **VERIFIED**
- Human Hero 1 remains independently controllable at the same time. **VERIFIED**
- Three virtual Xbox/XInput controllers can coexist. **VERIFIED**
- Bot 2, Bot 3, and Bot 4 can receive independent input at the same time. **VERIFIED**
- Those player assignments stayed correct during the three-pad test. **VERIFIED**
- Multi-companion control architecture. **VERIFIED**

```text
Human Player 1  →  keyboard / mouse or physical human input
Bot Player 2    →  virtual XInput controller #1
Bot Player 3    →  virtual XInput controller #2
Bot Player 4    →  virtual XInput controller #3
```

Pads stay connected for the lifetime of the companion program.

Still open:

- Long-session remapping (hours, unplug/replug, Steam restart). **TO VERIFY**
- Face/shoulder/trigger gameplay labels besides `A` = jump. **TO VERIFY**
- Analog stick speed curve, deadzone, and right-stick camera behavior. **TO VERIFY** (`test-movement`)

## Movement limitation (read before `test-movement`)

Holding a stick for N seconds is **not** a position. It is also **not** a heading in degrees.

Distance and facing can change with:

- hero movement speed / stats
- equipment
- buffs and debuffs
- collisions
- slopes
- framerate or other game timing
- stick deadzones

The characterization command only logs commanded stick values and durations so a human can watch the result.

## Chosen stack

- **Python:** `vgamepad` 0.1.0, hidden behind `src/input/gamepad.py`
- **Driver:** ViGEmBus 1.22.0 (retired/archived, still works on Windows 10/11)
- **Higher layers** (`src/control/`) must not import `vgamepad`

Fallback if ViGEm becomes unusable: HIDMaestro (.NET / UMDF2, no first-class PyPI API).

## Steam Input

- Steam Input can intercept an Xbox pad. **TO VERIFY** as a long-term risk
- The successful three-pad test did not require changing this conclusion: extra pads worked as independent players in that session.

## Isolation from player 1

- Keyboard `F2`–`F5` steals the human's active hero. **VERIFIED** — rejected as the companion path
- Independent virtual-controller control of Hero 2 while Hero 1 stays on keyboard/mouse. **VERIFIED**
- Same isolation with three virtual companions at once. **VERIFIED**

## Suggested next experiment

1. `python src/main.py test-movement` on a flat open spot.
2. Watch 25% vs 50% vs 100% forward, then the 50% right-stick hold.
3. Fill `docs/movement-characterization.md` with observations only.
