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

### Cycle 8 — #24: 12. Bug Fixing & Edge Cases

**APPROVE** — The implementation successfully addresses all acceptance criteria: collision glitches are fixed with substep collision resolution, player clipping is prevented through velocity clamping and axis-separated collision, multiple enemy collisions are handled by processing stomps first, and inconsistent jump behavior is fixed with coyote time and jump buffering. The code also includes robust edge case handling for gravity direction and screen bounds.

### Cycle 9 — #22: 10. “World Change” Mechanic (Your USP)

**REQUEST_CHANGES** — The implementation adds gravity toggle and multiple levels but does not implement the core 'World Change' mechanic. There is no effect system manager, no random effects triggered when enemies are killed, and no display of active effects to the player. The gravity toggle is player-initiated rather than triggered by enemy kills.

### Cycle 10 — #21: 9. Sound Effects

**REJECT** — Failed to parse QA output: Expecting value: line 1 column 1 (char 0)

Raw output:


### Cycle 11 — #20: 8. Juice (Game Feel)

**REQUEST_CHANGES** — The implementation does not meet any of the acceptance criteria for the juice/game feel issue. No jump animation, squash/stretch on landing, particles on enemy death, or screen shake on hit were implemented. The changes instead focus on level progression, enemy types, and gravity mechanics which are unrelated to this specific issue.

### Cycle 12 — #19: 7. Basic Art Upgrade

**REQUEST_CHANGES** — The implementation does not meet the acceptance criteria for the Basic Art Upgrade issue. The player and enemies remain placeholder colored rectangles, platforms are still drawn as green rectangles, and no tileset or background layers have been added. The code changes primarily add level progression and gravity mechanics rather than addressing the art requirements.

### Cycle 13 — #18: 6. Score / Progress Tracking

**REQUEST_CHANGES** — The implementation adds multiple levels, enemy types, and gravity mechanics, but fails to implement the core requirements of issue #18: score tracking, level timer, death counter, and UI display. None of these features are present in the code changes.

### Cycle 14 — #17: 5. Checkpoints

**REQUEST_CHANGES** — The implementation does not include checkpoint functionality as specified in the issue. There are no checkpoint objects, no player position saving, and respawning always occurs from the level start. The changes instead add multiple levels, gravity toggle, and new enemy types which appear to be for a different feature.

### Cycle 15 — #16: 4. Level System

**APPROVE** — The implementation successfully meets all acceptance criteria for the level system. A LevelManager class handles level progression, win conditions are implemented via goal collision detection, level restart on death works correctly, and the game loads the next level upon completion. The code includes 7 distinct levels with increasing difficulty and proper state management for game completion.

### Cycle 16 — #15: 3. Combat & Collision Improvements

**REQUEST_CHANGES** — The implementation successfully adds bounce effects and improves stomp detection with gravity-aware collision handling. However, it fails to implement damage cooldown (invincibility frames) and visual feedback (flash/red tint on hit) as required by the acceptance criteria.

### Cycle 17 — #14: 2. Enemy (Creeper) Behavior System

**REQUEST_CHANGES** — The implementation adds multiple enemy types (normal, fast, flying) with patrol behavior, but fails to implement edge detection to prevent enemies from falling off platforms. Additionally, the issue requested a jumping enemy type which is not implemented. The patrol bounds are hardcoded in level data rather than dynamically detected.

### Cycle 18 — #13: 1. Player Movement Polish

**APPROVE** — The implementation successfully meets all acceptance criteria for player movement polish. Acceleration/deceleration, variable jump height, coyote time, and jump buffering are all correctly implemented with appropriate constants and logic. The movement feels responsive and the code integrates cleanly with the existing architecture.

### Cycle 19 — #28: Implement effect system manager and random effect triggering on enemy kill

**REQUEST_CHANGES** — The implementation does not meet the acceptance criteria for issue #28. No EffectManager class was created, and none of the three required effects (platform movement, gravity change, enemy speed increase) were implemented. The changes instead focus on adding multiple levels, enemy types, and a gravity toggle feature, which are unrelated to the requested effect system.

