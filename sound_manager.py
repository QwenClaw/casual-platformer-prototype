import pygame
import math
import struct


class SoundManager:
    """Manages game sounds with graceful fallback."""

    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return

        # Generate simple sounds
        self.jump_sound = self._generate_tone(440, 0.1)
        self.stomp_sound = self._generate_tone(220, 0.2)
        self.win_sound = self._generate_tone(880, 0.5)

    def _generate_tone(self, frequency, duration):
        """Generate a simple sine wave tone."""
        if not self.enabled:
            return None

        sample_rate = 44100
        n_samples = int(round(duration * sample_rate))

        buf = bytearray(n_samples * 2)
        max_sample = 32767

        for i in range(n_samples):
            sample = int(max_sample * math.sin(2 * math.pi * frequency * i / sample_rate))
            struct.pack_into('<h', buf, i * 2, sample)

        return pygame.mixer.Sound(buffer=bytes(buf))

    def play_jump(self):
        """Play jump sound."""
        if self.enabled and self.jump_sound:
            self.jump_sound.play()

    def play_stomp(self):
        """Play stomp sound."""
        if self.enabled and self.stomp_sound:
            self.stomp_sound.play()

    def play_win(self):
        """Play win sound."""
        if self.enabled and self.win_sound:
            self.win_sound.play()
