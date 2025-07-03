import pygame
import sys
import random
from constants import *
from player import Player, Shield
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullets import Shot


def main():
    # Pygame variables
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    # If Player containers added to group, instantiate player object after not before so that its correctly added to groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    # Since shield is instantiate in in Player, i need to add this before creating player object, else its not added into the containers
    Shield.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    bullets = pygame.sprite.Group()
    Shot.containers = (bullets, updatable, drawable)

    # Game logic variables
    game_over = False
    shield = None

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

            # Awards shield power up for player accuracy. 
            # shield is None prevent more than 1 shield in game but doesnt prevent shield to be generated when player in shield power up
            # player.shield is None make sure no shield can be generated when player reach shield combo streak during shield power up
            if player.shield_combo_streak == 3 and shield is None and player.shield is None:
                x = random.randint(SHIELD_RADIUS, SCREEN_WIDTH - SHIELD_RADIUS)
                y = random.randint(SHIELD_RADIUS, SCREEN_HEIGHT - SHIELD_RADIUS)
                shield = Shield(x, y, SHIELD_RADIUS)
                player.shield_combo_streak = 0
            
            # Check whether player gets the game shield. If so, remove game shield and player now has a shield
            if shield and shield.is_collided(player):
                shield.kill()
                shield = None
                player.shield = Shield(player.position.x, player.position.y, SHIELD_RADIUS)
                player.invincible = 5
            
            # Remove player shield when timer expires
            if player.invincible < 0 and player.shield is not None:
                player.shield.kill()
                player.shield = None

            for asteroid in asteroids:
                asteroid.wrap_around()

                if asteroid.is_collided(player) and player.invincible < 0:
                    player.life -= 1
                    if player.life < 0:
                        game_over = True
                    
                    # Prevent player and asteroid always colliding
                    player.back_to_center()
                    asteroid.kill()
                    
                    # 5s invincibility after respawn
                    player.invincible = 5
                    
                    player.shield_combo_streak = 0

                # Shield power up kill asteroids like bullets
                if player.shield is not None and asteroid.is_collided(player.shield):
                    asteroid.split()
                    player.score = max(player.score + 1, player.streak + player.score)
                    player.streak += 1
                        
                for bullet in bullets:
                    if asteroid.is_collided(bullet):
                        bullet.kill()
                        asteroid.split()
                        player.score = max(player.score + 1, player.streak + player.score)
                        player.streak += 1
                        if player.shield_combo_streak < 3:
                            player.shield_combo_streak += 1
                    elif bullet.is_out_of_bounds():
                        bullet.kill()
                        player.streak = 0 
                        player.shield_combo_streak = 0          
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