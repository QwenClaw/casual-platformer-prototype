# HANDOVER.md

## 1. What Was Built
A 2D platformer prototype built with Python and Pygame. The game features a player character that can run, jump, and defeat enemies by stomping on them. It includes a single hardcoded level with platforms, patrolling enemies, and a goal to reach. The prototype handles basic physics, collision detection, sound effects, and game state management (playing, dead, level complete).

## 2. Getting Started
**Prerequisites:** Python 3.x installed on your system.

**Installation:**
```bash
pip install pygame
```

**Running the game:**
```bash
python main.py
```

**Controls:**
- Arrow keys or WASD to move
- Space or Up arrow to jump
- R to restart current level
- N to advance to next level (when level is complete)

No environment variables or additional configuration required. The game will generate simple sound effects if audio files are missing.

## 3. Project Status

| Issue | Title | Status |
|-------|-------|--------|
| #72 | LEVEL_COMPLETE overlay text shows incorrect restart instruction | ✅ Done |
| #75 | Some weird issue on jumping | ⚠️ Needs Rework |
| #71 | Restart in GAME_COMPLETE state doesn't reset entire game | ✅ Done |
| #67 | Unimplemented feature | ❌ Not Started |
| #65 | Unimplemented feature | ❌ Not Started |
| #64 | Unimplemented feature | ❌ Not Started |
| #63 | Unimplemented feature | ❌ Not Started |
| #62 | Unimplemented feature | ❌ Not Started |
| #61 | Unimplemented feature | ❌ Not Started |
| #60 | Unimplemented feature | ❌ Not Started |
| #59 | Unimplemented feature | ❌ Not Started |
| #58 | Unimplemented feature | ❌ Not Started |
| #57 | Unimplemented feature | ❌ Not Started |
| #54 | Unimplemented feature | ❌ Not Started |
| #53 | Unimplemented feature | ❌ Not Started |
| #52 | Unimplemented feature | ❌ Not Started |
| #50 | Unimplemented feature | ❌ Not Started |
| #49 | Unimplemented feature | ❌ Not Started |
| #48 | Unimplemented feature | ❌ Not Started |
| #46 | Unimplemented feature | ❌ Not Started |
| #44 | Unimplemented feature | ❌ Not Started |
| #43 | Unimplemented feature | ❌ Not Started |

## 4. Known Issues
- **Incorrect vertical velocity clamping when gravity is reversed** (from issue #75): In `player.py`, when gravity is reversed, the vertical velocity clamping logic incorrectly sets velocity to a positive value instead of negative, which could cause unexpected direction changes during jumps.

## 5. How to Resume
To continue development, run:

```
python agency.py --resume casual-platformer-prototype --cycles 3
```

This will pick up open issues (#75 and the 19 unimplemented features) and run up to 3 more dev cycles.