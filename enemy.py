import pygame
from constants import ENEMY_SPEED, GRAY, TILE_SIZE


class Enemy(pygame.sprite.Sprite):
    """Enemy that patrols back and forth between two x-coordinates."""

    def __init__(self, x, y, patrol_left, patrol_right):
        super().__init__()

        # Create enemy surface (32x32 rectangle)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GRAY)

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
