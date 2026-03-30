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

    def update(self):
        """Move horizontally at ENEMY_SPEED; reverse at patrol bounds."""
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

    def update(self):
        """Move horizontally at FAST_ENEMY_SPEED; reverse at patrol bounds."""
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
