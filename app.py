import pygame
from pygame.sprite import Group
from config import Config
from ship import Ship
from alien import Alien
from star import Star
import game
from stats import Stats
from leaderboard import Leaderboard
from button import Button




def run():
    # Initialize game and create a screen object
    settings = Config()
    stats = Stats(settings)
    

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(settings.default_size)
    pygame.display.set_caption(settings.default_name)
    play_button = Button(settings, screen, "Play")
    game_over = Button(settings, screen, "Game Over", 600, 75)
    leader = Leaderboard(settings, screen, stats)

    stars = Group()

    # Make a ship
    ship = Ship(settings, screen)

    # Make a group to store projectiles in
    projectiles = Group()

    # Make an invasion group
    aliens = Group()
    game.create_fleet(settings, screen, ship, aliens)

    # Start the main game loop
    while True:

        # Watch for keyboard and mouse events
        game.check_events(settings, screen, stats, leader, play_button, ship, aliens, projectiles)

        #game.update_screen(settings, screen, stats, leader, ship, aliens, projectiles, play_button)

        if stats.game_active:
            ship.update()
            game.update_projectiles(settings, screen, stats, leader, ship, aliens, projectiles)
            game.update_aliens(settings, stats, screen, leader, ship, aliens, projectiles)
        
        game.update_screen(settings, screen, stats, leader, ship, aliens, projectiles, play_button, game_over)

run()