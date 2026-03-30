# HANDOVER.md

## 1. What Was Built
A playable 2D platformer prototype featuring a player character that can run, jump, and defeat enemies by stomping on them. The game includes a single level with platforms, patrolling enemies, a goal to reach, and basic sound effects. Core mechanics like collision detection, game state management (playing, dead, level complete), and enemy AI are fully implemented and functional.

## 2. Getting Started
**Prerequisites:** Python 3.6+ and Pygame.

**Installation:**
```bash
pip install pygame
```

**Running the game:**
```bash
python main.py
```
No environment variables or additional configuration is required. The game will launch in a window and can be controlled with arrow keys and the spacebar.

## 3. Project Status

| Issue | Title | Status |
|-------|-------|--------|
| #23 | 11. Game States | ⚠️ Needs Rework |
| #68 | Fix game over screen and restart flow | ⚠️ Needs Rework |

## 4. Known Issues
- **Issue #23:** The implementation adds level progression and a game complete state but fails to implement the required main menu and pause menu. The code also introduces unplanned features like gravity toggling and multiple levels.
- **Issue #68:** There is a critical bug in the restart flow for the `GAME_COMPLETE` state and inconsistent behavior in the `LEVEL_COMPLETE` state overlay text.

## 5. How to Resume
To continue development, run:

    python agency.py --resume casual-platformer-prototype --cycles 3

This will pick up open issues and run up to 3 more dev cycles.