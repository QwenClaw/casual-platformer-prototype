import pygame
from constants import MAX_FALL_SPEED, PLAYER_SPEED


def resolve_platform_collisions(sprite, platforms, gravity_direction=1):
    """Resolve collisions between sprite and platforms using axis-separated resolution.

    Uses substep collision to prevent tunneling through platforms at high speeds.
    Handles edge cases like sprite already inside a platform.

    Args:
        sprite: Sprite with rect and velocity attributes
        platforms: List of pygame.Rect representing collision surfaces
        gravity_direction: 1 for normal gravity, -1 for reversed

    Returns:
        bool: True if sprite is on ground after resolution
    """
    on_ground = False

    # Calculate total movement this frame
    dx = int(sprite.velocity.x)
    dy = int(sprite.velocity.y)

    # Substep collision for X axis to prevent tunneling
    steps_x = max(1, abs(dx))
    step_dx = dx / steps_x

    for _ in range(steps_x):
        sprite.rect.x += int(step_dx) if step_dx >= 0 else -int(abs(step_dx))
        # Handle fractional movement accumulation
        sprite.rect.x += round(step_dx - int(step_dx)) if abs(step_dx) >= 1 else 0

        for platform in platforms:
            if sprite.rect.colliderect(platform):
                if dx > 0:  # Moving right
                    sprite.rect.right = platform.left
                elif dx < 0:  # Moving left
                    sprite.rect.left = platform.right
                sprite.velocity.x = 0
                dx = 0
                break

    # Substep collision for Y axis to prevent tunneling
    steps_y = max(1, abs(dy))
    step_dy = dy / steps_y

    for _ in range(steps_y):
        sprite.rect.y += int(step_dy) if step_dy >= 0 else -int(abs(step_dy))

        for platform in platforms:
            if sprite.rect.colliderect(platform):
                if gravity_direction > 0:  # Normal gravity
                    if dy > 0:  # Falling
                        sprite.rect.bottom = platform.top
                        sprite.velocity.y = 0
                        on_ground = True
                    elif dy < 0:  # Jumping/hitting ceiling
                        sprite.rect.top = platform.bottom
                        sprite.velocity.y = 0
                else:  # Reversed gravity
                    if dy < 0:  # Falling (upward)
                        sprite.rect.top = platform.bottom
                        sprite.velocity.y = 0
                        on_ground = True
                    elif dy > 0:  # Jumping (downward)/hitting floor
                        sprite.rect.bottom = platform.top
                        sprite.velocity.y = 0
                dy = 0
                break

    # Final ground check - ensure sprite is resting on a platform
    if not on_ground:
        # Check if sprite is standing on a platform (small overlap check)
        test_rect = sprite.rect.copy()
        if gravity_direction > 0:
            test_rect.y += 2  # Check slightly below
        else:
            test_rect.y -= 2  # Check slightly above

        for platform in platforms:
            if test_rect.colliderect(platform):
                if gravity_direction > 0 and sprite.velocity.y >= 0:
                    on_ground = True
                elif gravity_direction < 0 and sprite.velocity.y <= 0:
                    on_ground = True
                break

    return on_ground


def check_enemy_collision(player, enemies):
    """Check if player collides with any enemy and determine if it's a stomp.

    Handles multiple enemy collisions - returns all collisions found.

    Args:
        player: Player sprite with rect and velocity
        enemies: List or group of Enemy sprites

    Returns:
        list: List of (enemy, is_stomp) tuples for all collisions
    """
    collisions = []
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            # Check if player is falling toward enemy based on gravity direction
            is_stomp = False
            if player.gravity_direction > 0:  # Normal gravity
                # Player falling down, stomp if above enemy midpoint
                if player.velocity.y > 0 and player.rect.bottom <= enemy.rect.centery + 4:
                    is_stomp = True
            else:  # Reversed gravity
                # Player falling up, stomp if below enemy midpoint
                if player.velocity.y < 0 and player.rect.top >= enemy.rect.centery - 4:
                    is_stomp = True
            collisions.append((enemy, is_stomp))
    return collisions


def check_goal_collision(player, goal_rect):
    """Check if player reached the goal.

    Args:
        player: Player sprite with rect
        goal_rect: pygame.Rect representing goal area

    Returns:
        bool: True if player collides with goal
    """
    return player.rect.colliderect(goal_rect)
