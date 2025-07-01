import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullets import Shot

def main():
    pygame.init()
    game_over = False
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    # If Player containers added to group, instantiate player object after not before so that its correctly added to groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    bullets = pygame.sprite.Group()
    Shot.containers = (bullets, updatable, drawable)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

       # update current player state before refreshing the screen, for now might have no diff but this is standard practice
        updatable.update(dt)
        screen.fill("black")

        player.invincible -= dt

        if not game_over:
            for obj in drawable:
                obj.draw(screen)
            # Doesn't work because Group.draw() in sprite module expects "image" attribute
            # drawable.draw(screen)

            for asteroid in asteroids:
                if asteroid.is_collided(player) and player.invincible < 0:
                    player.life -= 1
                    if player.life < 0:
                        game_over = True
                    
                    # Prevent player and asteroid always colliding
                    player.back_to_center()
                    asteroid.kill()
                    
                    # 5s invincibility after respawn
                    player.invincible = 5
                    
                asteroid.wrap_around()
                    
                for bullet in bullets:
                    if asteroid.is_collided(bullet):
                        bullet.kill()
                        asteroid.split()
                        player.score = max(player.score + 1, player.streak + player.score)
                        player.streak += 1

                    elif bullet.is_out_of_bounds():
                        bullet.kill()
                        player.streak = 0           
        else:
            player.show_highest_score(screen)

        pygame.display.flip()
        delta_time = clock.tick(60)
        dt = delta_time / 1000

        
    print("Starting Asteroids!")
    print(
        f"Screen width: {SCREEN_WIDTH}\n"
        f"Screen height: {SCREEN_HEIGHT}"
    )

if __name__ == "__main__":
    main()