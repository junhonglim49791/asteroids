import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
        pygame.draw.circle(screen, color="white", center=self.position, radius=self.radius, width=2)
    
    def update(self, dt):
        self.position += self.velocity * dt
    
    def is_collided(self, circle):
        return super().is_collided(circle)

    def split(self):
        self.kill()

        if (self.radius <= ASTEROID_MIN_RADIUS):
            return

        angle = random.uniform(20, 50)
        rotate_angle_1 = self.velocity.rotate(angle)
        rotate_angle_2 = self.velocity.rotate(-angle)

        smaller_radius = self.radius - ASTEROID_MIN_RADIUS
        smaller_asteroid_1 = Asteroid(self.position.x, self.position.y, smaller_radius)
        smaller_asteroid_2 = Asteroid(self.position.x, self.position.y, smaller_radius)

        smaller_asteroid_1.velocity = rotate_angle_1 * 1.2
        smaller_asteroid_2.velocity += rotate_angle_2 * 1.2

