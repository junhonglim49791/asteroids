import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
from bullets import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.score = 0
        self.streak = 0
        self.life = 3
        self.invincible = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        
        return [a,b,c]

    def shield_triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        d = self.position + right
        e = self.position - right
        f = self.position - forward * self.radius

        return [d,e,f]
        
    def draw(self, screen):
        score = pygame.font.Font(None, 36).render(f"Score: {str(self.score)}", True, "white")
        streak = pygame.font.Font(None, 36).render(f"{str(self.streak)}x Combo", True, "white")
        lives = pygame.font.Font(None, 36).render(f"{str(self.life)} Live(s)", True, "white")
        screen.blit(score, (5, 5))
        screen.blit(streak, (5, 40))
        screen.blit(lives, (5, 75))

        pygame.draw.polygon(screen, color="white", points=self.triangle(), width=2)  
        if self.invincible > 0:
            pygame.draw.polygon(screen, color="white", points=self.shield_triangle(), width=2)        
      

    def show_highest_score(self, screen):
        highest_score = pygame.font.Font(None, 80).render(f"Nice try! Your Score: {self.score}", True, "white")
        screen.blit(highest_score, (SCREEN_WIDTH/4, SCREEN_HEIGHT/3))

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
       
            