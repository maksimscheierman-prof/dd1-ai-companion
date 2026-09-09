# Movement characterization

Time-based analog-stick input is **not** a coordinate or navigation system.

Distance traveled can change with hero movement speed, equipment, buffs/debuffs, collisions, slopes, framerate, and stick deadzones. Right-stick hold time is **not** a camera angle.

Command: `python src/main.py test-movement`

## Planning conclusion (manual observation)

25% / 50% / 100% left-stick forward did **not** appear meaningfully useful as different movement speeds.

Until later evidence says otherwise, companions should use **full stick + neutral** only. Do not build a speed-band or dead-reckoning navigator on partial stick values.

No distances or angles were recorded. Do not invent them.

## Session template (optional later runs)

- Date:
- Hero / class:
- Movement-speed stat:
- Map / location:
- Notes on ground (flat, stairs, crowded):

### Left stick forward (2 seconds each)

- 25% stick:
- 50% stick:
- 100% stick:
- Did 50% look about halfway between 25% and 100%? (yes / no / unclear): **no — partial magnitudes did not look useful**
- Observed deadzone (lowest stick value that still moved, if you tried):
- Did the same command look repeatable on a second run? (yes / no / not retested):

### Right stick

- Command used: X = 50% for 1 second, then neutral
- What happened (camera yaw, hero turn, nothing, other):
- Did hold time look like a reliable angle? (yes / no / unclear):

### Other

- Jump after the last 100% forward:
- Hero 1 still independently controllable:
- Extra notes:
