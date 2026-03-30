import pygame
from constants import SKY_BLUE, GREEN, SCREEN_W, SCREEN_H, BLACK, WHITE, YELLOW, DARK_GREEN


class Renderer:
    """Handles all rendering for the game."""

    def __init__(self, screen):
        """Initialize the renderer.

        Args:
            screen: pygame.Surface to draw on
        """
        self.screen = screen
        self.font_large = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 32)

    def draw(self, player, enemies, level, state, level_number, is_final_level, active_effects=None):
        """Draw the complete game frame.

        Args:
            player: Player sprite
            enemies: List/group of enemy sprites
            level: Level object with platforms and goal
            state: Current game state (PLAYING, LEVEL_COMPLETE, DEAD, or GAME_COMPLETE)
            level_number: Current level number (1-indexed)
            is_final_level: Whether this is the final level
            active_effects: List of active Effect objects (optional)
        """
        # Clear screen with sky color
        self.screen.fill(SKY_BLUE)

        # Draw platforms as colored rectangles
        for platform in level.platforms:
            pygame.draw.rect(self.screen, GREEN, platform)
            # Draw darker border
            pygame.draw.rect(self.screen, DARK_GREEN, platform, 2)

        # Draw goal as yellow rectangle
        pygame.draw.rect(self.screen, YELLOW, level.goal)
        pygame.draw.rect(self.screen, (200, 180, 0), level.goal, 2)

        # Draw enemy sprites
        for enemy in enemies:
            self.screen.blit(enemy.image, enemy.rect)

        # Draw player sprite
        self.screen.blit(player.image, player.rect)

        # Draw HUD
        self._draw_hud(level_number, active_effects or [])

        # Draw overlay text based on state
        if state == 1:  # LEVEL_COMPLETE
            self._draw_overlay("LEVEL COMPLETE!", (0, 255, 0), "Press R for next level")
        elif state == 2:  # DEAD
            self._draw_overlay("GAME OVER", (255, 0, 0), "Press R to restart")
        elif state == 3:  # GAME_COMPLETE
            self._draw_overlay("YOU WIN!", (255, 215, 0), "Press R to play again")

        pygame.display.flip()

    def _draw_hud(self, level_number, active_effects):
        """Draw the heads-up display.

        Args:
            level_number: Current level number
            active_effects: List of active Effect objects
        """
        # Draw level number
        level_text = self.font_small.render(f"Level {level_number}", True, BLACK)
        self.screen.blit(level_text, (10, 10))

        # Draw active effects
        y_offset = 40
        if active_effects:
            # Draw effects header
            effects_header = self.font_small.render("Effects:", True, BLACK)
            self.screen.blit(effects_header, (10, y_offset))
            y_offset += 25

            # Draw each active effect with its color
            for effect in active_effects:
                duration_text = effect.get_duration_text()
                effect_text = f"  {effect.name}{duration_text}"
                text_surface = self.font_small.render(effect_text, True, effect.color)
                self.screen.blit(text_surface, (10, y_offset))
                y_offset += 25
        else:
            # No active effects
            no_effects_text = self.font_small.render("No active effects", True, (128, 128, 128))
            self.screen.blit(no_effects_text, (10, y_offset))

    def _draw_overlay(self, text, color, subtitle):
        """Draw overlay text centered on screen.

        Args:
            text: Text string to display
            color: RGB color tuple for the text
            subtitle: Subtitle text
        """
        # Semi-transparent background
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Main text
        text_surface = self.font_large.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 20))
        self.screen.blit(text_surface, text_rect)

        # Subtitle
        sub_surface = self.font_small.render(subtitle, True, WHITE)
        sub_rect = sub_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 30))
        self.screen.blit(sub_surface, sub_rect)
