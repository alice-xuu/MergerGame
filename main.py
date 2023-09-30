from ScoreHandler import ScoreHandler
import pygame

from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
)
from Ball import Ball
from Bird import Bird
from Colour import Colour

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

dropped_balls = pygame.sprite.Group()
sprites_bg = pygame.sprite.Group()

# Initialize score and font
score_handler = ScoreHandler()
font = pygame.font.Font(None, 36)

player = Ball(SCREEN_WIDTH/2, 50, score_handler)

# custom events
ADDBIRD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDBIRD, 1000)


clock = pygame.time.Clock()
running = True
# Run until the user chooses to quit
while running:

    screen.fill((232, 220, 242 ))

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            
            # escape
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE:
                new_ball = player.create_ball()
                dropped_balls.add(new_ball)

        # Window close button
        elif event.type == QUIT:
            running = False

        # Add new bird
        elif event.type == ADDBIRD:
            new_bird = Bird()
            sprites_bg.add(new_bird)

            
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    dropped_balls.update(dropped_balls)
    sprites_bg.update()

    # Draw all sprites

    for entity in sprites_bg:
        screen.blit(entity.surface, entity.rect)

    screen.blit(player.surface, player.rect)
    for entity in dropped_balls:
        screen.blit(entity.surface, entity.rect)
    
    # Render the score text
    score_text = font.render("Score: " + str(score_handler.get_score()), True, Colour.WHITE.value)
    score_rect = score_text.get_rect()
    score_rect.topleft = (10, 10)
    screen.blit(score_text, score_rect)

    if score_handler.gameover:
        running = False

    # Flip everything to the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

pygame.quit()