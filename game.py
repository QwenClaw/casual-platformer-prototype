import pygame
from constants import SCREEN_W, SCREEN_H, FPS, STATE_PLAYING, STATE_LEVEL_COMPLETE, STATE_DEAD, STATE_GAME_COMPLETE, STATE_MAIN_MENU
from player import Player
from level import LevelManager
from collision import check_enemy_collision, check_goal_collision
from sound_manager import SoundManager
from renderer import Renderer
from effects import Effect, EffectManager


class Game:
    """Main game loop and state manager."""

    # Game states (mapped to constants for backward compatibility)
    PLAYING = STATE_PLAYING
    LEVEL_COMPLETE = STATE_LEVEL_COMPLETE
    DEAD = STATE_DEAD
    GAME_COMPLETE = STATE_GAME_COMPLETE
    MAIN_MENU = STATE_MAIN_MENU

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Casual Platformer Prototype")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game objects
        self.level_manager = LevelManager()
        level = self.level_manager.get_current_level()
        self.player = Player(*level.spawn_point)
        self.enemies = level.enemies
        self.sound_manager = SoundManager()
        self.renderer = Renderer(self.screen)

        # Effect manager for tracking active effects
        self.effect_manager = EffectManager()

        # Game state - start in main menu
        self.state = self.MAIN_MENU

        # Track previous on_ground state for jump detection
        self.prev_on_ground = True

        # Gravity toggle cooldown
        self.gravity_toggle_cooldown = 0

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.state == self.MAIN_MENU:
                    # Start game from main menu
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self._start_game()
                elif event.key == pygame.K_r and self.state != self.PLAYING and self.state != self.MAIN_MENU:
                    # Reset game
                    self.reset()
                elif event.key == pygame.K_g and self.state == self.PLAYING:
                    # Toggle gravity
                    if self.gravity_toggle_cooldown <= 0:
                        self.player.toggle_gravity()
                        self.sound_manager.play_gravity_toggle()
                        self.gravity_toggle_cooldown = 30  # Half second cooldown
                        # Update gravity effect
                        self._update_gravity_effect()

    def _start_game(self):
        """Start the game from main menu."""
        # Reset to first level
        self.level_manager.reset()
        level = self.level_manager.get_current_level()
        self.player = Player(*level.spawn_point)
        self.enemies = level.enemies
        self.effect_manager.clear()
        self.state = self.PLAYING
        self.prev_on_ground = True
        self.gravity_toggle_cooldown = 0

    def _update_gravity_effect(self):
        """Update the gravity effect based on current gravity direction."""
        if self.player.gravity_direction < 0:
            # Gravity is reversed - add effect
            self.effect_manager.add_effect(
                Effect("Gravity Reversed", (255, 100, 0), duration=None)
            )
        else:
            # Gravity is normal - remove effect
            self.effect_manager.remove_effect("Gravity Reversed")

    def update(self):
        """Update game state."""
        # Update gravity toggle cooldown
        if self.gravity_toggle_cooldown > 0:
            self.gravity_toggle_cooldown -= 1

        if self.state != self.PLAYING:
            return

        # Update effects
        self.effect_manager.update()

        # Store previous on_ground state before update
        self.prev_on_ground = self.player.on_ground

        # Update player with current key states
        keys = pygame.key.get_pressed()
        level = self.level_manager.get_current_level()
        jumped = self.player.update(keys, level.platforms)

        # Play jump sound if a jump occurred
        if jumped:
            self.sound_manager.play_jump()

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

        # Check enemy collisions - handle multiple collisions
        collisions = check_enemy_collision(self.player, self.enemies)
        if collisions:
            # Process stomps first
            stomped = False
            for enemy, is_stomp in collisions:
                if is_stomp:
                    if enemy in self.enemies:
                        enemy.kill()
                        self.enemies.remove(enemy)
                        stomped = True

            if stomped:
                # Bounce once after stomping any enemies
                self.player.bounce()
                self.sound_manager.play_stomp()
            else:
                # All collisions were non-stomp hits - player dies
                # But only if no stomp happened
                has_non_stomp = any(not is_stomp for _, is_stomp in collisions)
                if has_non_stomp:
                    self.player.die()
                    self.state = self.DEAD
                    self.sound_manager.play_death()
                    return

        # Check goal collision
        if check_goal_collision(self.player, level.goal):
            if self.level_manager.is_final_level():
                self.state = self.GAME_COMPLETE
                self.sound_manager.play_win()
            else:
                self.state = self.LEVEL_COMPLETE
                self.sound_manager.play_win()

        # Check if player fell off screen (depends on gravity direction)
        if self.player.gravity_direction > 0 and self.player.rect.top > SCREEN_H:
            self.player.die()
            self.state = self.DEAD
            self.sound_manager.play_death()
        elif self.player.gravity_direction < 0 and self.player.rect.bottom < 0:
            self.player.die()
            self.state = self.DEAD
            self.sound_manager.play_death()

    def draw(self):
        """Render the frame using the renderer."""
        if self.state == self.MAIN_MENU:
            # Draw main menu
            self.renderer.draw_main_menu()
        else:
            # Draw game
            level = self.level_manager.get_current_level()
            self.renderer.draw(
                self.player,
                self.enemies,
                level,
                self.state,
                self.level_manager.get_level_number(),
                self.level_manager.is_final_level(),
                self.effect_manager.get_active_effects()
            )

    def reset(self):
        """Reset the game to initial state."""
        if self.state == self.LEVEL_COMPLETE:
            # Advance to next level
            if not self.level_manager.next_level():
                # Shouldn't happen, but handle gracefully
                self.level_manager.reset()
        elif self.state == self.GAME_COMPLETE:
            # Reset entire game
            self.level_manager.reset()
        else:
            # Restart current level (DEAD state)
            self.level_manager.restart_level()

        # Reset player
        level = self.level_manager.get_current_level()
        self.player = Player(*level.spawn_point)
        self.enemies = level.enemies

        # Reset effects
        self.effect_manager.clear()

        # Reset state
        self.state = self.PLAYING
        self.prev_on_ground = True
        self.gravity_toggle_cooldown = 0