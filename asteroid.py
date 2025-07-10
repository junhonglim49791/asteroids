import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from explosion import ExplosionCircles


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, choice):
        super().__init__(x, y, radius)
        # I found that if generate radius length by a long r long r short r pattern, the circle will not looks very sharp.
        self.asteroid_styles = [
            [
                # Each lumpy circle is formed by 10 points. Using i % 3 != 2, for every 3 radius, the first 2 would be longer than the 3rd.
                #  Example: when i = 0 i = 1, these 2 radius would range from 0.8 to 1. Where i = 2 the radius range from 0.5 to 0.7
                (
                    random.uniform(self.radius * 0.8, self.radius * 1)
                    if i % 3 != 2
                    else random.uniform(self.radius * 0.5, self.radius * 0.7)
                )
                for i in range(0, 10)
            ],
            [
                # Using i % 4 != 3, for every 4 radius, the first 3 would be longer than the 4th
                (
                    random.uniform(self.radius * 0.8, self.radius * 1)
                    if i % 4 != 3
                    else random.uniform(self.radius * 0.5, self.radius * 0.7)
                )
                for i in range(0, 10)
            ],
            [
                # # Using i % 5 != 4, for every 5 radius, the first 4 would be longer than the 5th
                (
                    random.uniform(self.radius * 0.8, self.radius * 1)
                    if i % 5 != 4
                    else random.uniform(self.radius * 0.5, self.radius * 0.7)
                )
                for i in range(0, 10)
            ],
        ]
        # To choose 1 out of the 3 patterns in asteroid_styles
        self.index = choice

    def lumpy_circle(self):
        angle_interval = 36
        return [
            self.position + pygame.Vector2(0, 1).rotate(angle_interval * i) * r
            for i, r in enumerate(self.asteroid_styles[self.index])
        ]

    def draw(self, screen):
        pygame.draw.polygon(screen, color="white", points=self.lumpy_circle(), width=2)

    def update(self, dt):
        self.position += self.velocity * dt

    def is_collided(self, circle):
        return super().is_collided(circle)

    def split(self):
        # Even the asteroid object is kill. It still exists in this function so its variables are still accessible
        self.kill()
        explosion_effect = ExplosionCircles(self.position.x, self.position.y)

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        angle = random.uniform(20, 50)
        rotate_angle_1 = self.velocity.rotate(angle)
        rotate_angle_2 = self.velocity.rotate(-angle)

        asteroid_style_choice_1 = random.randint(0, 2)
        asteroid_style_choice_2 = random.randint(0, 2)

        smaller_radius = self.radius - ASTEROID_MIN_RADIUS
        smaller_asteroid_1 = Asteroid(
            self.position.x, self.position.y, smaller_radius, asteroid_style_choice_1
        )
        smaller_asteroid_2 = Asteroid(
            self.position.x, self.position.y, smaller_radius, asteroid_style_choice_2
        )

        smaller_asteroid_1.velocity += rotate_angle_1 * 1.2
        smaller_asteroid_2.velocity += rotate_angle_2 * 1.2
