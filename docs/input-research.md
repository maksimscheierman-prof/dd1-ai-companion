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

## Keyboard `SendInput` (early Prototype 0)

- Synthetic keyboard scan-code `SendInput` is accepted by DD1 (`F3` + `W`). **VERIFIED**
- Player switching through `F2`–`F5` works from an external Python process. **VERIFIED**
- After `F3`, further keyboard input goes to Hero 2. **VERIFIED**
- Main keyboard-switching architecture for companions. **REJECTED**

Reason: selecting Hero 2 with `F3` changes the actively controlled local hero. The human then loses Hero 1.

`python src/main.py test-player2` stays as a **diagnostic only**.

## Prototype 0B virtual controller — PASSED

Manual test in Dungeon Defenders 1:

- ViGEmBus + `vgamepad` creates a virtual Xbox 360 / XInput controller. **VERIFIED**
- DD1 recognizes that pad as an independent local player. **VERIFIED**
- Hero 2 can move through the virtual controller. **VERIFIED**
- Hero 2 can jump through the virtual controller (`A`). **VERIFIED**
- Human-controlled Hero 1 remains independently controllable at the same time. **VERIFIED**

This is the companion-control architecture.

```text
Human Player 1  →  keyboard / mouse or physical human input
Bot Player 2    →  virtual XInput controller #1
Bot Player 3    →  virtual XInput controller #2
Bot Player 4    →  virtual XInput controller #3
```

Pads stay connected for the lifetime of the companion program. Do not plug/unplug per action.

Still open:

- Does DD1 keep three virtual pads mapped stably to Heroes 2/3/4? **TO VERIFY**
- Is mapping by XInput user index, connection order, or something else? **TO VERIFY**
- Do other face/shoulder/trigger buttons match the usual Xbox labels in DD1? **TO VERIFY** (`A` = jump is the only verified gameplay button)

## Chosen stack

- **Python:** `vgamepad` 0.1.0, hidden behind `src/input/gamepad.py`
- **Driver:** ViGEmBus 1.22.0 (retired/archived, still works on Windows 10/11)
- **Higher layers** (`src/control/`) must not import `vgamepad`

Fallback if ViGEm becomes unusable: HIDMaestro (.NET / UMDF2, no first-class PyPI API).

## Steam Input

- Steam Input can intercept an Xbox pad and present a "Steam Virtual Gamepad". **TO VERIFY**
- If extra pads collapse or swap heroes, disable Steam Input for Dungeon Defenders and retry.

## Isolation from player 1

- Keyboard `F2`–`F5` steals the human's active hero. **VERIFIED** — rejected as the companion path
- Independent virtual-controller control of Hero 2 while Hero 1 stays on keyboard/mouse. **VERIFIED**
- Same isolation with three virtual companions at once. **TO VERIFY**

## Suggested next experiment

1. `python src/main.py test-companion` — persistent Bot 2 walk/jump; confirm Hero 1 still works after the sequence while the pad stays plugged in.
2. `python src/main.py test-three-companions` — three pads, three different actions at once. Record which hero did what versus creation order.
