import pygame
import math
import struct
import os


class SoundManager:
    """Manages game sounds with graceful fallback."""

    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init()
        except pygame.error:
            self.enabled = False
            return

        # Try to load .wav files from assets/ folder
        self.jump_sound = self._load_sound("assets/jump.wav")
        self.stomp_sound = self._load_sound("assets/stomp.wav")
        self.win_sound = self._load_sound("assets/win.wav")
        self.death_sound = self._load_sound("assets/death.wav")
        self.gravity_sound = self._load_sound("assets/gravity.wav")

        # Generate sounds if files don't exist
        if self.jump_sound is None:
            self.jump_sound = self._generate_jump_sound()
        if self.stomp_sound is None:
            self.stomp_sound = self._generate_stomp_sound()
        if self.win_sound is None:
            self.win_sound = self._generate_win_sound()
        if self.death_sound is None:
            self.death_sound = self._generate_death_sound()
        if self.gravity_sound is None:
            self.gravity_sound = self._generate_gravity_sound()

    def _load_sound(self, filepath):
        """Try to load a sound file. Returns None if file doesn't exist."""
        if not self.enabled:
            return None
        try:
            if os.path.exists(filepath):
                return pygame.mixer.Sound(filepath)
        except (pygame.error, FileNotFoundError):
            pass
        return None

    def _generate_jump_sound(self):
        """Generate an ascending tone (440Hz to 880Hz, 100ms)."""
        if not self.enabled:
            return None

        try:
            sample_rate = 44100
            duration = 0.1
            n_samples = int(round(duration * sample_rate))
            buf = bytearray(n_samples * 2)
            max_sample = 32767

            for i in range(n_samples):
                progress = i / n_samples
                frequency = 440 + (440 * progress)
                sample = int(max_sample * 0.7 * math.sin(2 * math.pi * frequency * i / sample_rate))
                struct.pack_into('<h', buf, i * 2, sample)

            return pygame.mixer.Sound(buffer=bytes(buf))
        except Exception:
            return None

    def _generate_stomp_sound(self):
        """Generate a short descending/pop tone."""
        if not self.enabled:
            return None

        try:
            sample_rate = 44100
            duration = 0.15
            n_samples = int(round(duration * sample_rate))
            buf = bytearray(n_samples * 2)
            max_sample = 32767

            for i in range(n_samples):
                progress = i / n_samples
                frequency = 600 - (450 * progress)
                amplitude = 1.0 - (progress * 0.8)
                sample = int(max_sample * amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
                struct.pack_into('<h', buf, i * 2, sample)

            return pygame.mixer.Sound(buffer=bytes(buf))
        except Exception:
            return None

    def _generate_win_sound(self):
        """Generate a triumphant ascending arpeggio (C-E-G-C)."""
        if not self.enabled:
            return None

        try:
            sample_rate = 44100
            note_duration = 0.12
            notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
            total_duration = note_duration * len(notes)
            n_samples = int(round(total_duration * sample_rate))
            buf = bytearray(n_samples * 2)
            max_sample = 32767

            for i in range(n_samples):
                note_index = int(i / (note_duration * sample_rate))
                if note_index >= len(notes):
                    note_index = len(notes) - 1
                frequency = notes[note_index]
                sample = int(max_sample * 0.6 * math.sin(2 * math.pi * frequency * i / sample_rate))
                struct.pack_into('<h', buf, i * 2, sample)

            return pygame.mixer.Sound(buffer=bytes(buf))
        except Exception:
            return None

    def _generate_death_sound(self):
        """Generate a descending sad tone."""
        if not self.enabled:
            return None

        try:
            sample_rate = 44100
            duration = 0.4
            n_samples = int(round(duration * sample_rate))
            buf = bytearray(n_samples * 2)
            max_sample = 32767

            for i in range(n_samples):
                progress = i / n_samples
                frequency = 400 - (200 * progress)
                amplitude = 1.0 - (progress * 0.7)
                sample = int(max_sample * amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
                struct.pack_into('<h', buf, i * 2, sample)

            return pygame.mixer.Sound(buffer=bytes(buf))
        except Exception:
            return None

    def _generate_gravity_sound(self):
        """Generate a whoosh-like sound for gravity toggle."""
        if not self.enabled:
            return None

        try:
            sample_rate = 44100
            duration = 0.2
            n_samples = int(round(duration * sample_rate))
            buf = bytearray(n_samples * 2)
            max_sample = 32767

            for i in range(n_samples):
                progress = i / n_samples
                # Sweep from low to high then back down
                if progress < 0.5:
                    frequency = 200 + (600 * progress * 2)
                else:
                    frequency = 800 - (600 * (progress - 0.5) * 2)
                amplitude = 0.8
                sample = int(max_sample * amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
                struct.pack_into('<h', buf, i * 2, sample)

            return pygame.mixer.Sound(buffer=bytes(buf))
        except Exception:
            return None

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

    def play_death(self):
        """Play death sound."""
        if self.enabled and self.death_sound:
            self.death_sound.play()

    def play_gravity_toggle(self):
        """Play gravity toggle sound."""
        if self.enabled and self.gravity_sound:
            self.gravity_sound.play()
