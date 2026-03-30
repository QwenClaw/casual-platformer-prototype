# HANDOVER.md

## 1. What Was Built
A simple 2D platformer prototype where the player runs, jumps, stomps on enemies, and reaches a goal to complete the level. The game includes a single hardcoded level with platforms, patrolling enemies, and a win condition. The final development cycle fixed two UI issues: making the restart prompt on the game-over screen more visible and correcting the instruction text on the level-complete screen.

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
No configuration or environment variables are needed. The game will open in a new window.

## 3. Project Status

| Issue | Title | Status |
|-------|-------|--------|
| #73 | Missing visual indication of restart option on game over screen | ✅ Done |
| #72 | LEVEL_COMPLETE overlay text shows incorrect restart instruction | ✅ Done |

## 4. Known Issues
None — all implemented features passed QA review.