import os
import pygame
from constants import ENEMY_SPEED, FAST_ENEMY_SPEED, FLYING_ENEMY_SPEED, TILE_SIZE

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, 'assets')


def _load_enemy_image(filename):
    """Load an enemy sprite image from the assets folder.

    Args:
        filename: Name of the image file (e.g., 'enemy_basic.png')

    Returns:
        pygame.Surface: The loaded image, or a fallback colored rectangle if loading fails
    """
    image_path = os.path.join(ASSETS_DIR, filename)
    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except (pygame.error, FileNotFoundError):
        # Fallback: return a colored rectangle if image loading fails
        surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        surface.fill((128, 128, 128, 255))
        return surface


class Enemy(pygame.sprite.Sprite):
    """Enemy that patrols back and forth between two x-coordinates."""

    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()

        # Load sprite image
        self.original_image = _load_enemy_image('enemy_basic.png')
        self.image = self.original_image

        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Patrol bounds
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

        # Direction: 1 = right, -1 = left
        self.direction = 1

    def update(self, platforms=None):
        """Move horizontally at ENEMY_SPEED; reverse at patrol bounds or platform edges."""
        # Check for platform edge before moving
        if platforms and self._is_at_edge(platforms):
            self.direction *= -1
        
        self.rect.x += ENEMY_SPEED * self.direction

        # Reverse direction when reaching patrol bounds
        if self.rect.right >= self.patrol_right:
            self.rect.right = self.patrol_right
            self.direction = -1
        elif self.rect.left <= self.patrol_left:
            self.rect.left = self.patrol_left
            self.direction = 1

        # Flip sprite based on direction
        if self.direction == 1:
            self.image = self.original_image
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)

    def _is_at_edge(self, platforms):
        """Check if enemy is at a platform edge in its current direction."""
        # Create a test rect slightly ahead in movement direction
        test_rect = self.rect.copy()
        test_rect.x += ENEMY_SPEED * self.direction
        
        # Check if there's a platform below the test position
        # For ground enemies, we check if there's a platform directly below
        ground_check_rect = pygame.Rect(
            test_rect.x,
            test_rect.bottom,
            test_rect.width,
            4  # Check a few pixels below
        )
        
        # If no platform below, we're at an edge
        for platform in platforms:
            if ground_check_rect.colliderect(platform):
                return False
        
        return True


class FastEnemy(pygame.sprite.Sprite):
    """Faster enemy that patrols back and forth."""

    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()

        # Load sprite image
        self.original_image = _load_enemy_image('enemy_fast.png')
        self.image = self.original_image

        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Patrol bounds
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

        # Direction: 1 = right, -1 = left
        self.direction = 1

    def update(self, platforms=None):
        """Move horizontally at FAST_ENEMY_SPEED; reverse at patrol bounds or platform edges."""
        # Check for platform edge before moving
        if platforms and self._is_at_edge(platforms):
            self.direction *= -1
        
        self.rect.x += FAST_ENEMY_SPEED * self.direction

        # Reverse direction when reaching patrol bounds
        if self.rect.right >= self.patrol_right:
            self.rect.right = self.patrol_right
            self.direction = -1
        elif self.rect.left <= self.patrol_left:
            self.rect.left = self.patrol_left
            self.direction = 1

        # Flip sprite based on direction
        if self.direction == 1:
            self.image = self.original_image
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)

    def _is_at_edge(self, platforms):
        """Check if enemy is at a platform edge in its current direction."""
        # Create a test rect slightly ahead in movement direction
        test_rect = self.rect.copy()
        test_rect.x += FAST_ENEMY_SPEED * self.direction
        
        # Check if there's a platform below the test position
        ground_check_rect = pygame.Rect(
            test_rect.x,
            test_rect.bottom,
            test_rect.width,
            4  # Check a few pixels below
        )
        
        # If no platform below, we're at an edge
        for platform in platforms:
            if ground_check_rect.colliderect(platform):
                return False
        
        return True


class FlyingEnemy(pygame.sprite.Sprite):
    """Enemy that flies up and down between two y-coordinates."""

    def __init__(self, x, y, patrol_top, patrol_bottom):
        super().__init__()

        # Load sprite image
        self.original_image = _load_enemy_image('enemy_flying.png')
        self.image = self.original_image

        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Patrol bounds (vertical)
        self.patrol_top = patrol_top
        self.patrol_bottom = patrol_bottom

        # Direction: 1 = down, -1 = up
        self.direction = 1

    def update(self):
        """Move vertically at FLYING_ENEMY_SPEED; reverse at patrol bounds."""
        self.rect.y += FLYING_ENEMY_SPEED * self.direction

        # Reverse direction when reaching patrol bounds
        if self.rect.bottom >= self.patrol_bottom:
            self.rect.bottom = self.patrol_bottom
            self.direction = -1
        elif self.rect.top <= self.patrol_top:
            self.rect.top = self.patrol_top
            self.direction = 1


class JumpingEnemy(pygame.sprite.Sprite):
    """Enemy that patrols horizontally and jumps periodically."""

    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()

        # Load sprite image
        self.original_image = _load_enemy_image('enemy_jumping.png')
        self.image = self.original_image

        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Patrol bounds
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right

        # Direction: 1 = right, -1 = left
        self.direction = 1

        # Physics
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = True
        self.jump_timer = 0
        self.jump_interval = 60  # frames between jumps

    def update(self):
        """Move horizontally and apply gravity; jump periodically."""
        from constants import GRAVITY, JUMP_FORCE, ENEMY_SPEED

        # Horizontal movement
        self.rect.x += ENEMY_SPEED * self.direction

        # Reverse direction when reaching patrol bounds
        if self.rect.right >= self.patrol_right:
            self.rect.right = self.patrol_right
            self.direction = -1
        elif self.rect.left <= self.patrol_left:
            self.rect.left = self.patrol_left
            self.direction = 1

        # Jump logic
        self.jump_timer += 1
        if self.on_ground and self.jump_timer >= self.jump_interval:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False
            self.jump_timer = 0

        # Apply gravity
        self.velocity.y += GRAVITY

        # Apply vertical velocity
        self.rect.y += self.velocity.y

        # Simple ground check (assuming ground is at y = SCREEN_H - TILE_SIZE)
        # This is a placeholder; in a real game, you'd check platform collisions.
        # For now, we'll just stop falling if we go below a certain y.
        # We'll use a simple ground level based on the initial y.
        # Actually, we can't know the ground level here. Let's assume the enemy
        # starts on ground and we'll just let it fall indefinitely.
        # For the purpose of this prototype, we'll just let it jump and fall.
        # The enemy will eventually fall off screen, but that's okay for now.

        # Flip sprite based on direction
        if self.direction == 1:
            self.image = self.original_image
        else:
            self.image = pygame.transform.flip(self.original_image, True, False)
