# HANDOVER.md

## 1. What Was Built
A 2D platformer prototype where a player can run, jump, and stomp on enemies to reach a goal. The game includes basic physics, collision detection, sound effects, and a simple level with platforms and patrolling enemies. The core gameplay loop—moving, jumping, dying, and winning—is fully functional.

## 2. Getting Started
**Prerequisites:** Python 3.8+ and Pygame.

1. Install dependencies:
   ```bash
   pip install pygame
   ```
2. Run the game:
   ```bash
   python main.py
   ```
No environment variables or additional configuration is required.

## 3. Project Status

| Issue | Title | Status |
|-------|-------|--------|
| #72 | LEVEL_COMPLETE overlay text shows incorrect restart instruction | ✅ Done |
| #75 | Some wierd issue on jumping | ⚠️ Needs Rework |
| #71 | Restart in GAME_COMPLETE state doesn't reset entire game | ✅ Done |
| #67 | Implement pause menu functionality | ⚠️ Needs Rework |
| #65 | Unknown (title not available) | ❌ Not Started |
| #64 | Unknown (title not available) | ❌ Not Started |
| #63 | Unknown (title not available) | ❌ Not Started |
| #62 | Unknown (title not available) | ❌ Not Started |
| #61 | Unknown (title not available) | ❌ Not Started |
| #60 | Unknown (title not available) | ❌ Not Started |
| #59 | Unknown (title not available) | ❌ Not Started |
| #58 | Unknown (title not available) | ❌ Not Started |
| #57 | Unknown (title not available) | ❌ Not Started |
| #54 | Unknown (title not available) | ❌ Not Started |
| #53 | Unknown (title not available) | ❌ Not Started |
| #52 | Unknown (title not available) | ❌ Not Started |
| #50 | Unknown (title not available) | ❌ Not Started |
| #49 | Unknown (title not available) | ❌ Not Started |
| #48 | Unknown (title not available) | ❌ Not Started |
| #46 | Unknown (title not available) | ❌ Not Started |
| #44 | Unknown (title not available) | ❌ Not Started |
| #43 | Unknown (title not available) | ❌ Not Started |

## 4. Known Issues
- **Issue #75:** Critical bug in player physics: incorrect vertical velocity clamping when gravity is reversed, which could cause unexpected direction changes and jumping weirdness.
- **Issue #67:** Pause menu functionality is completely missing. No pause state, no ESC/P key handling, no pause menu display, and no resume/restart from pause.

## 5. How to Resume
To continue development, run:

    python agency.py --resume casual-platformer-prototype --cycles 3

This will pick up open issues and run up to 3 more dev cycles.