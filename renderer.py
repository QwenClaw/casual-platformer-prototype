import pygame
from constants import SKY_BLUE, GREEN, SCREEN_W, SCREEN_H, BLACK, WHITE, YELLOW, DARK_GREEN, TILE_SIZE, STATE_MAIN_MENU
from tileset import Tileset
from background import Background


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
        
        # Initialize tileset for platform rendering
        self.tileset = Tileset()
        
        # Initialize background with parallax layers
        self.background = Background()
        
        # Camera position for parallax scrolling
        self.camera_x = 0

    def draw_main_menu(self):
        """Draw the main menu screen."""
        # Draw background with fixed camera position
        self.background.draw(self.screen, 0)
        
        # Semi-transparent overlay for better text visibility
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = self.font_large.render("Casual Platformer Prototype", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
        self.screen.blit(title_text, title_rect)
        
        # Draw start instruction
        start_text = self.font_small.render("Press ENTER or SPACE to Start", True, YELLOW)
        start_rect = start_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        self.screen.blit(start_text, start_rect)
        
        # Draw controls hint
        controls_text = self.font_small.render("Controls: Arrow keys/WASD to move, SPACE to jump", True, WHITE)
        controls_rect = controls_text.get_rect(center=(SCREEN_W // 2, SCREEN_H * 2 // 3))
        self.screen.blit(controls_text, controls_rect)
        
        # Draw gravity toggle hint
        gravity_text = self.font_small.render("Press G to toggle gravity", True, (200, 200, 255))
        gravity_rect = gravity_text.get_rect(center=(SCREEN_W // 2, SCREEN_H * 2 // 3 + 40))
        self.screen.blit(gravity_text, gravity_rect)
        
        pygame.display.flip()

    def draw(self, player, enemies, level, state, level_number, is_final_level, active_effects=None, timer=0.0):
        """Draw the complete game frame.

        Args:
            player: Player sprite
            enemies: List/group of enemy sprites
            level: Level object with platforms and goal
            state: Current game state (PLAYING, LEVEL_COMPLETE, DEAD, or GAME_COMPLETE)
            level_number: Current level number (1-indexed)
            is_final_level: Whether this is the final level
            active_effects: List of active Effect objects (optional)
            timer: Elapsed time in seconds for the current level
        """
        # Update camera position based on player position (simple follow camera)
        # Keep player roughly in the left third of the screen
        target_camera_x = player.rect.x - SCREEN_W // 3
        # Smooth camera movement
        self.camera_x += (target_camera_x - self.camera_x) * 0.1
        
        # Clamp camera to level bounds
        level_width = level.width
        max_camera_x = max(0, level_width - SCREEN_W)
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
        
        # Draw background with parallax effect
        self.background.draw(self.screen, self.camera_x)

        # Draw platforms using tileset
        for platform in level.platforms:
            # Adjust platform position for camera
            adjusted_rect = platform.move(-int(self.camera_x), 0)
            
            # Only draw if on screen
            if -TILE_SIZE < adjusted_rect.right and adjusted_rect.left < SCREEN_W:
                self.tileset.draw_platform(self.screen, adjusted_rect, SCREEN_H)

        # Draw goal as yellow rectangle (adjusted for camera)
        goal_adjusted = level.goal.move(-int(self.camera_x), 0)
        pygame.draw.rect(self.screen, YELLOW, goal_adjusted)
        pygame.draw.rect(self.screen, (200, 180, 0), goal_adjusted, 2)

        # Draw enemy sprites (adjusted for camera)
        for enemy in enemies:
            enemy_adjusted_rect = enemy.rect.move(-int(self.camera_x), 0)
            self.screen.blit(enemy.image, enemy_adjusted_rect)

        # Draw player sprite (adjusted for camera)
        player_adjusted_rect = player.rect.move(-int(self.camera_x), 0)
        self.screen.blit(player.image, player_adjusted_rect)

        # Draw HUD
        self._draw_hud(level_number, active_effects or [], timer)

        # Draw overlay text based on state
        if state == 1:  # LEVEL_COMPLETE
            self._draw_overlay("LEVEL COMPLETE!", (0, 255, 0), "Press R to restart current level | Press N for next level")
        elif state == 2:  # DEAD
            self._draw_overlay("GAME OVER", (255, 0, 0), "Press [R] to restart current level", YELLOW)
        elif state == 3:  # GAME_COMPLETE
            self._draw_overlay("YOU WIN!", (255, 215, 0), "Press R to play again")

        pygame.display.flip()

    def _draw_hud(self, level_number, active_effects, timer):
        """Draw the heads-up display.

        Args:
            level_number: Current level number
            active_effects: List of active Effect objects
            timer: Elapsed time in seconds for the current level
        """
        # Draw level number
        level_text = self.font_small.render(f"Level {level_number}", True, BLACK)
        self.screen.blit(level_text, (10, 10))
        
        # Draw timer at top-right
        timer_text = self.font_small.render(f"Time: {timer:.2f}s", True, BLACK)
        timer_rect = timer_text.get_rect()
        timer_rect.topright = (SCREEN_W - 10, 10)
        self.screen.blit(timer_text, timer_rect)
        
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

    def _draw_overlay(self, text, color, subtitle, subtitle_color=WHITE):
        """Draw overlay text centered on screen.

        Args:
            text: Text string to display
            color: RGB color tuple for the text
            subtitle: Subtitle text
            subtitle_color: RGB color tuple for the subtitle text (default: WHITE)
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
        subtitle_surface = self.font_small.render(subtitle, True, subtitle_color)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 30))
        self.screen.blit(subtitle_surface, subtitle_rect)
