# Movement characterization

Time-based analog-stick input is **not** a coordinate or navigation system.

Distance traveled can change with hero movement speed, equipment, buffs/debuffs, collisions, slopes, framerate, and stick deadzones. Right-stick hold time is **not** a camera angle.

Use `python src/main.py test-movement` and fill this in from what you actually see. Leave blanks if you did not measure something. Do not invent numbers.

## Session

- Date:
- Hero / class:
- Movement-speed stat:
- Map / location:
- Notes on ground (flat, stairs, crowded):

## Left stick forward (2 seconds each)

- 25% stick:
- 50% stick:
- 100% stick:
- Did 50% look about halfway between 25% and 100%? (yes / no / unclear):
- Observed deadzone (lowest stick value that still moved, if you tried):
- Did the same command look repeatable on a second run? (yes / no / not retested):

## Right stick

- Command used: X = 50% for 1 second, then neutral
- What happened (camera yaw, hero turn, nothing, other):
- Did hold time look like a reliable angle? (yes / no / unclear):

## Other

- Jump after the last 100% forward: (worked / failed / not watched)
- Hero 1 still independently controllable: (yes / no)
- Extra notes:
