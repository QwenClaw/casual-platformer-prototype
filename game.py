import pygame
from constants import SCREEN_W, SCREEN_H, FPS, SKY_BLUE, GREEN
from player import Player
from level import Level
from collision import check_enemy_collision, check_goal_collision
from sound_manager import SoundManager


class Game:
    """Main game loop and state manager."""

    # Game states
    PLAYING = 0
    LEVEL_COMPLETE = 1
    DEAD = 2

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Casual Platformer Prototype")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game objects
        self.level = Level()
        self.player = Player(*self.level.spawn_point)
        self.enemies = self.level.enemies
        self.sound_manager = SoundManager()

        # Game state
        self.state = self.PLAYING

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
                    self.__init__()

    def update(self):
        """Update game state."""
        if self.state != self.PLAYING:
            return

        # Update player with current key states
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.level.platforms)

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

        # Check enemy collisions
        enemy_hit, is_stomp = check_enemy_collision(self.player, self.enemies)
        if enemy_hit:
            if is_stomp:
                enemy_hit.kill()
                self.player.bounce()
                self.sound_manager.play_stomp()
            else:
                self.player.die()
                self.state = self.DEAD
                return

        # Check goal collision
        if check_goal_collision(self.player, self.level.goal):
            self.state = self.LEVEL_COMPLETE
            self.sound_manager.play_win()

        # Check if player fell off screen
        if self.player.rect.top > SCREEN_H:
            self.player.die()
            self.state = self.DEAD

    def draw(self):
        """Render the frame."""
        # Clear screen with sky color
        self.screen.fill(SKY_BLUE)

        # Draw platforms
        for platform in self.level.platforms:
            pygame.draw.rect(self.screen, GREEN, platform)

        # Draw goal
        pygame.draw.rect(self.screen, (255, 215, 0), self.level.goal)

        # Draw enemies
        for enemy in self.enemies:
            self.screen.blit(enemy.image, enemy.rect)

        # Draw player
        self.screen.blit(self.player.image, self.player.rect)

        # Draw overlay text based on state
        if self.state == self.LEVEL_COMPLETE:
            self._draw_overlay("Level Complete! Press R to restart", (0, 255, 0))
        elif self.state == self.DEAD:
            self._draw_overlay("Game Over! Press R to restart", (255, 0, 0))

        pygame.display.flip()

    def _draw_overlay(self, text, color):
        """Draw overlay text on screen."""
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        self.screen.blit(text_surface, text_rect)
