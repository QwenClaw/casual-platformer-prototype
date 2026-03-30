import pygame
from constants import SCREEN_W, SCREEN_H, TILE_SIZE
from enemy import Enemy


class Level:
    """Stores level data: platforms, enemies, goal, and spawn point."""

    def __init__(self):
        self.platforms = []
        self.enemies = []
        self.goal = None
        self.spawn_point = (0, 0)
        self._build_level()

    def _build_level(self):
        """Create hardcoded level data."""
        ground_y = SCREEN_H - TILE_SIZE

        # Spawn point at left side of level
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Ground segments with a gap/pitfall
        # Left ground segment
        self.platforms.append(pygame.Rect(0, ground_y, TILE_SIZE * 10, TILE_SIZE))

        # Gap between x=320 and x=448 (4 tiles wide)

        # Middle ground segment
        self.platforms.append(pygame.Rect(TILE_SIZE * 14, ground_y, TILE_SIZE * 8, TILE_SIZE))

        # Another gap between x=576 and x=704 (4 tiles wide)

        # Right ground segment
        self.platforms.append(pygame.Rect(TILE_SIZE * 22, ground_y, TILE_SIZE * 10, TILE_SIZE))

        # Floating platforms
        # Platform 1: over first gap
        self.platforms.append(pygame.Rect(TILE_SIZE * 11, ground_y - TILE_SIZE * 3, TILE_SIZE * 2, TILE_SIZE))

        # Platform 2: higher, over second gap
        self.platforms.append(pygame.Rect(TILE_SIZE * 18, ground_y - TILE_SIZE * 5, TILE_SIZE * 2, TILE_SIZE))

        # Platform 3: mid-height floating platform
        self.platforms.append(pygame.Rect(TILE_SIZE * 6, ground_y - TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE))

        # Platform 4: floating platform near end
        self.platforms.append(pygame.Rect(TILE_SIZE * 25, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))

        # Enemies
        # Enemy 1: patrols on left ground segment
        enemy1 = Enemy(
            x=TILE_SIZE * 4,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 3,
            patrol_right=TILE_SIZE * 8
        )
        self.enemies.append(enemy1)

        # Enemy 2: patrols on middle ground segment
        enemy2 = Enemy(
            x=TILE_SIZE * 16,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 15,
            patrol_right=TILE_SIZE * 20
        )
        self.enemies.append(enemy2)

        # Enemy 3: patrols on right ground segment
        enemy3 = Enemy(
            x=TILE_SIZE * 26,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 24,
            patrol_right=TILE_SIZE * 29
        )
        self.enemies.append(enemy3)

        # Goal at far right of level
        self.goal = pygame.Rect(TILE_SIZE * 30, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE * 3)
