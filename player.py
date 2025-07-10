import pygame
from circleshape import CircleShape
from constants import *
from bullets import Shot
import math


class PowerUp(CircleShape):
    def __init__(self, x, y, radius, p_type="", with_player=False):
        super().__init__(x, y, radius)
        # Relative vectors to be added with either player's or the powerups' position
        self.dotted_circles = [
            pygame.Vector2(
                math.cos(math.radians(30) * i), math.sin(math.radians(30) * i)
            )
            * self.radius
            for i in range(0, 12)
        ]
        # To rotate the powerups
        self.rotation_angle = 0
        self.p_type = p_type
        self.with_player = with_player

    def draw(self, screen):
        for circle in self.dotted_circles:
            # if i passed in rotated_circle to draw.circle() without adding the position, the circle is rotated relative to origin (top left corner of the game
            # window)
            rotated_circle = circle.rotate(self.rotation_angle)
            rotated_position = self.position + rotated_circle
            pygame.draw.circle(
                screen, color="white", center=rotated_position, radius=2, width=2
            )

            power_type = pygame.font.Font(None, 40).render(
                self.p_type[0].upper(), True, "white"
            )
            if not self.with_player and self.p_type == "shield":
                screen.blit(power_type, (self.position.x - 10, self.position.y - 10))
            if self.p_type == "laser":
                screen.blit(power_type, (self.position.x - 10, self.position.y - 10))

    def update(self, dt):
        self.rotation_angle += 30 * dt

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
        self.laser_combo_streak = 0
        self.laser_power_up = False
        self.laser_timer = 0
        self.max_speed = PLAYER_SPEED
        self.speed = 0
        self.w_accel = None

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        # Draw inner triangle after respawn to show player's invincibility
        if self.invincible > 0:
            d = self.position + right
            e = self.position - right
            f = self.position - forward * self.radius
            return [[a, b, c], [d, e, f]]

        return [[a, b, c]]

    def draw(self, screen):
        score = pygame.font.Font(None, 36).render(
            f"Score: {str(self.score)}", True, "white"
        )
        streak = pygame.font.Font(None, 36).render(
            f"{str(self.streak)}x Combo", True, "white"
        )
        lives = pygame.font.Font(None, 36).render(
            f"{str(self.life)} Live(s)", True, "white"
        )
        shield_combo = pygame.font.Font(None, 36).render(
            f"Shield {str(self.shield_combo_streak)}/{SHIELD_TRIGGER_COMBO}",
            True,
            "white",
        )
        laser_combo = pygame.font.Font(None, 36).render(
            f"Laser {str(self.laser_combo_streak)}/{LASER_TRIGGER_COMBO}", True, "white"
        )
        screen.blit(score, (5, 5))
        screen.blit(streak, (5, 40))
        screen.blit(lives, (5, 75))
        screen.blit(shield_combo, (5, 110))
        screen.blit(laser_combo, (5, 145))

        pygame.draw.polygon(screen, color="white", points=self.triangle()[0], width=2)
        if self.invincible > 0 and self.shield is None:
            pygame.draw.polygon(
                screen, color="white", points=self.triangle()[1], width=2
            )

    def show_highest_score(self, screen):
        highest_score = pygame.font.Font(None, 80).render(
            f"Nice try! Your Score: {self.score}", True, "white"
        )
        screen.blit(highest_score, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 3))
        new_game = pygame.font.Font(None, 80).render(
            f"Press 'E' to restart", True, "white"
        )
        screen.blit(new_game, (SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2))

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    """Acceleration
    Player player moves in a direction (W/S) it accelerates, but when the opposition direction key is pressed, player starts decelerate until 0 and pick up speed
    again. In this case, when player manually decelerates its faster than letting the player object to decelerate naturally (no direction keys are pressed) for more 
    control.
    """

    def inc_accel(self, dt):
        if self.speed <= self.max_speed:
            self.speed += dt * PLAYER_ACCELERATION

    def dec_accel(self, dt):
        if self.speed > 0:
            self.speed -= dt * PLAYER_DECELERATION
        else:
            self.speed = 0
            self.w_accel = None

    def update(self, dt):
        self.invincible -= dt
        self.laser_timer -= dt
        keys = pygame.key.get_pressed()

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            self.dec_accel(dt)

        if self.w_accel:
            self.move(dt)
        else:
            self.move(-dt)

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            # Check whether player is pressing S to accelerate, if so pressing W will decelerates
            if self.w_accel is False:
                self.dec_accel(dt * MANUAL_DECELERATION_MULTIPLIER)
                return
            self.inc_accel(dt)
            self.move(dt)
            self.w_accel = True

        if keys[pygame.K_s]:
            if self.w_accel:
                self.dec_accel(dt * MANUAL_DECELERATION_MULTIPLIER)
                return
            self.inc_accel(dt)
            self.move(-dt)
            self.w_accel = False

        if keys[pygame.K_SPACE]:
            self.shoot(dt)

    def move(self, dt):
        # +ve rotate clockwise, vice versa
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # += forward only still works, but doesn't make it frame independent. self.speed is now a variable instead of constant for acceleration logic
        self.position += forward * self.speed * dt

        # player shield has to keep track of player position to always display correctly around player
        if self.shield is not None:
            self.shield.position = self.position

    # For respawn purpose
    def back_to_center(self):
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    def shoot(self, dt):
        self.shoot_cooldown -= dt

        # If player has laser power up, then no cooldown for shooting speed
        if self.shoot_cooldown > 0 and not self.laser_power_up:
            return

        bullet = Shot(self.position[0], self.position.y, SHOT_RADIUS)
        bullet.velocity += (
            pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        )

        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
