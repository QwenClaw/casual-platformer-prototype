import pygame
from constants import SCREEN_W, SCREEN_H, SKY_BLUE


class BackgroundLayer:
    """Represents a single background layer with optional parallax scrolling."""
    
    def __init__(self, color, parallax_factor=1.0, y_offset=0):
        """Initialize a background layer.
        
        Args:
            color: RGB tuple for solid color, or pygame.Surface for image
            parallax_factor: Movement speed relative to camera (1.0 = same as foreground)
            y_offset: Vertical offset for the layer
        """
        self.parallax_factor = parallax_factor
        self.y_offset = y_offset
        
        if isinstance(color, tuple):
            # Create a solid color surface
            self.surface = pygame.Surface((SCREEN_W, SCREEN_H))
            self.surface.fill(color)
        else:
            # Assume it's a surface
            self.surface = color
    
    def draw(self, surface, camera_x=0):
        """Draw the background layer with parallax effect.
        
        Args:
            surface: Surface to draw on
            camera_x: Horizontal camera position for parallax calculation
        """
        # Calculate parallax offset
        offset_x = -camera_x * self.parallax_factor
        
        # Tile the background horizontally if needed
        if offset_x < 0:
            offset_x = offset_x % SCREEN_W
        
        # Draw the background (tiled if necessary)
        surface.blit(self.surface, (offset_x, self.y_offset))
        
        # Draw a second copy for seamless tiling
        if offset_x > 0:
            surface.blit(self.surface, (offset_x - SCREEN_W, self.y_offset))
        elif offset_x < 0 and offset_x + SCREEN_W < SCREEN_W:
            surface.blit(self.surface, (offset_x + SCREEN_W, self.y_offset))


class Background:
    """Manages multiple background layers with parallax scrolling."""
    
    def __init__(self):
        """Initialize the background with gradient and cloud layers."""
        self.layers = []
        self._create_gradient_background()
        self._create_cloud_layer()
    
    def _create_gradient_background(self):
        """Create a sky gradient background layer."""
        # Create gradient from light blue (top) to darker blue (bottom)
        gradient_surface = pygame.Surface((SCREEN_W, SCREEN_H))
        
        for y in range(SCREEN_H):
            # Calculate color for this row
            ratio = y / SCREEN_H
            r = int(135 * (1 - ratio) + 100 * ratio)
            g = int(206 * (1 - ratio) + 150 * ratio)
            b = int(235 * (1 - ratio) + 200 * ratio)
            pygame.draw.line(gradient_surface, (r, g, b), (0, y), (SCREEN_W, y))
        
        # Add gradient layer with no parallax (moves with camera)
        self.layers.append(BackgroundLayer(gradient_surface, parallax_factor=0.0))
    
    def _create_cloud_layer(self):
        """Create a simple cloud layer."""
        cloud_surface = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        
        # Draw some simple clouds
        cloud_color = (255, 255, 255, 150)  # Semi-transparent white
        
        # Cloud 1
        pygame.draw.ellipse(cloud_surface, cloud_color, (100, 50, 120, 40))
        pygame.draw.ellipse(cloud_surface, cloud_color, (140, 40, 80, 50))
        pygame.draw.ellipse(cloud_surface, cloud_color, (80, 60, 100, 30))
        
        # Cloud 2
        pygame.draw.ellipse(cloud_surface, cloud_color, (400, 80, 100, 35))
        pygame.draw.ellipse(cloud_surface, cloud_color, (430, 70, 70, 45))
        pygame.draw.ellipse(cloud_surface, cloud_color, (380, 90, 90, 30))
        
        # Cloud 3
        pygame.draw.ellipse(cloud_surface, cloud_color, (650, 60, 110, 40))
        pygame.draw.ellipse(cloud_surface, cloud_color, (680, 50, 80, 50))
        pygame.draw.ellipse(cloud_surface, cloud_color, (630, 70, 100, 30))
        
        # Add cloud layer with slow parallax (moves slower than foreground)
        self.layers.append(BackgroundLayer(cloud_surface, parallax_factor=0.2))
    
    def draw(self, surface, camera_x=0):
        """Draw all background layers.
        
        Args:
            surface: Surface to draw on
            camera_x: Horizontal camera position for parallax calculation
        """
        for layer in self.layers:
            layer.draw(surface, camera_x)