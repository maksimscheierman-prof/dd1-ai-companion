# Development plan

This is a rough phase list. Each phase should stay small. Do not start the next phase until the current one has a clear yes/no result.

## Prototype 0: Input feasibility

Local-player **switching** on the shared keyboard is **verified**:

- `F2`–`F5` select Heroes 1–4
- `F6` spawns extra configured heroes
- `F7` removes extras
- `F8` leaves split-screen; `F2`–`F5` still switch the selected hero

Remaining question: can an **external** Python process send those same keys and move the selected hero?

Immediate Prototype 0 success condition:

- Dungeon Defenders is already running
- Heroes 1 and 2 are already spawned
- Run our Python command
- The script selects Hero 2 with `F3`
- The script waits briefly
- It holds `W` for approximately one second
- It releases `W`
- No other actions are performed

Do not launch the game, attach to its process, or use virtual controllers for this check.

## Prototype 1: Basic scripted companion

If Prototype 0 works, drive the extra character with a fixed script:

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
- virtual gamepads, only if shared-keyboard control is not enough
