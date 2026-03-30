import pygame
from constants import (
    PLAYER_SPEED,
    JUMP_FORCE,
    GRAVITY,
    MAX_FALL_SPEED,
    RED,
    SCREEN_W,
)
from collision import resolve_platform_collisions


class Player(pygame.sprite.Sprite):
    """Player character with physics and collision handling."""

    # Movement tuning
    ACCELERATION = 0.8
    DECELERATION = 0.8
    BOUNCE_FORCE = -10

    def __init__(self, x, y):
        super().__init__()

        # Create player surface (32x48 rectangle)
        self.image = pygame.Surface((32, 48))
        self.image.fill(RED)

        # Set up rect and position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Physics
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.alive = True

    def update(self, keys, platforms):
        """Update player state based on input and collisions.

        Args:
            keys: Dictionary of key states from pygame.key.get_pressed()
            platforms: List of pygame.Rect representing collision surfaces
        """
        if not self.alive:
            return

        # Handle horizontal input
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity.x -= self.ACCELERATION
            if self.velocity.x < -PLAYER_SPEED:
                self.velocity.x = -PLAYER_SPEED
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity.x += self.ACCELERATION
            if self.velocity.x > PLAYER_SPEED:
                self.velocity.x = PLAYER_SPEED
            moving = True

        # Apply deceleration when no horizontal input
        if not moving:
            if self.velocity.x > 0:
                self.velocity.x -= self.DECELERATION
                if self.velocity.x < 0:
                    self.velocity.x = 0
            elif self.velocity.x < 0:
                self.velocity.x += self.DECELERATION
                if self.velocity.x > 0:
                    self.velocity.x = 0

        # Handle jump input
        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        ) and self.on_ground:
            self.velocity.y = JUMP_FORCE
            self.on_ground = False

        # Apply gravity
        self.velocity.y += GRAVITY
        if self.velocity.y > MAX_FALL_SPEED:
            self.velocity.y = MAX_FALL_SPEED

        # Resolve collisions using collision module
        self.on_ground = resolve_platform_collisions(self, platforms)

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity.x = 0
        if self.rect.right > SCREEN_W:
            self.rect.right = SCREEN_W
            self.velocity.x = 0

    def die(self):
        """Set player as dead."""
        self.alive = False

    def bounce(self):
        """Apply small upward velocity impulse after stomping enemy."""
        self.velocity.y = self.BOUNCE_FORCE
