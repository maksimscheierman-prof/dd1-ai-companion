# DD1 AI Companion

A small technical prototype for **Dungeon Defenders 1** on Windows/Steam. The long-term idea is to control extra local characters as AI companions during private play. This repository is not a bot, a trainer, or a complete companion system.

Intended use is **local / private gameplay**. The program sits outside the game: no memory reads, no DLL injection, no game patches, and no Steam or anti-cheat bypass.

## Architecture

Prototype 0 is **PASSED**. A virtual Xbox 360 / XInput pad can drive Hero 2 while the human keeps Hero 1.

```text
Human Player 1  →  keyboard / mouse (or a physical pad)
Bot Player 2    →  virtual XInput controller #1
Bot Player 3    →  virtual XInput controller #2
Bot Player 4    →  virtual XInput controller #3
```

Pads stay connected for the life of the companion program. Do not create and destroy a controller per action.

Keyboard `F2`–`F5` switching works and is **rejected**: it steals the human's hero.

Current phase: **Prototype 1** — a persistent control API for up to three companions. No AI, vision, or combat logic yet.

How DD1 maps three virtual pads to heroes 2/3/4 is still **unverified**. Treat player numbers as logical labels until the three-controller test is done.

See `docs/plan.md` and `docs/input-research.md`.

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

## Manual tests

Preferred (Prototype 1, one companion):

```text
python src/main.py test-companion
```

Experimental (three pads at once):

```text
python src/main.py test-three-companions
```

Start DD1 yourself. Keep Hero 1 on keyboard. Spawn extra heroes with `F6` if needed. During the wait, assign each new Xbox controller to a companion hero. Do not press `F2`–`F5`.

Older diagnostics:

```text
python src/main.py test-gamepad
python src/main.py test-player2
```
