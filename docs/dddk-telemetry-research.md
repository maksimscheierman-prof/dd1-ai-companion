# DDDK / UnrealScript telemetry research

Research questions only. Mark findings **VERIFIED** or **TO VERIFY**. Do not treat the lists below as facts about the kit.

Goal: decide whether Dungeon Defenders 1 can expose a little game state through its official Development Kit / UnrealScript, so the Python companion does not need split-screen or camera-switching vision.

Player 1 should stay in normal full-screen play. Pads 2–4 already work as independent XInput devices.

```text
Dungeon Defenders 1
        |
        | game-state / telemetry
        v
     Python bot
   /      |      \
Pad 2   Pad 3   Pad 4
        |
        v
Dungeon Defenders 1
```

Prefer official/local modding. Do **not** implement process-memory reading, DLL injection, code injection, game hooks, packet manipulation, or anti-cheat bypass for this research. Those are later last-resorts only.

Do **not** start OpenCV, OCR, screenshot navigation, object detection, AI, pathfinding, combat, or building logic until this document has real answers.

## Development Kit

- Where is the Dungeon Defenders Development Kit installed? **TO VERIFY**
- What gameplay source is under its `Development/Src` tree? **TO VERIFY**
- Which UnrealScript packages/classes represent the following? **TO VERIFY** for each:
  - player controllers
  - hero / player pawns
  - enemies
  - towers / defenses
  - crystals / objectives
  - build phase
  - combat phase
  - wave state
  - mana
  - health
  - map / world state

Record install path, package names, and class names only after you have seen them in the kit.

## Player telemetry

Can UnrealScript access, for **each local player** (especially P2–P4): **TO VERIFY** for each field

- player index / local player identity
- actor / pawn reference
- world position
- rotation / facing
- health
- mana
- alive / dead
- current hero / class, if available

## World telemetry

Can game code enumerate or inspect: **TO VERIFY** for each

- enemies
- enemy positions
- enemy health
- defenses / towers
- defense positions
- crystals / objectives
- current build / combat phase
- current wave
- remaining enemy count
- dropped mana or other useful world objects

## Output / IPC

Practical ways to send a small payload from UnrealScript to the external Python process. **TO VERIFY** for each; none are assumed to work:

- Unreal / UDK log output
- file output, if supported
- localhost UDP
- localhost TCP
- console / debug output
- any existing DD1 modding hook that is suitable for **local** telemetry

Do not pick an IPC method until one of these is shown to work from a tiny test.

## First proof of concept

If anything is exported at all, keep the first payload extremely small, about every 250–500 ms:

```text
P2 position
P3 position
P4 position
current phase
current wave
enemy count
```

If that works, expand later. If it does not, document why and then consider the screen-vision fallback.

## Decision after this research

| Outcome | Next step |
| --- | --- |
| Tiny telemetry works | Read it from Python; keep pads as they are |
| Kit exists but cannot export | Revisit screen vision as a fallback (without forcing split-screen if possible) |
| Kit missing or unusable | Same fallback discussion; still no memory/DLL work unless explicitly decided later |

## Notes from install (fill in next session)

- DDDK install path:
- `Development/Src` present: (yes / no)
- Packages opened:
- Classes that look relevant:
- Any log/file/socket test attempted:
- POC result (P2–P4 positions printed or not):
