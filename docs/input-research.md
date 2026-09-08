# Input research (Prototype 0)

Questions that must be answered before we pick an input library or write a controller backend. Do not treat anything marked **TO VERIFY** as a fact.

This project will only use an external input path. Process injection, memory reads, DLL hooks, game patches, and Steam/anti-cheat bypass are out of scope.

## Local multiplayer in DD1

- How does Dungeon Defenders 1 support local multiplayer on PC? **TO VERIFY**
- How many local characters can exist in one session? **TO VERIFY**
- How is a second local player added (in-game prompt, extra controller connect, split keyboard, something else)? **TO VERIFY**
- What input devices does the Steam Windows build accept for extra local players (keyboard, mouse, XInput gamepad, DirectInput, other)? **TO VERIFY**

## Controllers and device identity

- Can multiple local characters be controlled using separate Xbox / XInput controllers? **TO VERIFY**
- Does DD1 distinguish individual controller devices reliably (gamepad A always maps to player 2, gamepad B to player 3, etc.)? **TO VERIFY**
- If two pads are connected, can each pad move only its own character? **TO VERIFY**
- Does the game bind pads by XInput user index (0–3), by connection order, or by some other rule? **TO VERIFY**
- Can player 1 stay on keyboard/mouse while another character is bound to a pad? **TO VERIFY**

## Virtual gamepads

- Can a virtual controller be exposed to the game as a separate player? **TO VERIFY**
- Does DD1 treat a virtual Xbox-compatible pad the same as a physical one? **TO VERIFY**
- After a virtual pad appears, does the game create or join a new local character without extra manual steps? **TO VERIFY**

Candidate Windows tools and libraries (not chosen yet; evaluate only after the questions above):

- ViGEmBus and a user-mode client such as `vgamepad` — virtual Xbox 360 / DualShock devices
- vJoy / `pyvjoy` — virtual DirectInput joysticks
- raw `SendInput` / similar — keyboard and mouse events
- native XInput inspection (read-only) to see which user slots the OS reports

Do not add these dependencies until the input approach is verified.

## Steam Input

- Are there limitations if Steam Input is enabled? **TO VERIFY**
- Does Steam Input merge or remap pads so DD1 no longer sees distinct devices? **TO VERIFY**
- Do we need to disable or configure Steam Input for reliable per-player control? **TO VERIFY**
- Is the result different for "Dungeon Defenders" specifically vs. Steam's global controller settings? **TO VERIFY**

## Isolation from player 1

- When we send input to the extra character, does player 1's keyboard/mouse remain untouched? **TO VERIFY**
- Does focusing the DD1 window, overlay, or Steam Big Picture cause our input to leak to player 1? **TO VERIFY**
- Does the game require the window to be focused for pad input? **TO VERIFY**

## Suggested first experiment

1. Launch DD1 on Windows via Steam with one physical Xbox-compatible pad connected.
2. Confirm how a second local character is created and which device controls it.
3. Repeat with Steam Input enabled, then disabled / per-game off, and note any difference.
4. Only after a physical pad can control player 2 without moving player 1, try a virtual pad.

Until that experiment is done, treat keyboard-only extra-player control and virtual pads as unproven.
