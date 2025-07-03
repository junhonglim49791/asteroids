import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from bullets import Shot
import math

class Shield(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        # I don't have to add position during instantiation, can add all these circles with Shield's current position
        self.dotted_circles = [pygame.Vector2(math.cos(math.radians(30)*i), math.sin(math.radians(30)*i)) * self.radius for i in range(0, 12)]
        # self.base_vectors = [
        #     pygame.Vector2(0, self.radius).rotate(i * 360 / 12)  # 12 dots
        #     for i in range(12)
        # ]
        self.rotation_angle = 0

    # def draw(self, screen):
    #     for vec in self.base_vectors:
    #         rotated_vec = vec.rotate(self.rotation_angle)
    #         pos = self.position + rotated_vec
    #         pygame.draw.circle(screen, color="white", center=pos, radius=2, width=2)

    def draw(self, screen):
        for circle in self.dotted_circles:
            # if i passed in rotated_circle to draw.circle(), the circle is rotated relative to origin (top left corner of the game window)
            rotated_circle = circle.rotate(self.rotation_angle)
            # all these dotted circles should always be relative to the shield's current position
            rotated_position = self.position + rotated_circle
            pygame.draw.circle(screen, color="white", center=rotated_position, radius=2, width=2)
    
    def update(self, dt):
        self.rotation_angle += 30*dt

    def is_collided(self, circle):
        return super().is_collided(circle)

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.score = 0
        self.streak = 0
        self.life = 3
        self.invincible = 0
        self.shield = None
        self.shield_combo_streak = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        
        # Draw inner triangle after respawn
        if self.invincible > 0:
            d = self.position + right
            e = self.position - right
            f = self.position - forward * self.radius   
            return [[a, b, c], [d, e, f]]  

        return [[a,b,c]]

    def draw(self, screen):
        score = pygame.font.Font(None, 36).render(f"Score: {str(self.score)}", True, "white")
        streak = pygame.font.Font(None, 36).render(f"{str(self.streak)}x Combo", True, "white")
        lives = pygame.font.Font(None, 36).render(f"{str(self.life)} Live(s)", True, "white")
        shield_combo = pygame.font.Font(None, 36).render(f"Shield {str(self.shield_combo_streak)}/3", True, "white")
        screen.blit(score, (5, 5))
        screen.blit(streak, (5, 40))
        screen.blit(lives, (5, 75))
        screen.blit(shield_combo, (5, 110))

        # self.shield.draw(screen)

        pygame.draw.polygon(screen, color="white", points=self.triangle()[0], width=2)  
        if self.invincible > 0 and self.shield is None:
            pygame.draw.polygon(screen, color="white", points=self.triangle()[1], width=2)   

        # Check real shape and triangle shape difference
        # pygame.draw.circle(screen, color="white", center=self.position, radius=self.radius, width=2)
        # pygame.draw.polygon(screen, color="white", points=self.triangle()[0], width=2)     
      

    def show_highest_score(self, screen):
        highest_score = pygame.font.Font(None, 80).render(f"Nice try! Your Score: {self.score}", True, "white")
        screen.blit(highest_score, (SCREEN_WIDTH/6, SCREEN_HEIGHT/3))

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
            
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)
            
        if keys[pygame.K_s]:
            self.move(-dt)
        
        if keys[pygame.K_SPACE]:
            self.shoot(dt)

    
    def move(self, dt):
        # +ve rotate clockwise, vice versa
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # += forward works, but doesn't make it frame independent
        self.position += forward * PLAYER_SPEED * dt

        # player shield has to keep track of player position to always display correctly around player
        if self.shield is not None:
            self.shield.position = self.position
        
    def back_to_center(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
    def shoot(self, dt):
        self.shoot_cooldown -= dt

        if(self.shoot_cooldown > 0):
            return
            
        bullet = Shot(self.position[0], self.position.y, SHOT_RADIUS)
        bullet.velocity += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

        PLAYER_SHOOT_COOLDOWN = 0.3
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
       
            