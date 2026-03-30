import pygame
from constants import SCREEN_W, SCREEN_H, TILE_SIZE, NUM_LEVELS
from enemy import Enemy, FastEnemy, FlyingEnemy


class Level:
    """Stores level data: platforms, enemies, goal, and spawn point."""

    def __init__(self, level_index=0):
        self.platforms = []
        self.enemies = []
        self.goal = None
        self.spawn_point = (0, 0)
        self.level_index = level_index
        self._build_level(level_index)

    def _build_level(self, level_index):
        """Create level data based on level index."""
        builders = [
            self._build_level_1,
            self._build_level_2,
            self._build_level_3,
            self._build_level_4,
            self._build_level_5,
            self._build_level_6,
            self._build_level_7,
        ]
        if 0 <= level_index < len(builders):
            builders[level_index]()
        else:
            builders[0]()

    def _build_level_1(self):
        """Level 1: Simple introduction - flat ground with one enemy."""
        ground_y = SCREEN_H - TILE_SIZE
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Full ground
        self.platforms.append(pygame.Rect(0, ground_y, SCREEN_W, TILE_SIZE))

        # A few floating platforms
        self.platforms.append(pygame.Rect(TILE_SIZE * 5, ground_y - TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 12, ground_y - TILE_SIZE * 4, TILE_SIZE * 3, TILE_SIZE))

        # One patrol enemy
        self.enemies.append(Enemy(
            x=TILE_SIZE * 10,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 8,
            patrol_right=TILE_SIZE * 15
        ))

        # Goal at far right
        self.goal = pygame.Rect(TILE_SIZE * 23, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE * 3)

    def _build_level_2(self):
        """Level 2: Gaps introduction - ground with gaps."""
        ground_y = SCREEN_H - TILE_SIZE
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Ground segments with gaps
        self.platforms.append(pygame.Rect(0, ground_y, TILE_SIZE * 8, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 12, ground_y, TILE_SIZE * 6, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 22, ground_y, TILE_SIZE * 10, TILE_SIZE))

        # Platforms over gaps
        self.platforms.append(pygame.Rect(TILE_SIZE * 9, ground_y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 19, ground_y - TILE_SIZE * 3, TILE_SIZE * 2, TILE_SIZE))

        # Enemies
        self.enemies.append(Enemy(
            x=TILE_SIZE * 4,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 2,
            patrol_right=TILE_SIZE * 7
        ))
        self.enemies.append(Enemy(
            x=TILE_SIZE * 14,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 13,
            patrol_right=TILE_SIZE * 17
        ))

        # Goal
        self.goal = pygame.Rect(TILE_SIZE * 30, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE * 3)

    def _build_level_3(self):
        """Level 3: Floating platforms - platforms above gaps."""
        ground_y = SCREEN_H - TILE_SIZE
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Ground segments
        self.platforms.append(pygame.Rect(0, ground_y, TILE_SIZE * 6, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 24, ground_y, TILE_SIZE * 8, TILE_SIZE))

        # Floating platform staircase
        self.platforms.append(pygame.Rect(TILE_SIZE * 7, ground_y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 10, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 13, ground_y - TILE_SIZE * 6, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 16, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 19, ground_y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 22, ground_y - TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE))

        # Flying enemy in the middle
        self.enemies.append(FlyingEnemy(
            x=TILE_SIZE * 13,
            y=ground_y - TILE_SIZE * 5,
            patrol_top=ground_y - TILE_SIZE * 7,
            patrol_bottom=ground_y - TILE_SIZE * 3
        ))

        # Ground enemy
        self.enemies.append(Enemy(
            x=TILE_SIZE * 26,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 25,
            patrol_right=TILE_SIZE * 30
        ))

        # Goal
        self.goal = pygame.Rect(TILE_SIZE * 30, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE * 3)

    def _build_level_4(self):
        """Level 4: More enemies - multiple patrol enemies."""
        ground_y = SCREEN_H - TILE_SIZE
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Ground with small gaps
        self.platforms.append(pygame.Rect(0, ground_y, TILE_SIZE * 10, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 11, ground_y, TILE_SIZE * 8, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 20, ground_y, TILE_SIZE * 12, TILE_SIZE))

        # High platforms for safety
        self.platforms.append(pygame.Rect(TILE_SIZE * 9, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 18, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))

        # Multiple enemies including fast enemy
        self.enemies.append(Enemy(
            x=TILE_SIZE * 4,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 2,
            patrol_right=TILE_SIZE * 8
        ))
        self.enemies.append(FastEnemy(
            x=TILE_SIZE * 14,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 12,
            patrol_right=TILE_SIZE * 18
        ))
        self.enemies.append(Enemy(
            x=TILE_SIZE * 24,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 21,
            patrol_right=TILE_SIZE * 28
        ))
        self.enemies.append(FastEnemy(
            x=TILE_SIZE * 28,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 26,
            patrol_right=TILE_SIZE * 30
        ))

        # Goal
        self.goal = pygame.Rect(TILE_SIZE * 30, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE * 3)

    def _build_level_5(self):
        """Level 5: Vertical challenge - tall platforms."""
        ground_y = SCREEN_H - TILE_SIZE
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Ground segments
        self.platforms.append(pygame.Rect(0, ground_y, TILE_SIZE * 8, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 22, ground_y, TILE_SIZE * 10, TILE_SIZE))

        # Tall vertical platforms
        self.platforms.append(pygame.Rect(TILE_SIZE * 10, ground_y - TILE_SIZE * 8, TILE_SIZE * 2, TILE_SIZE * 8))
        self.platforms.append(pygame.Rect(TILE_SIZE * 15, ground_y - TILE_SIZE * 6, TILE_SIZE * 2, TILE_SIZE * 6))
        self.platforms.append(pygame.Rect(TILE_SIZE * 20, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE * 4))

        # Floating platforms at various heights
        self.platforms.append(pygame.Rect(TILE_SIZE * 8, ground_y - TILE_SIZE * 3, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 12, ground_y - TILE_SIZE * 5, TILE_SIZE * 3, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 17, ground_y - TILE_SIZE * 7, TILE_SIZE * 3, TILE_SIZE))

        # Flying enemies
        self.enemies.append(FlyingEnemy(
            x=TILE_SIZE * 12,
            y=ground_y - TILE_SIZE * 4,
            patrol_top=ground_y - TILE_SIZE * 6,
            patrol_bottom=ground_y - TILE_SIZE * 2
        ))
        self.enemies.append(FlyingEnemy(
            x=TILE_SIZE * 18,
            y=ground_y - TILE_SIZE * 6,
            patrol_top=ground_y - TILE_SIZE * 8,
            patrol_bottom=ground_y - TILE_SIZE * 4
        ))

        # Ground enemy
        self.enemies.append(Enemy(
            x=TILE_SIZE * 25,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 23,
            patrol_right=TILE_SIZE * 30
        ))

        # Goal at top
        self.goal = pygame.Rect(TILE_SIZE * 17, ground_y - TILE_SIZE * 10, TILE_SIZE, TILE_SIZE * 2)

    def _build_level_6(self):
        """Level 6: Gravity introduction - designed for gravity reversal."""
        ground_y = SCREEN_H - TILE_SIZE
        ceiling_y = 0
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Ground
        self.platforms.append(pygame.Rect(0, ground_y, TILE_SIZE * 8, TILE_SIZE))
        # Ceiling (becomes ground when gravity reversed)
        self.platforms.append(pygame.Rect(0, ceiling_y, TILE_SIZE * 8, TILE_SIZE))

        # Middle platforms
        self.platforms.append(pygame.Rect(TILE_SIZE * 10, ground_y - TILE_SIZE * 2, TILE_SIZE * 3, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 10, TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE))

        # Far section with ground and ceiling
        self.platforms.append(pygame.Rect(TILE_SIZE * 18, ground_y, TILE_SIZE * 14, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 18, ceiling_y, TILE_SIZE * 14, TILE_SIZE))

        # Platforms in the middle area
        self.platforms.append(pygame.Rect(TILE_SIZE * 15, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 15, TILE_SIZE * 5, TILE_SIZE * 2, TILE_SIZE))

        # Enemies
        self.enemies.append(Enemy(
            x=TILE_SIZE * 4,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 2,
            patrol_right=TILE_SIZE * 7
        ))
        self.enemies.append(FlyingEnemy(
            x=TILE_SIZE * 15,
            y=ground_y - TILE_SIZE * 3,
            patrol_top=TILE_SIZE * 4,
            patrol_bottom=ground_y - TILE_SIZE * 3
        ))
        self.enemies.append(FastEnemy(
            x=TILE_SIZE * 22,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 19,
            patrol_right=TILE_SIZE * 28
        ))

        # Goal
        self.goal = pygame.Rect(TILE_SIZE * 30, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE * 3)

    def _build_level_7(self):
        """Level 7: Final challenge - combines all elements."""
        ground_y = SCREEN_H - TILE_SIZE
        self.spawn_point = (TILE_SIZE * 2, ground_y - 48)

        # Ground segments with multiple gaps
        self.platforms.append(pygame.Rect(0, ground_y, TILE_SIZE * 6, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 8, ground_y, TILE_SIZE * 4, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 14, ground_y, TILE_SIZE * 4, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 20, ground_y, TILE_SIZE * 4, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 26, ground_y, TILE_SIZE * 6, TILE_SIZE))

        # Complex floating platform layout
        self.platforms.append(pygame.Rect(TILE_SIZE * 7, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 12, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 18, ground_y - TILE_SIZE * 5, TILE_SIZE * 2, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 24, ground_y - TILE_SIZE * 4, TILE_SIZE * 2, TILE_SIZE))

        # High platforms
        self.platforms.append(pygame.Rect(TILE_SIZE * 9, ground_y - TILE_SIZE * 7, TILE_SIZE * 3, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 15, ground_y - TILE_SIZE * 8, TILE_SIZE * 3, TILE_SIZE))
        self.platforms.append(pygame.Rect(TILE_SIZE * 21, ground_y - TILE_SIZE * 7, TILE_SIZE * 3, TILE_SIZE))

        # All enemy types
        self.enemies.append(Enemy(
            x=TILE_SIZE * 3,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 1,
            patrol_right=TILE_SIZE * 5
        ))
        self.enemies.append(FastEnemy(
            x=TILE_SIZE * 10,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 9,
            patrol_right=TILE_SIZE * 11
        ))
        self.enemies.append(FlyingEnemy(
            x=TILE_SIZE * 12,
            y=ground_y - TILE_SIZE * 3,
            patrol_top=ground_y - TILE_SIZE * 6,
            patrol_bottom=ground_y - TILE_SIZE * 2
        ))
        self.enemies.append(Enemy(
            x=TILE_SIZE * 16,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 15,
            patrol_right=TILE_SIZE * 17
        ))
        self.enemies.append(FastEnemy(
            x=TILE_SIZE * 22,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 21,
            patrol_right=TILE_SIZE * 23
        ))
        self.enemies.append(FlyingEnemy(
            x=TILE_SIZE * 21,
            y=ground_y - TILE_SIZE * 5,
            patrol_top=ground_y - TILE_SIZE * 8,
            patrol_bottom=ground_y - TILE_SIZE * 4
        ))
        self.enemies.append(Enemy(
            x=TILE_SIZE * 28,
            y=ground_y - TILE_SIZE,
            patrol_left=TILE_SIZE * 27,
            patrol_right=TILE_SIZE * 30
        ))

        # Goal at the end
        self.goal = pygame.Rect(TILE_SIZE * 30, ground_y - TILE_SIZE * 3, TILE_SIZE, TILE_SIZE * 3)


class LevelManager:
    """Manages level progression."""

    def __init__(self):
        self.current_level_index = 0
        self.current_level = Level(self.current_level_index)

    def get_current_level(self):
        """Get the current level."""
        return self.current_level

    def next_level(self):
        """Advance to the next level. Returns True if there is a next level."""
        self.current_level_index += 1
        if self.current_level_index >= NUM_LEVELS:
            return False
        self.current_level = Level(self.current_level_index)
        return True

    def restart_level(self):
        """Restart the current level."""
        self.current_level = Level(self.current_level_index)

    def reset(self):
        """Reset to level 1."""
        self.current_level_index = 0
        self.current_level = Level(self.current_level_index)

    def is_final_level(self):
        """Check if current level is the final level."""
        return self.current_level_index >= NUM_LEVELS - 1

    def get_level_number(self):
        """Get the current level number (1-indexed)."""
        return self.current_level_index + 1
