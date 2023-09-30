import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)

from DroppedBall import DroppedBall
from Colour import Colour

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Ball(pygame.sprite.Sprite):
    
    def __init__(self, x, y, score_handler):
        super(Ball, self).__init__()
        size = 50
        self.size = size
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.colour = Colour.RED.value
        pygame.draw.circle(self.surface, self.colour, (size // 2, size // 2), size // 2)
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score_handler = score_handler

    # Move the sprite based on keys
    def update(self, pressed_keys):

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def create_ball(self):
        new_ball = DroppedBall(self.rect.x, self.rect.y, self.size, self.colour, self.score_handler)
        self.score_handler.update_score(10)
        return new_ball