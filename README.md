# DD1 AI Companion

A small technical prototype for **Dungeon Defenders 1** on Windows/Steam. The long-term idea is to control extra local characters as AI companions during private play. This repository is not a bot, a trainer, or a complete companion system.

The current phase is only a **feasibility prototype**. Before any companion behavior exists, we need to know whether a second local character can be driven from an external program without touching player 1's input. That single question decides whether the rest of the project is worth building.

Intended use is **local / private gameplay** with characters that already belong to the local session. The program should sit outside the game: no memory reads, no DLL injection, no game patches, and no Steam or anti-cheat bypass. If independent local input is possible, later prototypes can add scripted movement, crude game-state perception, and map-specific helpers. If it is not possible, the project stops at Prototype 0.

See `docs/plan.md` for phases and `docs/input-research.md` for verified local-player keys and open questions.

```text
pip install -r requirements.txt
python src/main.py test-player2
```

Start Dungeon Defenders yourself, spawn Hero 2 (`F6`), then focus the game window during the countdown. The script only sends `F3` and a one-second `W` hold.
