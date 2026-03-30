import pygame
from constants import SKY_BLUE, GREEN, SCREEN_W, SCREEN_H


class Renderer:
    """Handles all rendering for the game."""

    def __init__(self, screen):
        """Initialize the renderer.

        Args:
            screen: pygame.Surface to draw on
        """
        self.screen = screen

    def draw(self, player, enemies, level, state):
        """Draw the complete game frame.

        Args:
            player: Player sprite
            enemies: List/group of enemy sprites
            level: Level object with platforms and goal
            state: Current game state (PLAYING, LEVEL_COMPLETE, or DEAD)
        """
        # Clear screen with sky color
        self.screen.fill(SKY_BLUE)

        # Draw platforms as colored rectangles
        for platform in level.platforms:
            pygame.draw.rect(self.screen, GREEN, platform)

        # Draw goal as yellow rectangle
        pygame.draw.rect(self.screen, (255, 215, 0), level.goal)

        # Draw enemy sprites
        for enemy in enemies:
            self.screen.blit(enemy.image, enemy.rect)

        # Draw player sprite
        self.screen.blit(player.image, player.rect)

        # Draw overlay text based on state
        if state == 1:  # LEVEL_COMPLETE
            self._draw_overlay("LEVEL COMPLETE!", (0, 255, 0))
        elif state == 2:  # DEAD
            self._draw_overlay("GAME OVER", (255, 0, 0))

        pygame.display.flip()

    def _draw_overlay(self, text, color):
        """Draw overlay text centered on screen.

        Args:
            text: Text string to display
            color: RGB color tuple for the text
        """
        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        self.screen.blit(text_surface, text_rect)
