import pygame


def resolve_platform_collisions(sprite, platforms):
    """Resolve collisions between sprite and platforms using axis-separated resolution.

    Args:
        sprite: Sprite with rect and velocity attributes
        platforms: List of pygame.Rect representing collision surfaces

    Returns:
        bool: True if sprite is on ground after resolution
    """
    # Resolve X-axis collisions
    sprite.rect.x += int(sprite.velocity.x)
    for platform in platforms:
        if sprite.rect.colliderect(platform):
            if sprite.velocity.x > 0:  # Moving right
                sprite.rect.right = platform.left
            elif sprite.velocity.x < 0:  # Moving left
                sprite.rect.left = platform.right
            sprite.velocity.x = 0

    # Resolve Y-axis collisions
    on_ground = False
    sprite.rect.y += int(sprite.velocity.y)
    for platform in platforms:
        if sprite.rect.colliderect(platform):
            if sprite.velocity.y > 0:  # Falling
                sprite.rect.bottom = platform.top
                sprite.velocity.y = 0
                on_ground = True
            elif sprite.velocity.y < 0:  # Jumping/hitting ceiling
                sprite.rect.top = platform.bottom
                sprite.velocity.y = 0

    return on_ground


def check_enemy_collision(player, enemies):
    """Check if player collides with any enemy and determine if it's a stomp.

    Args:
        player: Player sprite with rect and velocity
        enemies: List or group of Enemy sprites

    Returns:
        tuple: (enemy, is_stomp) where enemy is the collided enemy or None,
               and is_stomp is True if player stomped the enemy
    """
    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            # Check if player is falling and above enemy's midpoint
            if player.velocity.y > 0 and player.rect.bottom <= enemy.rect.centery:
                return (enemy, True)  # Stomp
            else:
                return (enemy, False)  # Hit from side or below
    return (None, False)


def check_goal_collision(player, goal_rect):
    """Check if player reached the goal.

    Args:
        player: Player sprite with rect
        goal_rect: pygame.Rect representing goal area

    Returns:
        bool: True if player collides with goal
    """
    return player.rect.colliderect(goal_rect)
