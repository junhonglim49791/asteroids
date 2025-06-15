from circleshape import CircleShape
import pygame

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, color="white", center=self.position, radius=self.radius, width=2)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def is_collided(self, circle):
        return super().is_collided(circle)