import pygame
from constants import EXPLOSION_SPEED, EXPLOSION_TIMER


# Draw the 4 circles which move in fixed angles in a period of time
class ExplosionCircles(pygame.sprite.Sprite):
    def __init__(self, x, y):

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.asteroid_position = pygame.Vector2(x, y)
        self.timer = EXPLOSION_TIMER
        # 4 angles
        self.directions = [
            pygame.Vector2(0, 1).rotate(45),
            pygame.Vector2(0, 1).rotate(-45),
            pygame.Vector2(0, 1).rotate(135),
            pygame.Vector2(0, 1).rotate(-135),
        ]

        self.explosion_radius = 0

    def draw(self, screen):
        for direction in self.directions:
            pygame.draw.circle(
                screen,
                color="white",
                center=direction * self.explosion_radius + self.asteroid_position,
                radius=2,
                width=2,
            )

    def update(self, dt):
        self.timer -= dt
        if self.timer < 0:
            self.kill()
        # Update explosion radius so that 4 circles will keep moving on screen
        self.explosion_radius += EXPLOSION_SPEED * dt
