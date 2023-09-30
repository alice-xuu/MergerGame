import pygame

from Colour import Colour
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRAVITY = 0.4
DECAY = 0.6
COLLISION_DECAY = 0.5

class DroppedBall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, size, colour, score_handler):
        super(DroppedBall, self).__init__()
        
        self.surface = pygame.Surface((size, size), pygame.SRCALPHA)
        self.colour = colour
        pygame.draw.circle(self.surface, self.colour, (size // 2, size // 2), size // 2)
        self.size = size
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.dx = 0
        self.dy = 10
        self.score_handler = score_handler
        self.delete = False
        

    # Drop ball until hit bottom of window or other balls
    def update(self, dropped_balls):


        # Update velocity due to gravity
        self.dy += GRAVITY

        # Update position based on velocity
        
        self.rect.x += self.dx
        self.rect.y += self.dy


        # Check for collisions with the bottom of the window
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT - 1  # Prevent the ball from going below the bottom
            self.dy *= -DECAY
        if self.rect.top <= 0:
            self.rect.top = 1
            self.dy *= -DECAY
            self.score_handler.update_gameover()
        if self.rect.left < 0:
            self.rect.left = 1
            self.dx *= -DECAY
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH -1
            self.dx *= -DECAY


        # Check for collisions with other balls
        for ball in dropped_balls:
            if ball != self:  # Avoid checking collision with itself
                if pygame.sprite.collide_rect(self, ball):

                    # faster ball is merged into slower ball
                    if self.colour == ball.colour:
                        if self.dy + self.dx <= ball.dy + ball.dx:
                            is_pink = False
                            if self.colour == Colour.RED.value:
                                self.colour = Colour.ORANGE.value
                                self.score_handler.update_score(50)
                            elif self.colour == Colour.ORANGE.value:
                                self.colour = Colour.YELLOW.value
                                self.score_handler.update_score(100)
                            elif self.colour == Colour.YELLOW.value:
                                self.colour = Colour.GREEN.value
                                self.score_handler.update_score(200)
                            elif self.colour == Colour.GREEN.value:
                                self.colour = Colour.BLUE.value
                                self.score_handler.update_score(400)
                            elif self.colour == Colour.BLUE.value:
                                self.colour = Colour.INDIGO.value
                                self.score_handler.update_score(800)
                            elif self.colour == Colour.INDIGO.value:
                                self.colour = Colour.PINK.value
                                self.score_handler.update_score(1600)

                            elif self.colour == Colour.PINK.value:
                                is_pink = True
                                self.delete = True
                                ball.delete = True
                                self.score_handler.update_score(5000)
                            if not is_pink:
                                self.size *= 1.2
                                x = self.rect.centerx
                                y = self.rect.centery
                                self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
                                pygame.draw.circle(self.surface, self.colour, (self.size // 2, self.size // 2), self.size // 2)
                                self.rect = self.surface.get_rect()
                                self.rect.centerx = x
                                self.rect.centery = y
                                ball.delete = True
                            
                    else:
                        # Calculate the new position to prevent overlap
                        distx = (self.rect.centerx) - (ball.rect.centerx)
                        disty = (self.rect.centery)  - (ball.rect.centery)
                        distance = math.hypot(distx, disty)
                        min_distance = max(self.rect.width, ball.rect.width)
                        overlap = min_distance - distance

                        if distance != 0:
                            distx /= distance
                            disty /= distance
                            adjust_x = distx * overlap / 2
                            adjust_y = disty * overlap / 2

                            self.rect.x += adjust_x
                            self.rect.y += adjust_y

                        # Calculate collision angle
                        angle = math.atan2(self.rect.centery - ball.rect.centery, self.rect.centerx - ball.rect.centerx)

                        # Calculate new velocities
                        combined_speed = math.sqrt(self.dx ** 2 + self.dy ** 2) + math.sqrt(ball.dx ** 2 + ball.dy ** 2)
                        new_dx1 = math.cos(angle) * combined_speed
                        new_dy1 = math.sin(angle) * combined_speed
                        new_dx2 = math.cos(angle + math.pi) * combined_speed
                        new_dy2 = math.sin(angle + math.pi) * combined_speed

                        # Set new velocities for both balls
                        self.dx, self.dy = new_dx1 * COLLISION_DECAY, new_dy1 * COLLISION_DECAY
                        ball.dx, ball.dy = new_dx2 * COLLISION_DECAY, new_dy2 * COLLISION_DECAY
                    
        for ball in dropped_balls:
            if ball.delete:
                dropped_balls.remove(ball)


    def update_circle_color(self):
        size = self.size
        pygame.draw.circle(self.surface, self.colour, (size // 2, size // 2), size // 2)

def is_negative(value):
    return value < 0