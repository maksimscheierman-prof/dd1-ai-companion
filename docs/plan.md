# Development plan

This is a rough phase list. Each phase should stay small. Do not start the next phase until the current one has a clear yes/no result.

## Prototype 0: Shared-keyboard feasibility — done, rejected as main path

Local-player switching on the shared keyboard is **verified**:

- `F2`–`F5` select Heroes 1–4
- `F6` / `F7` spawn / remove extras
- Synthetic scan-code `SendInput` is accepted by DD1

That path is **VERIFIED TECHNICALLY, REJECTED FOR MAIN CONTROL PATH**. `F3` steals active control from the human. Keep `python src/main.py test-player2` for diagnostics only.

## Prototype 0B: Independent virtual-controller feasibility

Current work. Goal: control Hero 2 from a virtual Xbox/XInput pad while the human keeps Hero 1.

Success criteria:

- Dungeon Defenders is already running
- Hero 1 is controlled normally by the human
- Hero 2 is assigned to a separate controller slot
- Our Python program exposes a virtual Xbox-compatible controller
- The virtual controller moves Hero 2
- Hero 1 remains controllable at the same time
- The program does **not** switch heroes with `F2`–`F5`
- The program does **not** need DD1's currently selected hero slot

Do not launch the game, attach to its process, or send keyboard hero-select keys.

## Prototype 1: Basic scripted companion

If Prototype 0B works, drive the extra character with a fixed pad script:

- move
- stop
- jump
- trigger a simple action
- execute a predefined sequence

Still no decision-making. The companion should do exactly what the script says.

## Prototype 2: Game-state perception

Explore whether we can tell what is happening without reading game memory:

- screenshots / screen capture
- detect simple UI or game-state signals (menus, ready prompts, obvious HUD markers)

No advanced computer vision in this phase. The goal is to find cheap, reliable signals.

## Prototype 3: Navigation and map-specific scripts

Use the input path and any cheap state signals to walk predefined routes on known maps. Scripts stay map-specific. No general pathfinding yet.

## Later

Only after the early prototypes are proven:

- combat logic
- building logic
- multiple companions
- higher-level AI decision making
- replace ViGEm if it becomes unusable (HIDMaestro is the first fallback)
