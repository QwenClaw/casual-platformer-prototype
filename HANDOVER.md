## 1. What Was Built

A casual 2D platformer prototype built with Python and Pygame. The game features a player character that can run, jump, and stomp on patrolling enemies across a single hardcoded level. The player must navigate platforms, avoid or defeat enemies by jumping on them, and reach a goal to complete the level. Game states include active play, death (with restart option), and level completion overlays.

## 2. Getting Started

**Prerequisites:**
- Python 3.8+
- Pygame (`pip install pygame`)

**Install:**
```bash
pip install pygame
```

**Run:**
```bash
python main.py
```

**Controls:**
- Arrow keys or WASD to move
- Space or Up arrow to jump
- R to restart after death or level completion

No environment variables or external config files are needed. The game generates simple tone-based sound effects if `.wav` asset files are not present.

## 3. Project Status

| Issue | Title | Status |
|-------|-------|--------|
| #68 | Fix game over screen and restart flow | ⚠️ Needs Rework |
| #73 | Missing visual indication of restart option on game over screen | ✅ Done |

## 4. Known Issues

- **#68 — GAME_COMPLETE restart bug:** The restart flow has a critical bug when in the `GAME_COMPLETE` state. Restarting from this state does not behave correctly.
- **#68 — LEVEL_COMPLETE overlay text:** The overlay text displayed during the `LEVEL_COMPLETE` state is inconsistent or incorrect.

## 5. How to Resume

To continue development, run:

```
python agency.py --resume casual-platformer-prototype --cycles 3
```

This will pick up open issues and run up to 3 more dev cycles.