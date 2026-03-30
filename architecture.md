# Casual Platformer Prototype — Technical Architecture

## Tech Stack
**Python 3 + Pygame** — Pygame is the most straightforward library for a 2D sprite-based platformer in Python. It provides hardware-accelerated rendering, collision primitives (`pygame.sprite`), built-in audio mixing, and a tight game-loop model. No external dependencies beyond Pygame are needed, keeping the prototype zero-friction to run.

## Component Design

### 1. Entry Point (`main.py`)
- Instantiates `Game`, calls `game.run()`. Single responsibility: bootstrap.

### 2. Game Loop (`game.py` — `Game` class)
- Owns the `pygame.display`, clock, and all sprite groups.
- `run()` → standard loop: `handle_events → update → draw → flip`.
- Manages three states: `PLAYING`, `LEVEL_COMPLETE`, `DEAD` (reset).
- Holds references to `Player`, enemy group, `Level`, `SoundManager`.

### 3. Player (`player.py` — `Player` class, extends `pygame.sprite.Sprite`)
- Horizontal acceleration/deceleration with a speed cap; gravity + jump impulse.
- `update(keys, platforms)` — reads input, applies physics, resolves Y-axis collisions with platforms, resolves X-axis collisions.
- Exposes `rect`, `velocity`, `on_ground` flag.
- `die()` → triggers state change; `win()` → triggers LEVEL_COMPLETE.

### 4. Enemy (`enemy.py` — `Enemy` class, extends `pygame.sprite.Sprite`)
- Patrols between two x-coordinates, reversing direction at endpoints.
- `update()` — moves horizontally, flips at bounds.
- On collision: if player is falling (`velocity.y > 0`) and above enemy midpoint → `kill()` enemy + bounce player; else → player `die()`.

### 5. Level Data (`level.py` — `Level` class)
- Stores platform rects, enemy spawn data, player spawn, and goal rect as plain data.
- `load()` builds the single hardcoded level: ground segments, floating platforms, gaps, enemy placements, goal position.
- Provides `platforms` (list of `pygame.Rect`), `enemies` (list of `Enemy`), `goal` (`pygame.Rect`), `spawn_point`.

### 6. Rendering (`renderer.py` — `Renderer` class)
- `draw(screen, player, enemies, level, state)` — clears screen, draws platforms (colored rects), player, enemies, goal marker, and overlay text for LEVEL_COMPLETE / DEAD.
- Keeps all `pygame.draw` / `blit` calls out of game logic.

### 7. Collision Manager (`collision.py`)
- `resolve_platform_collisions(sprite, platforms)` — axis-separated collision response (move-and-slide). Returns corrected position.
- `check_enemy_collision(player, enemies)` → returns hit enemy or `None`, and whether it was a stomp.
- `check_goal_collision(player, goal_rect)` → bool.
- Pure functions, no state.

### 8. Sound Manager (`sound_manager.py` — `SoundManager` class)
- Loads placeholder `.wav` files (or generates simple tones via `pygame.mixer.Sound` with raw samples if files are absent).
- `play_jump()`, `play_stomp()`, `play_win()`.
- Graceful fallback: if audio device unavailable, calls are no-ops.

### 9. Constants (`constants.py`)
- All magic numbers: `SCREEN_W`, `SCREEN_H`, `FPS`, `GRAVITY`, `PLAYER_SPEED`, `JUMP_FORCE`, `TILE_SIZE`, color tuples, etc.

## Data Flow
```
Keyboard Input
    → Game.handle_events() → stores key state
    → Player.update(keys, platforms)
        → apply acceleration / gravity
        → collision.resolve_platform_collisions() → corrected rect
    → collision.check_enemy_collision(player, enemies)
        → stomp? → enemy.kill(), player bounce, SoundManager.play_stomp()
        → hit?   → player.die(), Game.state = DEAD
    → collision.check_goal_collision(player, goal)
        → true  → Game.state = LEVEL_COMPLETE, SoundManager.play_win()
    → Renderer.draw(screen, ...) → pygame.display.flip()
```

## Key Design Decisions
- **Axis-separated collision resolution**: Resolve X and Y independently to avoid tunneling and give correct "land on platform" behavior without a physics engine.
- **Hardcoded single level in code**: No file parsing needed for a prototype; level data is just a method that appends rects. Easy to replace with Tiled JSON later.
- **Stomp detection via vertical position**: If the player's bottom is above the enemy's vertical midpoint at collision time, it counts as a stomp — simple and matches classic platformer feel.
- **State machine for game states (PLAYING / DEAD / LEVEL_COMPLETE)**: Keeps the game loop clean; each state has distinct update/draw behavior without tangled conditionals.
- **Generated fallback sounds**: `pygame.mixer.Sound(buffer=...)` can synthesize simple beeps from raw byte arrays, so the game runs with audio even without asset files.