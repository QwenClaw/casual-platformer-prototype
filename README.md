# Casual Platformer Prototype

A single-level, playable desktop platformer game that replicates the core mechanics and "feel" of a classic side-scroller for personal enjoyment and commercial viability assessment.

## Goals

- Deliver an immediately playable and fun platforming experience.
- Implement the essential gameplay loop: run, jump, interact with enemies, and reach a goal.
- Create a polished, single level that demonstrates the core mechanics.
- Establish a solid technical and gameplay foundation for potential future expansion.

---
## Architecture

**Python 3 + Pygame** — Pygame is the most straightforward library for a 2D sprite-based platformer in Python. It provides hardware-accelerated rendering, collision primitives (`pygame.sprite`), built-in audio mixing, and a tight game-loop model. No external dependencies beyond Pygame are needed, keeping the prototype zero-friction to run.

### Project Files

- `main.py` — Entry point: initializes Pygame, creates a Game instance, and calls game.run() to start the loop.
- `constants.py` — All configuration constants: screen dimensions, FPS, physics values (gravity, jump force, player speed), tile size, and color tuples.
- `game.py` — Game class: owns the main loop (handle_events → update → draw), manages game state (PLAYING/DEAD/LEVEL_COMPLETE), and coordinates all other components.
- `player.py` — Player sprite class: handles horizontal acceleration/deceleration, gravity, jumping, and exposes rect/velocity for collision; die() and win() methods trigger state changes.
- `enemy.py` — Enemy sprite class: patrols between two x-coordinates, reverses direction at bounds, and exposes rect for collision stomp detection.
- `level.py` — Level class: builds and stores the single hardcoded level — platform rects, enemy spawn data, player spawn point, and goal rect.
- `renderer.py` — Renderer class: draws platforms, player, enemies, goal marker, and state-overlay text (win/dead) to the screen each frame.
- `collision.py` — Collision utility functions: axis-separated platform collision resolution, enemy stomp-vs-hit detection, and goal reach check — all pure functions.
- `sound_manager.py` — SoundManager class: loads or synthesizes sound effects for jump, stomp, and win events; gracefully no-ops if audio is unavailable.

_See `architecture.md` for the full design._

---

_Development log will be appended as issues are completed._

## Development Log

### Cycle 1 — #1: Create project constants and entry point

**APPROVE** — The implementation fully meets all acceptance criteria. constants.py contains all specified constants with correct values, main.py provides a functional entry point that runs without errors, and the minimal game.py stub ensures the game loop executes properly. No critical bugs or missing requirements were found.

### Cycle 2 — #2: Implement player character with physics

**APPROVE** — The Player class implementation fully meets all acceptance criteria. It correctly handles physics with acceleration/deceleration, gravity, jumping, and platform collisions. The sprite renders as a red rectangle, movement feels responsive, and collision detection prevents passing through platforms from any direction.

### Cycle 3 — #3: Implement enemy and level data

**APPROVE** — The implementation fully meets all acceptance criteria. The Enemy class correctly patrols between bounds, and the Level class provides a complete level with gaps, multiple floating platforms, enemies, and properly positioned goal and spawn points. All required components are present and functional.

### Cycle 4 — #4: Implement collision detection system

**APPROVE** — The collision system implementation meets all acceptance criteria. Axis-separated collision resolution works correctly for platform landing and wall sliding. Enemy collision detection properly distinguishes stomps from side hits. Goal collision detection functions as specified. The code is clean and follows the architecture.

### Cycle 5 — #5: Implement sound manager with fallback

**APPROVE** — The SoundManager implementation fully meets all acceptance criteria. It properly initializes pygame.mixer with graceful fallback, generates appropriate programmatic sounds when .wav files are missing, and integrates correctly with the game loop to play sounds for jumps, stomps, and winning. The code handles audio device unavailability with try/except blocks and no-op fallbacks.

### Cycle 6 — #6: Implement game loop, renderer, and wire components

**APPROVE** — The implementation fully meets all acceptance criteria. The game window opens at 800x600, player movement and physics work correctly, enemies patrol and can be stomped or kill the player, reaching the goal shows 'LEVEL COMPLETE' and stops gameplay, dying shows 'GAME OVER' with reset functionality, all components are properly wired together, and the game runs at a stable 60 FPS.

### Cycle 7 — #25: 14. Minimal Content Scope (IMPORTANT)

**APPROVE** — The implementation fully meets the acceptance criteria: 7 handcrafted levels (within the 5-10 range), 3 distinct enemy types (standard, fast, flying), and a unique gravity toggle mechanic. The code is well-structured, integrates the new features cleanly with existing systems, and includes appropriate sound effects and UI feedback.
