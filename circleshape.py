import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        self.position = pygame.Vector2(x,y)
        self.velocity = pygame.Vector2(0,0)
        self.radius = radius

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

    def is_collided(self, circle):
        return self.position.distance_to(circle.position) <= self.radius + circle.radius

    def is_out_of_bounds(self):
        return (
            self.position.x - self.radius > SCREEN_WIDTH or
            self.position.x + self.radius < 0 or
            self.position.y - self.radius > SCREEN_HEIGHT or
            self.position.y + self.radius < 0
        )