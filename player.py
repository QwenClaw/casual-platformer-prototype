import pygame
from constants import (
    PLAYER_SPEED,
    JUMP_FORCE,
    GRAVITY,
    MAX_FALL_SPEED,
    RED,
    SCREEN_W,
    SCREEN_H,
)
from collision import resolve_platform_collisions


class Player(pygame.sprite.Sprite):
    """Player character with physics and collision handling."""

    # Movement tuning
    ACCELERATION = 0.8
    DECELERATION = 0.8
    BOUNCE_FORCE = -10

    # Coyote time: frames after leaving ground where jump is still allowed
    COYOTE_TIME = 6
    # Jump buffer: frames before landing where jump input is remembered
    JUMP_BUFFER = 8
    # Jump cutoff: multiplier applied when jump button released early (variable jump height)
    JUMP_CUTOFF = 0.4

    # Animation constants
    STRETCH_MAX = 1.25  # Maximum stretch factor when jumping up
    COMPRESS_MIN = 0.75  # Minimum compression factor when falling
    ANIMATION_SMOOTHING = 0.15  # How quickly animation transitions

    def __init__(self, x, y):
        super().__init__()

        # Original dimensions
        self.original_width = 32
        self.original_height = 48

        # Create player surface (32x48 rectangle)
        self.image = pygame.Surface((self.original_width, self.original_height))
        self.image.fill(RED)

        # Collision rect (fixed size for physics)
        self.collision_rect = pygame.Rect(x, y, self.original_width, self.original_height)

        # Draw rect (changes with animation)
        self.rect = self.collision_rect.copy()

        # Physics
        self.velocity = pygame.math.Vector2(0, 0)
        self.on_ground = False
        self.alive = True

        # Gravity direction: 1 = normal (down), -1 = reversed (up)
        self.gravity_direction = 1

        # Coyote time tracking
        self.coyote_timer = 0
        self.was_on_ground = False

        # Jump buffer tracking
        self.jump_buffer_timer = 0

        # Variable jump height tracking
        self.is_jumping = False

        # Animation state
        self.stretch_factor = 1.0  # Current stretch (1.0 = normal)
        self.target_stretch = 1.0  # Target stretch to interpolate toward

    def update(self, keys, platforms, level_width=SCREEN_W):
        """Update player state based on input and collisions.

        Args:
            keys: Dictionary of key states from pygame.key.get_pressed()
            platforms: List of pygame.Rect representing collision surfaces
            level_width: Width of the current level in pixels (default: SCREEN_W)

        Returns:
            bool: True if a jump occurred this frame
        """
        if not self.alive:
            return False

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

        # Update coyote time
        if self.on_ground:
            self.coyote_timer = self.COYOTE_TIME
            self.is_jumping = False
        elif self.coyote_timer > 0:
            self.coyote_timer -= 1

        # Handle jump input with buffering
        jump_pressed = (
            keys[pygame.K_SPACE]
            or keys[pygame.K_UP]
            or keys[pygame.K_w]
        )

        # Track jump buffer
        if jump_pressed:
            self.jump_buffer_timer = self.JUMP_BUFFER
        elif self.jump_buffer_timer > 0:
            self.jump_buffer_timer -= 1

        # Execute jump if buffered and within coyote time
        jump_occurred = False
        if self.jump_buffer_timer > 0 and self.coyote_timer > 0:
            self.velocity.y = JUMP_FORCE * self.gravity_direction
            self.on_ground = False
            self.coyote_timer = 0
            self.jump_buffer_timer = 0
            self.is_jumping = True
            jump_occurred = True

        # Variable jump height: cut jump short if button released during ascent
        if self.is_jumping and not jump_pressed:
            moving_against_gravity = (
                self.gravity_direction > 0 and self.velocity.y < 0
            ) or (
                self.gravity_direction < 0 and self.velocity.y > 0
            )
            if moving_against_gravity:
                self.velocity.y *= self.JUMP_CUTOFF
            self.is_jumping = False

        # Apply gravity (direction-aware)
        self.velocity.y += GRAVITY * self.gravity_direction

        # Clamp fall speed
        if self.gravity_direction > 0 and self.velocity.y > MAX_FALL_SPEED:
            self.velocity.y = MAX_FALL_SPEED
        elif self.gravity_direction < 0 and self.velocity.y < -MAX_FALL_SPEED:
            self.velocity.y = MAX_FALL_SPEED

        # Clamp horizontal velocity to prevent tunneling
        if self.velocity.x > PLAYER_SPEED:
            self.velocity.x = PLAYER_SPEED
        elif self.velocity.x < -PLAYER_SPEED:
            self.velocity.x = -PLAYER_SPEED

        # Clamp vertical velocity to prevent tunneling
        max_vel = MAX_FALL_SPEED
        if self.velocity.y > max_vel:
            self.velocity.y = max_vel
        elif self.velocity.y < -max_vel:
            self.velocity.y = -max_vel

        # Resolve collisions using collision module
        self.on_ground = resolve_platform_collisions(self, platforms, self.gravity_direction)

        # Keep player within level bounds
        if self.collision_rect.left < 0:
            self.collision_rect.left = 0
            self.velocity.x = 0
        if self.collision_rect.right > level_width:
            self.collision_rect.right = level_width
            self.velocity.x = 0

        # Update animation
        self._update_animation()

        return jump_occurred

    def _update_animation(self):
        """Update the player's visual animation based on velocity."""
        # Determine target stretch based on vertical movement
        if self.on_ground:
            self.target_stretch = 1.0
        else:
            # Check if moving upward or falling relative to gravity
            moving_up = (
                self.gravity_direction > 0 and self.velocity.y < 0
            ) or (
                self.gravity_direction < 0 and self.velocity.y > 0
            )
            falling = (
                self.gravity_direction > 0 and self.velocity.y > 2
            ) or (
                self.gravity_direction < 0 and self.velocity.y < -2
            )

            if moving_up:
                # Stretch vertically when jumping up
                stretch_amount = min(abs(self.velocity.y) / abs(JUMP_FORCE), 1.0)
                self.target_stretch = 1.0 + (self.STRETCH_MAX - 1.0) * stretch_amount
            elif falling:
                # Compress when falling
                compress_amount = min(abs(self.velocity.y) / MAX_FALL_SPEED, 1.0)
                self.target_stretch = 1.0 - (1.0 - self.COMPRESS_MIN) * compress_amount
            else:
                self.target_stretch = 1.0

        # Smoothly interpolate toward target
        self.stretch_factor += (self.target_stretch - self.stretch_factor) * self.ANIMATION_SMOOTHING

        # Clamp stretch factor
        self.stretch_factor = max(self.COMPRESS_MIN, min(self.STRETCH_MAX, self.stretch_factor))

        # Calculate new dimensions
        new_height = int(self.original_height * self.stretch_factor)
        new_width = int(self.original_width / self.stretch_factor)  # Inverse for squash and stretch

        # Ensure minimum dimensions
        new_height = max(10, new_height)
        new_width = max(10, new_width)

        # Create scaled image
        self.image = pygame.transform.scale(
            pygame.Surface((self.original_width, self.original_height)),
            (new_width, new_height)
        )
        self.image.fill(RED)

        # Update draw rect to align with collision rect
        self.rect = self.image.get_rect()

        # Align based on gravity direction
        if self.gravity_direction > 0:
            # Normal gravity: align bottom
            self.rect.bottom = self.collision_rect.bottom
        else:
            # Reversed gravity: align top
            self.rect.top = self.collision_rect.top

        # Center horizontally
        self.rect.centerx = self.collision_rect.centerx

    def toggle_gravity(self):
        """Toggle gravity direction."""
        self.gravity_direction *= -1
        # Give a small impulse in the new direction
        self.velocity.y = 3 * self.gravity_direction
        self.on_ground = False
        self.coyote_timer = 0
        self.is_jumping = False

    def bounce(self):
        """Bounce the player (after stomping an enemy)."""
        self.velocity.y = self.BOUNCE_FORCE * self.gravity_direction
        self.coyote_timer = 0
        self.is_jumping = False

    def die(self):
        """Set player as dead."""
        self.alive = False
        # Reset to normal appearance
        self.stretch_factor = 1.0
        self.image = pygame.Surface((self.original_width, self.original_height))
        self.image.fill(RED)
        self.rect = self.collision_rect.copy()