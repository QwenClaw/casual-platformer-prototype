# HANDOVER.md

## 1. What Was Built
A 2D platformer prototype where the player runs, jumps, and stomps on enemies to reach a goal. The game includes a single hardcoded level with platforms, patrolling enemies, and a win condition. Core mechanics like physics, collision detection, and basic sound effects are implemented. Two features—damage feedback and full game state menus—were not completed to QA standards.

## 2. Getting Started
**Prerequisites:** Python 3.8+ and Pygame.

**Install:**
```bash
pip install pygame
```

**Run:**
```bash
python main.py
```
No environment variables or additional configuration are required.

## 3. Project Status

| Issue | Title | Status |
|-------|-------|--------|
| #42 | Add visual feedback (flash/red tint) when player takes damage | ⚠️ Needs Rework |
| #23 | 11. Game States | ⚠️ Needs Rework |

## 4. Known Issues
- **#42:** Player dies immediately on non-stomp enemy collision with no invincibility frames or visual damage feedback. The effect system was added but not integrated for damage.
- **#23:** Main menu and pause menu are missing. Game over/restart is partially implemented but lacks proper menu interfaces. Unrequested features (gravity toggling, multiple levels) were added.

## 5. How to Resume
To continue development, run:

    python agency.py --resume casual-platformer-prototype --cycles 3

This will pick up open issues and run up to 3 more dev cycles.