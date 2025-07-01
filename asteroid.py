import pygame
import random
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, choice):
        super().__init__(x, y, radius)
        # randomize radius cannot be too small or too big, hit bos will be confusing
        self.asteroid_styles = [
            [random.uniform(self.radius * 0.8, self.radius * 1) if i % 3 != 2 else random.uniform(self.radius * 0.5, self.radius * 0.7) for i in range(0,10)],
            [random.uniform(self.radius * 0.8, self.radius * 1) if i % 4 != 3 else random.uniform(self.radius * 0.5, self.radius * 0.7) for i in range(0,10)],
            [random.uniform(self.radius * 0.8, self.radius * 1) if i % 5 != 4 else random.uniform(self.radius * 0.5, self.radius * 0.7) for i in range(0,10)]
        ]   
        self.index = choice


    def lumpy_circle(self):
        angle_interval = 36
        # print(self.radius)
        # print(self.random_radius)
        # a = self.position + pygame.Vector2(0, 1).rotate(36)*self.radius*0.9
        # b = self.position + pygame.Vector2(0, 1).rotate(72)*self.radius*0.9
        # c = self.position + pygame.Vector2(0, 1).rotate(108)*self.radius*0.6
        # d = self.position + pygame.Vector2(0, 1).rotate(144)*self.radius*0.8
        # e = self.position + pygame.Vector2(0, 1).rotate(180)*self.radius*0.8
        # f = self.position + pygame.Vector2(0, 1).rotate(216)*self.radius*0.6
        # g = self.position + pygame.Vector2(0, 1).rotate(252)*self.radius*0.7
        # h = self.position + pygame.Vector2(0, 1).rotate(288)*self.radius*0.7
        # i = self.position + pygame.Vector2(0, 1).rotate(324)*self.radius*0.6
        # j = self.position + pygame.Vector2(0, 1).rotate(360)*self.radius*0.9
        # return [j,h,c,d,e,f,g,b,i,a]
        return [self.position + pygame.Vector2(0, 1).rotate(angle_interval * i) * r for i, r in enumerate(self.asteroid_styles[self.index])]

    def draw(self, screen):
        # pygame.draw.circle(screen, color="white", center=self.position, radius=self.radius, width=2)
        pygame.draw.polygon(screen, color="white", points=self.lumpy_circle(), width=2)  
        
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

        asteroid_style_choice_1 = random.randint(0, 2)
        asteroid_style_choice_2 = random.randint(0, 2)

        smaller_radius = self.radius - ASTEROID_MIN_RADIUS
        smaller_asteroid_1 = Asteroid(self.position.x, self.position.y, smaller_radius, asteroid_style_choice_1)
        smaller_asteroid_2 = Asteroid(self.position.x, self.position.y, smaller_radius, asteroid_style_choice_2)

        smaller_asteroid_1.velocity += rotate_angle_1 * 1.2
        smaller_asteroid_2.velocity += rotate_angle_2 * 1.2

