import pygame
from constants import SCREEN_W, SCREEN_H, FPS, BLACK


class Game:
    """Main game loop and state manager."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Casual Platformer Prototype")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Update game state."""
        pass

    def draw(self):
        """Render the frame."""
        self.screen.fill(BLACK)
        pygame.display.flip()
