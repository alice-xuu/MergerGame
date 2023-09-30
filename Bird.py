import pygame

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

import random

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super(Bird, self).__init__()
        self.surface = pygame.image.load("assets/bird.jpeg").convert()
        self.surface.set_colorkey((255, 255, 255), RLEACCEL)
        self.surface = pygame.transform.scale(self.surface, (25,25))

        # The starting position is randomly generated
        self.rect = self.surface.get_rect(
            center=(
                0,
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the bird, remove when hit right wall
    def update(self):
        self.rect.move_ip(10, 0)
        if self.rect.right < 0:
            self.kill()