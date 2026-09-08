# Development plan

This is a rough phase list. Each phase should stay small. Do not start the next phase until the current one has a clear yes/no result.

## Prototype 0: Input feasibility

Determine how Dungeon Defenders 1 handles multiple local players on Windows.

Investigate whether additional local players are best controlled through:

- keyboard input
- physical or virtual Xbox-compatible gamepads
- another Windows input interface

**Goal:** control one additional local character independently.

**Minimum success case:**

- DD1 is running
- a second local character exists
- our program can send movement input to that character
- inputs for player 1 are not affected

This phase is research and a tiny external sender only. No combat logic, pathfinding, or vision.

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
