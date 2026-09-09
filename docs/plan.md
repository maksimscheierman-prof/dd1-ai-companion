# Development plan

This is a rough phase list. Each phase should stay small. Do not start the next phase until the current one has a clear yes/no result.

Runtime feature work is **paused**. Do not start screen capture, OpenCV, or a telemetry mod until the checklist below is done.

## NEXT SESSION START HERE

1. Install / locate the Dungeon Defenders Development Kit.
2. Inspect `Development/Src`.
3. Identify player / world-state classes.
4. Determine whether a tiny telemetry mod can print P2–P4 positions.
5. Only then decide between:
   - DDDK telemetry (preferred if feasible)
   - screen vision fallback
   - other approaches

Questions and constraints: `docs/dddk-telemetry-research.md`.

Do **not** start with process-memory reading, DLL injection, hooks, packet manipulation, or anti-cheat bypass. Those are last-resort only if official/local modding cannot export state.

---

## Prototype 0: Input feasibility — PASSED

Shared-keyboard switching works and is **rejected** as the companion path (`F3` steals Hero 1).

Virtual Xbox 360 / XInput control is the passing architecture.

Keep `test-player2` and `test-gamepad` as diagnostics only.

## Prototype 1: Persistent companion control — PASSED

Up to three companions, each on its own virtual XInput pad, staying connected until shutdown.

```text
Human Player 1  →  keyboard / mouse
Bot Player 2    →  virtual XInput #1
Bot Player 3    →  virtual XInput #2
Bot Player 4    →  virtual XInput #3
```

Manually verified: three pads coexist, receive independent input at the same time, keep their assignments, and leave Hero 1 under human control. Basic movement and jump work.

## Prototype 1b: Movement characterization — DONE (qualitative)

`python src/main.py test-movement`

Partial analog magnitudes (25% / 50% / 100%) did **not** look meaningfully different for movement speed. Planning default is **full stick + neutral** unless later evidence says otherwise.

Stick duration is still not a map coordinate or a camera angle. Notes: `docs/movement-characterization.md`.

## Prototype 2: Perception — BLOCKED

Blocked on **DDDK / UnrealScript telemetry feasibility**.

Preferred: the game (or a small official-kit mod) exports state for Players 2–4 while the human stays in normal full-screen Player 1 play.

```text
DD1  →  telemetry  →  Python bot  →  pads 2/3/4  →  DD1
```

Screen capture / split-screen / camera-switching vision is a **fallback**, not the preferred first solution. Split-screen or cycling P2–P4 cameras would hurt the human experience.

Do not implement OpenCV, OCR, or screenshot navigation until telemetry is ruled out or shown insufficient.

## Prototype 3: Navigation and map-specific scripts

Only after a state source exists (telemetry or, if needed, vision). Scripts stay map-specific. No general pathfinding yet.

## Later

Only after the early prototypes are proven:

- combat logic
- building logic
- higher-level AI decision making
- replace ViGEm if it becomes unusable (HIDMaestro is the first fallback)
