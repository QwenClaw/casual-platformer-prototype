import pygame


class Effect:
    """Represents an active effect on the player."""

    def __init__(self, name, color, duration=None, on_expire=None):
        """Initialize an effect.

        Args:
            name: Display name of the effect
            color: RGB color tuple for HUD display
            duration: Duration in frames, or None for permanent until removed
            on_expire: Optional callback to call when effect expires
        """
        self.name = name
        self.color = color
        self.duration = duration  # in frames, None means permanent
        self.active = True
        self.on_expire = on_expire

    def update(self):
        """Update effect timer. Returns True if effect expired."""
        if self.duration is not None:
            self.duration -= 1
            if self.duration <= 0:
                self.active = False
                if self.on_expire:
                    self.on_expire()
                return True
        return False

    def get_duration_text(self):
        """Get formatted duration text for display."""
        if self.duration is None:
            return ""
        # Convert frames to seconds (assuming 60 FPS)
        seconds = self.duration / 60.0
        return f" ({seconds:.1f}s)"


class EffectManager:
    """Manages active effects on the player and world."""

    def __init__(self, game):
        """Initialize the effect manager.

        Args:
            game: Reference to the Game instance to access level and enemies
        """
        self.effects = []
        self.game = game
        self.original_gravity = None  # Will be set when gravity change effect is applied
        self.original_enemy_speeds = {}  # Store original speeds of enemies

    def add_effect(self, effect):
        """Add an effect, replacing any existing effect with the same name.

        Args:
            effect: Effect instance to add
        """
        # Remove any existing effect with the same name
        self.effects = [e for e in self.effects if e.name != effect.name]
        self.effects.append(effect)

    def remove_effect(self, name):
        """Remove an effect by name.

        Args:
            name: Name of the effect to remove
        """
        self.effects = [e for e in self.effects if e.name != name]

    def has_effect(self, name):
        """Check if an effect with the given name is active.

        Args:
            name: Name of the effect to check

        Returns:
            True if the effect is active
        """
        return any(e.name == name and e.active for e in self.effects)

    def update(self):
        """Update all effects and remove expired ones."""
        for effect in self.effects:
            effect.update()
        # Remove inactive effects
        self.effects = [e for e in self.effects if e.active]

    def get_active_effects(self):
        """Get list of currently active effects.

        Returns:
            List of active Effect instances
        """
        return [e for e in self.effects if e.active]

    def clear(self):
        """Remove all effects."""
        self.effects = []

    def trigger_random_effect(self):
        """Trigger a random world change effect on enemy kill."""
        import random
        from constants import GRAVITY, ENEMY_SPEED, FAST_ENEMY_SPEED, FLYING_ENEMY_SPEED
        
        effect_types = ['platform_move', 'gravity_change', 'enemy_speed_increase']
        chosen_effect = random.choice(effect_types)
        
        if chosen_effect == 'platform_move':
            self._apply_platform_move_effect()
        elif chosen_effect == 'gravity_change':
            self._apply_gravity_change_effect()
        elif chosen_effect == 'enemy_speed_increase':
            self._apply_enemy_speed_increase_effect()

    def _apply_platform_move_effect(self):
        """Apply platform movement effect: shift platforms slightly."""
        level = self.game.level_manager.get_current_level()
        # Store original positions
        original_positions = [(p.x, p.y) for p in level.platforms]
        # Shift each platform by a small random amount
        shifts = []
        for platform in level.platforms:
            shift_x = random.randint(-10, 10)
            shift_y = random.randint(-5, 5)
            platform.x += shift_x
            platform.y += shift_y
            shifts.append((shift_x, shift_y))
        # Create revert callback
        def revert_platforms():
            for i, platform in enumerate(level.platforms):
                if i < len(original_positions):
                    platform.x, platform.y = original_positions[i]
        # Create an effect to revert after duration
        effect = Effect("Platforms Shifted", (255, 165, 0), duration=300, on_expire=revert_platforms)
        self.add_effect(effect)

    def _apply_gravity_change_effect(self):
        """Apply gravity change effect: slightly modify gravity value."""
        from constants import GRAVITY
        # Store original gravity in instance if not already stored
        if not hasattr(self, 'original_gravity') or self.original_gravity == 0.8:
            self.original_gravity = GRAVITY
        # Slightly increase or decrease gravity
        change = random.uniform(0.2, 0.5) * random.choice([-1, 1])
        new_gravity = GRAVITY + change
        # Update gravity in constants (hacky but works for prototype)
        import constants
        constants.GRAVITY = new_gravity
        # Create revert callback using stored original gravity
        def revert_gravity():
            import constants
            constants.GRAVITY = self.original_gravity
        effect = Effect("Gravity Changed", (128, 0, 128), duration=300, on_expire=revert_gravity)  # 5 seconds
        self.add_effect(effect)

    def _apply_enemy_speed_increase_effect(self):
        """Apply enemy speed increase effect: temporarily increase speed of all enemies."""
        from constants import ENEMY_SPEED, FAST_ENEMY_SPEED, FLYING_ENEMY_SPEED
        # Capture current speeds at the time of effect application
        current_speeds = {
            'ENEMY_SPEED': ENEMY_SPEED,
            'FAST_ENEMY_SPEED': FAST_ENEMY_SPEED,
            'FLYING_ENEMY_SPEED': FLYING_ENEMY_SPEED
        }
        # Increase speeds using current values
        import constants
        constants.ENEMY_SPEED = current_speeds['ENEMY_SPEED'] * 1.5
        constants.FAST_ENEMY_SPEED = current_speeds['FAST_ENEMY_SPEED'] * 1.5
        constants.FLYING_ENEMY_SPEED = current_speeds['FLYING_ENEMY_SPEED'] * 1.5
        # Create revert callback that captures the speeds at this moment
        def revert_enemy_speeds():
            import constants
            constants.ENEMY_SPEED = current_speeds['ENEMY_SPEED']
            constants.FAST_ENEMY_SPEED = current_speeds['FAST_ENEMY_SPEED']
            constants.FLYING_ENEMY_SPEED = current_speeds['FLYING_ENEMY_SPEED']
        effect = Effect("Enemies Faster", (255, 0, 0), duration=300, on_expire=revert_enemy_speeds)  # 5 seconds
        self.add_effect(effect)

    def _schedule_revert(self, effect_type, *args):
        """Schedule revert of an effect after duration."""
        # For simplicity, we'll handle reverts in the effect's update method
        # by checking the effect name and applying revert logic
        pass
