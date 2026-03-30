import pygame
from constants import TILE_SIZE, GREEN, DARK_GREEN, BROWN, GRAY, DARK_GRAY


class Tileset:
    """Generates and manages tile images for platform rendering."""
    
    def __init__(self):
        """Initialize the tileset by generating tile images."""
        self.ground_tile = self._create_ground_tile()
        self.platform_tile = self._create_platform_tile()
        self.grass_tile = self._create_grass_tile()
        self.dirt_tile = self._create_dirt_tile()
    
    def _create_ground_tile(self):
        """Create a ground tile with grass on top and dirt below.
        
        Returns:
            pygame.Surface: 32x32 tile with grass (top 16px) and dirt (bottom 16px)
        """
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        # Top half: grass (green with darker stripe at very top)
        pygame.draw.rect(tile, GREEN, (0, 0, TILE_SIZE, TILE_SIZE // 2))
        pygame.draw.rect(tile, DARK_GREEN, (0, 0, TILE_SIZE, 4))
        
        # Bottom half: dirt (brown)
        pygame.draw.rect(tile, BROWN, (0, TILE_SIZE // 2, TILE_SIZE, TILE_SIZE // 2))
        
        # Add some texture to dirt
        for i in range(0, TILE_SIZE, 8):
            for j in range(TILE_SIZE // 2, TILE_SIZE, 8):
                if (i + j) % 16 == 0:
                    pygame.draw.rect(tile, (120, 60, 15), (i, j, 2, 2))
        
        return tile
    
    def _create_platform_tile(self):
        """Create a platform tile for floating platforms.
        
        Returns:
            pygame.Surface: 32x32 tile with platform appearance
        """
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        
        # Main platform color (grayish brown)
        tile.fill((150, 120, 100))
        
        # Top edge highlight
        pygame.draw.rect(tile, (180, 150, 130), (0, 0, TILE_SIZE, 4))
        
        # Bottom edge shadow
        pygame.draw.rect(tile, (100, 80, 60), (0, TILE_SIZE - 4, TILE_SIZE, 4))
        
        # Side edges
        pygame.draw.rect(tile, (120, 90, 70), (0, 0, 4, TILE_SIZE))
        pygame.draw.rect(tile, (120, 90, 70), (TILE_SIZE - 4, 0, 4, TILE_SIZE))
        
        # Add some texture
        for i in range(4, TILE_SIZE - 4, 6):
            for j in range(4, TILE_SIZE - 4, 6):
                if (i + j) % 12 == 0:
                    pygame.draw.rect(tile, (130, 100, 80), (i, j, 2, 2))
        
        return tile
    
    def _create_grass_tile(self):
        """Create a pure grass tile for top of ground platforms.
        
        Returns:
            pygame.Surface: 32x32 grass tile
        """
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile.fill(GREEN)
        
        # Add grass texture
        for i in range(0, TILE_SIZE, 4):
            height = 8 + (i % 5) * 2
            pygame.draw.rect(tile, DARK_GREEN, (i, 0, 2, height))
        
        return tile
    
    def _create_dirt_tile(self):
        """Create a pure dirt tile for below grass.
        
        Returns:
            pygame.Surface: 32x32 dirt tile
        """
        tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile.fill(BROWN)
        
        # Add dirt texture
        for i in range(0, TILE_SIZE, 6):
            for j in range(0, TILE_SIZE, 6):
                if (i + j) % 12 == 0:
                    pygame.draw.rect(tile, (120, 60, 15), (i, j, 3, 3))
        
        return tile
    
    def get_tile_for_platform(self, platform_rect, screen_height):
        """Determine which tile to use for a platform based on its position.
        
        Args:
            platform_rect: pygame.Rect of the platform
            screen_height: Height of the screen (to detect ground platforms)
            
        Returns:
            pygame.Surface: The appropriate tile image
        """
        # Ground platforms are at the bottom of the screen
        if platform_rect.y == screen_height - TILE_SIZE:
            return self.ground_tile
        else:
            return self.platform_tile
    
    def draw_platform(self, surface, platform_rect, screen_height):
        """Draw a platform using tiles.
        
        Args:
            surface: Surface to draw on
            platform_rect: pygame.Rect of the platform
            screen_height: Height of the screen
        """
        tile = self.get_tile_for_platform(platform_rect, screen_height)
        
        # Calculate how many tiles we need
        tiles_x = platform_rect.width // TILE_SIZE
        tiles_y = platform_rect.height // TILE_SIZE
        
        # Draw tiles to cover the platform
        for x in range(tiles_x):
            for y in range(tiles_y):
                pos_x = platform_rect.x + x * TILE_SIZE
                pos_y = platform_rect.y + y * TILE_SIZE
                surface.blit(tile, (pos_x, pos_y))
        
        # Handle partial tiles at edges (if platform size isn't exact multiple of TILE_SIZE)
        if platform_rect.width % TILE_SIZE != 0 or platform_rect.height % TILE_SIZE != 0:
            # For simplicity, we'll just draw the platform as a colored rectangle
            # with a tile pattern overlay
            tile_surface = pygame.Surface((platform_rect.width, platform_rect.height), pygame.SRCALPHA)
            
            # Draw tiles onto the temporary surface
            for x in range(tiles_x):
                for y in range(tiles_y):
                    tile_surface.blit(tile, (x * TILE_SIZE, y * TILE_SIZE))
            
            # Draw any partial tiles
            if platform_rect.width % TILE_SIZE != 0:
                partial_width = platform_rect.width % TILE_SIZE
                for y in range(tiles_y):
                    # Create a subsurface for the partial tile
                    partial_tile = tile.subsurface((0, 0, partial_width, TILE_SIZE))
                    tile_surface.blit(partial_tile, (tiles_x * TILE_SIZE, y * TILE_SIZE))
            
            if platform_rect.height % TILE_SIZE != 0:
                partial_height = platform_rect.height % TILE_SIZE
                for x in range(tiles_x):
                    partial_tile = tile.subsurface((0, 0, TILE_SIZE, partial_height))
                    tile_surface.blit(partial_tile, (x * TILE_SIZE, tiles_y * TILE_SIZE))
            
            # Draw the composed tile surface
            surface.blit(tile_surface, platform_rect.topleft)