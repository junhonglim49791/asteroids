import pygame
import random
from constants import *
from player import Player, PowerUp
from asteroid import Asteroid
from asteroidfield import AsteroidField
from bullets import Shot
from explosion import ExplosionCircles


def main():
    # PYGAME VARIABLES
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    # convert() to prevent any unnecessary processing for pygame when displaying this image. Although no significant performance issues without it for now
    galaxy_background = pygame.image.load("galaxy.jpg").convert()
    # Change image size to fit determined game window
    galaxy_background = pygame.transform.scale(galaxy_background, screen.get_size())

    # Order: create groups -> add to class -> create objects. To prevent objects are not added correctly to the groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    PowerUp.containers = (updatable, drawable)
    ExplosionCircles.containers = (updatable, drawable)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    bullets = pygame.sprite.Group()
    Shot.containers = (bullets, updatable, drawable)

    # GAME LOGIC VARIABLES
    game_over = False
    # Easier to access in the game loop with the powerup_defs compared to:
    # shield = None
    # laser = None
    game_powerups = {"shield": None, "laser": None}

    # To loop every powerups in the game loop without repeating code, easier to extend or make changes. If not have to always copy paste for new powerups.
    # See ORIGINAL POWERUPS LOGIC below
    powerup_defs = {
        "shield": {
            "streak_name": "shield_combo_streak",
            "trigger_combo": SHIELD_TRIGGER_COMBO,
            "game_attr": "shield",
            "player_attr": "shield",
            "player_timer": "invincible",
            "timer_default": SHIELD_TIMER,
        },
        "laser": {
            "streak_name": "laser_combo_streak",
            "trigger_combo": LASER_TRIGGER_COMBO,
            "game_attr": "laser",
            "player_attr": "laser_power_up",
            "player_timer": "laser_timer",
            "timer_default": LASER_TIMER,
        },
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # update current player state before refreshing the screen, for now have no diff but this is standard practice
        updatable.update(dt)
        screen.blit(galaxy_background, (0, 0))

        if not game_over:
            for obj in drawable:
                obj.draw(screen)
            # Doesn't work because Group.draw() in sprite module expects "image" attribute
            # drawable.draw(screen)

            """ORIGINAL POWERUPS LOGIC
            # Awards shield power up for player's accuracy (killing asteroids without missing a bullet)
            # shield is None prevent more than 1 shield in game
            # player.shield is None prevent shield power up generated in game when player has it
            # if player.shield_combo_streak == 3 and shield is None and player.shield is None:
                  # Spawn PowerUp randomly within the game window
            #     x = random.randint(POWERUPS_RADIUS, SCREEN_WIDTH - POWERUPS_RADIUS)
            #     y = random.randint(POWERUPS_RADIUS, SCREEN_HEIGHT - POWERUPS_RADIUS)
            #     shield = PowerUp(x, y, POWERUPS_RADIUS, "shield")
            #     player.shield_combo_streak = 0

            # # Laser power up
            # if player.laser_combo_streak == 6 and laser is None and not player.laser_power_up:
            #     x = random.randint(POWERUPS_RADIUS, SCREEN_WIDTH - POWERUPS_RADIUS)
            #     y = random.randint(POWERUPS_RADIUS, SCREEN_HEIGHT - POWERUPS_RADIUS)
            #     laser = PowerUp(x, y, POWERUPS_RADIUS, "laser")
            #     player.laser_combo_streak = 0

            # # Check whether player gets the game shield. If so, remove game shield and player now has a shield
            # if shield and shield.is_collided(player):
            #     shield.kill()
            #     shield = None
            #     player.shield = PowerUp(player.position.x, player.position.y, POWERUPS_RADIUS, "shield", True)
            #     player.invincible = 5

            # if laser and laser.is_collided(player):
            #     laser.kill()
            #     laser = None
            #     player.laser_power_up = True
            #     player.laser_timer = 10

            # # Remove player's shield when timer expires
            # if player.invincible < 0 and player.shield is not None:
            #     player.shield.kill()
            #     player.shield = None

            # if player.laser_timer < 0 and player.laser_power_up:
            #     player.laser_power_up = False
            """

            """POWERUPS COMBO STREAK
            powerups combo streak increases up to the trigger combo (streak number to spawn power ups) and stop. It would be reset under 3 conditions:
                ctrl + F the implementation directs to that logic

            |        Logic         |             Implementation             |
            | -------------------- | -------------------------------------- |
            | Bullet out of bounds | bullet.is_out_of_bounds()              |
            | Generate Power Ups   | setattr(player, cfg["streak_name"], 0) |
            | Respawn              | player.back_to_center()                |

            """
            # Loop for power ups, logic check ORIGINAL POWERUPS LOGIC above
            for ptype, cfg in powerup_defs.items():
                if (
                    getattr(player, cfg["streak_name"]) == cfg["trigger_combo"]
                    and game_powerups[cfg["game_attr"]] is None
                    and not getattr(player, cfg["player_attr"])
                ):
                    x = random.randint(POWERUPS_RADIUS, SCREEN_WIDTH - POWERUPS_RADIUS)
                    y = random.randint(POWERUPS_RADIUS, SCREEN_HEIGHT - POWERUPS_RADIUS)
                    game_powerups[cfg["game_attr"]] = PowerUp(
                        x, y, POWERUPS_RADIUS, ptype
                    )
                    setattr(player, cfg["streak_name"], 0)

                if game_powerups[cfg["game_attr"]] and game_powerups[
                    cfg["game_attr"]
                ].is_collided(player):
                    game_powerups[cfg["game_attr"]].kill()
                    game_powerups[cfg["game_attr"]] = None
                    if ptype == "shield":
                        setattr(
                            player,
                            cfg["player_attr"],
                            PowerUp(
                                player.position.x,
                                player.position.y,
                                POWERUPS_RADIUS,
                                ptype,
                                True,
                            ),
                        )
                        setattr(player, cfg["player_timer"], cfg["timer_default"])
                    elif ptype == "laser":
                        setattr(player, cfg["player_attr"], True)
                        setattr(player, cfg["player_timer"], cfg["timer_default"])

                if getattr(player, cfg["player_timer"]) < 0 and getattr(
                    player, cfg["player_attr"]
                ):
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

                    # Prevent player and asteroid always colliding after respawn
                    player.back_to_center()
                    asteroid.kill()
                    player.invincible = 5

                    player.streak = 0
                    player.shield_combo_streak = 0
                    player.laser_combo_streak = 0

                """Scoring system
                    1. Each kill always get 1 score (bullet kill or player's shield kill).
                    2. Player combo streak (different with power ups streak) always add 1 if no bullet is out of bounds, else reset to 0. The streak will then add
                       to the score as bonus points.
                    Example: if current score is 10 and streak is 3, next kill will add 13 to player's score
                """
                # Shield power up kill asteroids like bullets
                if player.shield is not None and asteroid.is_collided(player.shield):
                    asteroid.split()
                    player.score = max(player.score + 1, player.streak + player.score)
                    player.streak += 1

                for bullet in bullets:
                    if asteroid.is_collided(bullet):
                        bullet.kill()
                        asteroid.split()
                        player.score = max(
                            player.score + 1, player.streak + player.score
                        )
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
            # Restart game by resetting all the current game states
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


if __name__ == "__main__":
    main()
