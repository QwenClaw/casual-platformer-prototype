import pygame


class Effect:
    """Represents an active effect on the player."""

    def __init__(self, name, color, duration=None):
        """Initialize an effect.

        Args:
            name: Display name of the effect
            color: RGB color tuple for HUD display
            duration: Duration in frames, or None for permanent until removed
        """
        self.name = name
        self.color = color
        self.duration = duration  # in frames, None means permanent
        self.active = True

    def update(self):
        """Update effect timer. Returns True if effect expired."""
        if self.duration is not None:
            self.duration -= 1
            if self.duration <= 0:
                self.active = False
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
    """Manages active effects on the player."""

    def __init__(self):
        """Initialize the effect manager."""
        self.effects = []

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
