# DD1 AI Companion

A small technical prototype for **Dungeon Defenders 1** on Windows/Steam. The long-term idea is to control extra local characters as AI companions during private play. This repository is not a bot, a trainer, or a complete companion system.

Intended use is **local / private gameplay**. The program sits outside the game: no memory reads, no DLL injection, no game patches, and no Steam or anti-cheat bypass.

Development is **paused** on runtime features. Next work is DDDK / UnrealScript telemetry research. See `docs/plan.md` (`NEXT SESSION START HERE`) and `docs/dddk-telemetry-research.md`.

## Verified architecture

Prototypes 0 and 1 (control feasibility) are **PASSED**.

```text
Human Player 1  →  keyboard / mouse (or a physical pad)
Bot Player 2    →  virtual XInput controller #1
Bot Player 3    →  virtual XInput controller #2
Bot Player 4    →  virtual XInput controller #3
```

Manually verified in DD1:

- Three virtual Xbox / XInput pads can exist at once (`vgamepad` + ViGEmBus).
- DD1 treats them as independent local players.
- Bots 2–4 can receive independent input at the same time.
- Human Player 1 stays independently controllable.
- Assignments stayed stable during the real three-controller test.
- Basic movement and jump work.
- Default movement assumption: **full stick + neutral**. Partial stick (25% / 50% / 100%) did not look useful for distinct speeds.

Keyboard `F2`–`F5` switching **works** and is **rejected** as the primary path: it steals the human's active hero.

## Perception (blocked)

Do **not** assume split-screen or camera-switching vision. That would hurt Player 1's full-screen play.

Preferred next architecture, **if** the Development Kit can export state:

```text
Dungeon Defenders 1
        |
        | game-state / telemetry
        v
     Python bot
   /      |      \
Pad 2   Pad 3   Pad 4
        |
        v
Dungeon Defenders 1
```

Prototype 2 screen vision is a **fallback**, not the first choice. It is **BLOCKED** until DDDK telemetry feasibility is checked.

## Install

ViGEmBus is a one-time Windows driver (admin). The Python library talks to it; it does not patch DD1.

1. Download [ViGEmBus 1.22.0](https://github.com/nefarius/ViGEmBus/releases/tag/v1.22.0) and run `ViGEmBus_1.22.0_x64_x86_arm64.exe`.
2. Install Python packages without the extra driver popup:

```text
# cmd
set VGAMEPAD_SKIP_VIGEMBUS_INSTALL=true
pip install -r requirements.txt

# PowerShell
$env:VGAMEPAD_SKIP_VIGEMBUS_INSTALL = "true"
pip install -r requirements.txt
```

## Manual tests (already used)

```text
python src/main.py test-companion
python src/main.py test-three-companions
python src/main.py test-movement
```

Older diagnostics: `test-gamepad`, `test-player2` (keyboard switch; not the companion path).