### Cycle 20 — #29: Display active effects to player on HUD

**APPROVE** — The implementation successfully adds an effect system and displays active effects on the HUD with names, colors, and remaining duration. The HUD updates in real-time as effects are added or expire, meeting all acceptance criteria. The code is well-structured and extensible for future effects.

### Cycle 21 — #30: Remove player-initiated gravity toggle and integrate with effect system

**REQUEST_CHANGES** — The implementation fails to meet several acceptance criteria. The G key gravity toggle and gravity_toggle_cooldown are still present in the code. Gravity changes are not triggered by enemy kills through the effect system. The gravity system still uses a complete direction toggle rather than a slight reduction as specified.

### Cycle 22 — #31: Add jump animation for player

**APPROVE** — The implementation fully meets all acceptance criteria for the jump animation. The player sprite stretches vertically when jumping upward and compresses when falling, with smooth transitions between states. The animation correctly resets when landing, and the code handles edge cases like gravity reversal and death states appropriately.

### Cycle 23 — #32: Add squash/stretch animation on landing

**REQUEST_CHANGES** — The implementation adds a continuous squash/stretch animation based on velocity, but the issue requires a distinct animation triggered specifically on landing with a fixed duration (5-10 frames). The current animation is always active and lacks a clear landing trigger with the specified frame count.

### Cycle 24 — #33: Add particle effects on enemy death

**REQUEST_CHANGES** — The implementation adds a text-based effect system for HUD display but does not implement the particle effects required by the acceptance criteria. No particle spawning, physics, or rendering code was added for enemy death effects. The existing Effect/EffectManager classes are for text overlays, not particle systems.

### Cycle 25 — #34: Replace player placeholder with sprite

**REQUEST_CHANGES** — The implementation does not meet the acceptance criteria for replacing the player placeholder with a sprite. The player is still rendered as a red rectangle, and no sprite image loading code was added. All other player functionality remains intact, but the core requirement of loading and displaying a sprite image is missing.

### Cycle 26 — #35: Replace enemy placeholders with sprites

**APPROVE** — The implementation successfully replaces enemy placeholders with sprite images for all three enemy types (basic, fast, flying). Sprite loading includes fallback handling, dimensions match collision rects via image.get_rect(), and all existing patrol and collision functionality is preserved. The changes integrate cleanly with the existing level data and rendering system.

### Cycle 27 — #36: Add tileset and background layers

**APPROVE** — The implementation successfully meets all acceptance criteria. Tileset images are generated programmatically with grass, dirt, and platform tiles, and platform drawing has been replaced with tile-based rendering. A gradient background with parallax-scrolling cloud layers has been added. The changes are functional and integrate well with the existing codebase.

### Cycle 28 — #37: Implement score tracking for enemy kills

**REQUEST_CHANGES** — The score tracking system is completely missing from the implementation. No score variable exists in the Game class, no score increment occurs when enemies are stomped, score is not reset on game restart, and the score is not displayed in the UI. All four acceptance criteria are unmet.

### Cycle 29 — #38: Add level timer and death counter

**REQUEST_CHANGES** — The implementation does not meet the acceptance criteria for the level timer and death counter. No timer or death tracking logic was added to the game state, and the UI does not display these metrics. The changes only include existing code without the required new features.

### Cycle 30 — #39: Create UI display for score, timer, and deaths

**REQUEST_CHANGES** — The implementation does not meet the acceptance criteria for issue #39. The required UI elements for score, timer, and death count are not present in the renderer, and the underlying data (score, timer, death count) is not tracked in the game state. The current HUD only displays level number and active effects.

### Cycle 31 — #40: Implement checkpoint system as specified in issue #17

**REQUEST_CHANGES** — The checkpoint system implementation is completely missing from the code changes. None of the acceptance criteria are addressed: no checkpoint objects are added to level data, no checkpoint collision detection or position saving exists, respawning still uses the original level spawn point, and there's no checkpoint persistence logic. The code appears unchanged from the original architecture without any checkpoint functionality.
