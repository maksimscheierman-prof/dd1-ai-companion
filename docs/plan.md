# Development plan

This is a rough phase list. Each phase should stay small. Do not start the next phase until the current one has a clear yes/no result.

## Prototype 0: Input feasibility — PASSED

Shared-keyboard switching works and is **rejected** as the companion path (`F3` steals Hero 1).

Virtual Xbox 360 / XInput control is the passing architecture:

- ViGEmBus + `vgamepad` creates a virtual pad
- DD1 treats it as an independent local player
- Hero 2 can move and jump from that pad
- Human Hero 1 stays independently controllable
- No `F2`–`F5` switching is required

Keep `test-player2` and `test-gamepad` as diagnostics only.

## Prototype 1: Persistent companion control layer — current

A small API that can drive up to three companions without exposing `vgamepad` to the rest of the program.

```text
Human Player 1  →  keyboard / mouse
Bot Player 2    →  virtual XInput #1  (stays connected)
Bot Player 3    →  virtual XInput #2  (stays connected)
Bot Player 4    →  virtual XInput #3  (stays connected)
```

In scope:

- `CompanionController` / `CompanionManager`
- movement, stop, jump, button/trigger primitives
- timed actions that always release
- one-companion and three-companion manual tests

Out of scope: AI, vision, pathfinding, combat/building decisions, launching DD1, process hooks.

Controller creation order is **not** assumed to equal DD1 player slots. Validate that mapping with `test-three-companions` before treating player 2/3/4 as reliable hardware slots.

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
- higher-level AI decision making
- replace ViGEm if it becomes unusable (HIDMaestro is the first fallback)
