# DD1 AI Companion

A small technical prototype for **Dungeon Defenders 1** on Windows/Steam. The long-term idea is to control extra local characters as AI companions during private play. This repository is not a bot, a trainer, or a complete companion system.

Intended use is **local / private gameplay**. The program sits outside the game: no memory reads, no DLL injection, no game patches, and no Steam or anti-cheat bypass.

## Architecture

Prototypes 0 and 1 are **PASSED**. Three virtual Xbox / XInput pads can drive Heroes 2–4 while the human keeps Hero 1.

```text
Human Player 1  →  keyboard / mouse (or a physical pad)
Bot Player 2    →  virtual XInput controller #1
Bot Player 3    →  virtual XInput controller #2
Bot Player 4    →  virtual XInput controller #3
```

Pads stay connected for the life of the companion program.

Keyboard `F2`–`F5` switching works and is **rejected**: it steals the human's hero.

Current phase: **movement characterization** (not navigation). Stick time is not a map coordinate and not a camera angle.

See `docs/plan.md`, `docs/input-research.md`, and `docs/movement-characterization.md`.

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

Current (watch analog speeds, then write notes):

```text
python src/main.py test-movement
```

Already verified:

```text
python src/main.py test-companion
python src/main.py test-three-companions
```

Older diagnostics:

```text
python src/main.py test-gamepad
python src/main.py test-player2
```
