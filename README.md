# DD1 AI Companion

A small technical prototype for **Dungeon Defenders 1** on Windows/Steam. The long-term idea is to control extra local characters as AI companions during private play. This repository is not a bot, a trainer, or a complete companion system.

Intended use is **local / private gameplay**. The program sits outside the game: no memory reads, no DLL injection, no game patches, and no Steam or anti-cheat bypass.

## Architecture decision

**Preferred direction**

```text
Human Player 1  (keyboard / mouse, or a physical pad)
        +
Independent virtual Xbox/XInput companions  (Hero 2+)
```

Keyboard hero switching (`F2`–`F5`) **works** and is **rejected** as the companion path: it steals the human's active hero. That command remains only as a diagnostic.

Current phase: **Prototype 0B** — can a virtual Xbox 360 controller move Hero 2 while the human still controls Hero 1?

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

Preferred (Prototype 0B):

```text
python src/main.py test-gamepad
```

Start DD1 yourself, keep Hero 1 on keyboard, spawn Hero 2 (`F6`) if needed. During the wait, assign the new Xbox controller to Hero 2. Do not press `F2`–`F5`. If the pad is swallowed by Steam, disable Steam Input for Dungeon Defenders and retry.

Diagnostic only (rejected path):

```text
python src/main.py test-player2
```
