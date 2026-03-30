import pygame
from constants import SCREEN_W, SCREEN_H, FPS
from player import Player
from level import LevelManager
from collision import check_enemy_collision, check_goal_collision
from sound_manager import SoundManager
from renderer import Renderer


class Game:
    """Main game loop and state manager."""

    # Game states
    PLAYING = 0
    LEVEL_COMPLETE = 1
    DEAD = 2
    GAME_COMPLETE = 3

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

        # Game state
        self.state = self.PLAYING

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
                if event.key == pygame.K_r and self.state != self.PLAYING:
                    # Reset game
                    self.reset()
                elif event.key == pygame.K_g and self.state == self.PLAYING:
                    # Toggle gravity
                    if self.gravity_toggle_cooldown <= 0:
                        self.player.toggle_gravity()
                        self.sound_manager.play_gravity_toggle()
                        self.gravity_toggle_cooldown = 30  # Half second cooldown

    def update(self):
        """Update game state."""
        # Update gravity toggle cooldown
        if self.gravity_toggle_cooldown > 0:
            self.gravity_toggle_cooldown -= 1

        if self.state != self.PLAYING:
            return

        # Store previous on_ground state before update
        self.prev_on_ground = self.player.on_ground

        # Update player with current key states
        keys = pygame.key.get_pressed()
        level = self.level_manager.get_current_level()
        self.player.update(keys, level.platforms)

        # Detect jump: player was on ground, now is not
        if self.prev_on_ground and not self.player.on_ground:
            if (self.player.gravity_direction > 0 and self.player.velocity.y < 0) or \
               (self.player.gravity_direction < 0 and self.player.velocity.y > 0):
                self.sound_manager.play_jump()

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

        # Check enemy collisions
        enemy_hit, is_stomp = check_enemy_collision(self.player, self.enemies)
        if enemy_hit:
            if is_stomp:
                enemy_hit.kill()
                self.enemies.remove(enemy_hit)
                self.player.bounce()
                self.sound_manager.play_stomp()
            else:
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
        level = self.level_manager.get_current_level()
        self.renderer.draw(
            self.player,
            self.enemies,
            level,
            self.state,
            self.level_manager.get_level_number(),
            self.level_manager.is_final_level()
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

        # Reset state
        self.state = self.PLAYING
        self.prev_on_ground = True
        self.gravity_toggle_cooldown = 0
