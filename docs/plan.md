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

## Prototype 1: Persistent companion control — PASSED

Up to three companions, each on its own virtual XInput pad, staying connected until shutdown.

```text
Human Player 1  →  keyboard / mouse
Bot Player 2    →  virtual XInput #1
Bot Player 3    →  virtual XInput #2
Bot Player 4    →  virtual XInput #3
```

Manually verified: three pads coexist, receive independent input at the same time, keep their assignments, and leave Hero 1 under human control.

## Prototype 1b: Movement characterization — current

Small analog-stick experiment only. `python src/main.py test-movement`

Goal: see how 25% / 50% / 100% forward and a short right-stick hold look in-game.

This is **not** navigation. Stick duration is not a distance or an angle. Record observations in `docs/movement-characterization.md`.

## Prototype 2: Game-state perception

Explore whether we can tell what is happening without reading game memory:

- screenshots / screen capture
- detect simple UI or game-state signals (menus, ready prompts, obvious HUD markers)

No advanced computer vision in this phase. The goal is to find cheap, reliable signals.

Dead-reckoning from stick time is not a substitute for perception. Even if movement looks smooth, later bots will still need some external state signal.

## Prototype 3: Navigation and map-specific scripts

Use the input path and any cheap state signals to walk predefined routes on known maps. Scripts stay map-specific. No general pathfinding yet.

## Later

Only after the early prototypes are proven:

- combat logic
- building logic
- higher-level AI decision making
- replace ViGEm if it becomes unusable (HIDMaestro is the first fallback)
