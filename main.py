import pygame
import sys
import random
from constants import *
from player import Player, PowerUp
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
    PowerUp.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)
    
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    bullets = pygame.sprite.Group()
    Shot.containers = (bullets, updatable, drawable)

    # Game logic variables
    game_over = False
    # shield = None
    # laser = None
    game_powerups = {
        "shield": None,
        "laser": None
    }
    
    # PowerUps dict
    powerup_defs = {
        "shield":{
            "streak_name": "shield_combo_streak",
            "trigger_combo": SHIELD_TRIGGER_COMBO,
            "game_attr": "shield",
            "player_attr": "shield",
            "player_timer": "invincible",
            "timer_default": SHIELD_TIMER
        },
        "laser":{
            "streak_name": "laser_combo_streak",
            "trigger_combo": LASER_TRIGGER_COMBO,
            "game_attr": "laser",
            "player_attr": "laser_power_up",
            "player_timer": "laser_timer",
            "timer_default": LASER_TIMER
        }
    }
        
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

       # update current player state before refreshing the screen, for now might have no diff but this is standard practice
        updatable.update(dt)
        screen.fill("black")

        player.invincible -= dt
        player.laser_timer -= dt

        if not game_over:
            for obj in drawable:
                obj.draw(screen)
            # Doesn't work because Group.draw() in sprite module expects "image" attribute
            # drawable.draw(screen)

            # Awards shield power up for player accuracy. 
            # shield is None prevent more than 1 shield in game but doesnt prevent shield to be generated when player in shield power up
            # player.shield is None make sure no shield can be generated when player reach shield combo streak during shield power up
            # if player.shield_combo_streak == 3 and shield is None and player.shield is None:
            #     x = random.randint(SHIELD_RADIUS, SCREEN_WIDTH - SHIELD_RADIUS)
            #     y = random.randint(SHIELD_RADIUS, SCREEN_HEIGHT - SHIELD_RADIUS)
            #     shield = PowerUp(x, y, SHIELD_RADIUS, "shield")
            #     player.shield_combo_streak = 0

            # # Laser power up
            # if player.laser_combo_streak == 6 and laser is None and not player.laser_power_up:
            #     x = random.randint(SHIELD_RADIUS, SCREEN_WIDTH - SHIELD_RADIUS)
            #     y = random.randint(SHIELD_RADIUS, SCREEN_HEIGHT - SHIELD_RADIUS)
            #     laser = PowerUp(x, y, SHIELD_RADIUS, "laser")
            #     player.laser_combo_streak = 0

            # # Check whether player gets the game shield. If so, remove game shield and player now has a shield
            # if shield and shield.is_collided(player):
            #     shield.kill()
            #     shield = None
            #     player.shield = PowerUp(player.position.x, player.position.y, SHIELD_RADIUS, "shield", True)
            #     player.invincible = 5
            
            # if laser and laser.is_collided(player):
            #     laser.kill()
            #     laser = None
            #     player.laser_power_up = True
            #     player.laser_timer = 10

            # # Remove player shield when timer expires
            # if player.invincible < 0 and player.shield is not None:
            #     player.shield.kill()
            #     player.shield = None

            # if player.laser_timer < 0 and player.laser_power_up:
            #     player.laser_power_up = False
            
            # Loop for power ups
            for ptype, cfg in powerup_defs.items():
                if getattr(player, cfg["streak_name"]) == cfg["trigger_combo"] and game_powerups[cfg["game_attr"]] is None and not getattr(player, cfg["player_attr"]):
                        x = random.randint(SHIELD_RADIUS, SCREEN_WIDTH - SHIELD_RADIUS)
                        y = random.randint(SHIELD_RADIUS, SCREEN_HEIGHT - SHIELD_RADIUS)
                        game_powerups[cfg["game_attr"]] = PowerUp(x, y, SHIELD_RADIUS, ptype)
                        setattr(player, cfg["streak_name"], 0)

                if game_powerups[cfg["game_attr"]] and game_powerups[cfg["game_attr"]].is_collided(player):
                    game_powerups[cfg["game_attr"]].kill()
                    game_powerups[cfg["game_attr"]] = None
                    if ptype == "shield":
                        setattr(player, cfg["player_attr"], PowerUp(player.position.x, player.position.y, SHIELD_RADIUS, ptype, True))
                        setattr(player, cfg["player_timer"], cfg["timer_default"])
                    elif ptype == "laser":
                        setattr(player, cfg["player_attr"], True)
                        setattr(player, cfg["player_timer"], cfg["timer_default"])

                if getattr(player, cfg["player_timer"]) < 0 and getattr(player, cfg["player_attr"]):
                    if ptype == "shield":
                        getattr(player, cfg["player_attr"]).kill()
                        setattr(player, cfg["player_attr"], None)
                    elif ptype == "laser":  
                        setattr(player, cfg["player_attr"], False)

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

                    player.streak = 0 
                    player.shield_combo_streak = 0
                    player.laser_combo_streak = 0

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
                        if player.shield_combo_streak < SHIELD_TRIGGER_COMBO:
                            player.shield_combo_streak += 1
                        if player.laser_combo_streak < LASER_TRIGGER_COMBO:
                            player.laser_combo_streak += 1
                    elif bullet.is_out_of_bounds():
                        bullet.kill()
                        player.streak = 0 
                        player.shield_combo_streak = 0 
                        player.laser_combo_streak = 0         
        else:           
            player.show_highest_score(screen)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e]:
                player.kill()
                # Using empty() need to reassign updatable and drawable again
                # asteroids.empty()
                # updatable.empty()
                # drawable.empty()
                for asteroid in asteroids:
                    asteroid.kill()
                for bullet in bullets:
                    bullet.kill()
                if game_powerups["shield"]:
                    game_powerups["shield"].kill()
                if game_powerups["laser"]:
                    game_powerups["laser"].kill()
                game_powerups["shield"] = None
                game_powerups["laser"] = None
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                game_over = False



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