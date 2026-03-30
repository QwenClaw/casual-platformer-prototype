# HANDOVER.md

## 1. What Was Built

A casual 2D platformer prototype built with Python and Pygame. The game features a player character with acceleration-based movement and jumping, patrolling enemies that can be stomped on, a single hardcoded level with platforms and a goal, and a state machine handling playing, death, and level-complete screens. Sound effects (with generated fallback tones) and visual effects are included. The LEVEL_COMPLETE overlay text was fixed to correctly display restart/next-level instructions.

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
- Arrow keys / WASD — move and jump
- R — restart current level
- N — next level (on level complete screen)

No environment variables or additional configuration required.

## 3. Project Status

| Issue | Title | Status |
|-------|-------|--------|
| #72 | LEVEL_COMPLETE overlay text shows incorrect restart instruction | ✅ Done |
| #75 | Some wierd issue on jumping | ⚠️ Needs Rework |
| #71 | — | ❌ Not Started |
| #67 | — | ❌ Not Started |
| #65 | — | ❌ Not Started |
| #64 | — | ❌ Not Started |
| #63 | — | ❌ Not Started |
| #62 | — | ❌ Not Started |
| #61 | — | ❌ Not Started |
| #60 | — | ❌ Not Started |
| #59 | — | ❌ Not Started |
| #58 | — | ❌ Not Started |
| #57 | — | ❌ Not Started |
| #54 | — | ❌ Not Started |
| #53 | — | ❌ Not Started |
| #52 | — | ❌ Not Started |
| #50 | — | ❌ Not Started |
| #49 | — | ❌ Not Started |
| #48 | — | ❌ Not Started |
| #46 | — | ❌ Not Started |
| #44 | — | ❌ Not Started |
| #43 | — | ❌ Not Started |

## 4. Known Issues

- **Incorrect vertical velocity clamping when gravity is reversed** (from #75): In `player.py`, when `gravity_direction < 0`, the vertical velocity clamping logic sets velocity to a positive value instead of negative, causing unexpected direction changes during reversed-gravity jumps. This may also be related to a reported movement issue near the goal in level 2.

## 5. How to Resume

To continue development, run:

```
python agency.py --resume casual-platformer-prototype --cycles 3
```

This will pick up open issues and run up to 3 more dev cycles.