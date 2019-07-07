import sys
from time import sleep
import pygame
from projectile import Projectile
from alien import Alien
from star import Star




def check_keydown_events(event, settings, screen, stats, leader, ship, aliens, projectiles):
    """ Respond to key presses"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_p:
        if not stats.game_active:
            start_game(settings, screen, stats, leader, ship, aliens, projectiles)
    elif event.key == pygame.K_SPACE:
        fire_projectile(settings, screen, ship, projectiles)
    elif (pygame.key.get_mods() & pygame.KMOD_LCTRL) and event.key == pygame.K_i or event.key == pygame.K_i:
        print("Game Options opened!")
    elif (pygame.key.get_mods() & pygame.KMOD_LCTRL) and event.key == pygame.K_r:
        print("Reseting the game...")
        reset_game(settings, screen, stats, leader, ship, aliens, projectiles, hard=True)
    elif (pygame.key.get_mods() & pygame.KMOD_LCTRL) and event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        print("Thank you for playing Alien Invasion!")
        print("Check out more web and desktop applications at https://www.brizzle.dev")
        sys.exit()


def check_keyup_events(event, ship):
    """ Respond to key releases """
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False


def check_events(settings, screen, stats, leader, play_button, ship, aliens, projectiles):
    """ Respond to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, stats, leader, ship, aliens, projectiles)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, leader, play_button, ship, aliens, projectiles, mouse_x, mouse_y)
        

def start_game(settings, screen, stats, leader, ship, aliens, projectiles):
    pygame.mouse.set_visible(False)
    stats.game_active = True
    leader.prep_score()
    leader.prep_high_score()
    leader.prep_level()
    stats.reset_stats_hard() 
    settings.initialize_dynamic_settings()
    reset_game(settings, screen, stats, leader, ship, aliens, projectiles, hard=True)


def check_play_button(settings, screen, stats, leader, play_button, ship, aliens, projectiles, mouse_x, mouse_y):
    """ Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mixer.Sound('assets/blop.wav').play()
        start_game(settings, screen, stats, leader, ship, aliens, projectiles)


def check_high_score(stats, leader):
    """ Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        leader.prep_high_score()


def update_screen(options, screen, stats, leader, ship, aliens, projectiles, play_button, game_over_btn):
    """ Update images on the screen and flip to the new screen"""
    
    # Redraw the screen during each pass through the loop
    screen.fill(options.default_bg_color)
    # Redraw all bullsets behind ship and aliens
    for projectile in projectiles.sprites():
        projectile.draw()
    ship.blitme()
    aliens.draw(screen)

    leader.show_score()

    if not stats.game_active:
        if stats.ships_left == 0:
            game_over_btn.draw()
        leader.show_controls()
        play_button.draw()

    # Make the most recently drawn screen visible
    pygame.display.flip()



def update_projectiles(settings, screen, stats, leader, ship, aliens, projectiles):
    """ Update the position of projectiles and get rid of old ones"""
    projectiles.update()


    # Get rid of projectiles that have cleared the screen
    for projectile in projectiles.copy():
        if projectile.rect.bottom <= 0:
            projectiles.remove(projectile)

    check_bullet_alien_collisions(settings, screen, stats, leader, ship, aliens, projectiles)


def check_bullet_alien_collisions(settings, screen, stats, leader, ship, aliens, projectiles):
    """ Respond to bullet-alien collisions"""

    # Remove any bullets and aliens that have collided
    collisions = pygame.sprite.groupcollide(projectiles, aliens, True, True)
    
    if collisions:
        for aliens in collisions.values():
            pygame.mixer.Sound('assets/alien.wav').play()
            stats.score += settings.alien_points * len(aliens)
            leader.prep_score()
        check_high_score(stats, leader)

    if len(aliens) == 0:
        settings.increase_speed()
        stats.level += 1
        leader.prep_level()
        reset_game(settings, screen, stats, leader, ship, aliens, projectiles)


def ship_hit(settings, stats, screen, leader, ship, aliens, projectiles):
    """ Respond to being hit by alien"""
    if stats.ships_left > 1:
        pygame.mixer.Sound('assets/hurt.wav').play()
        # Decrement ships lef
        stats.ships_left -= 1
        stats.score = 0
        leader.prep_ships()
        leader.prep_score()

        # Create a new fleet and center the ship
        reset_game(settings, screen, stats, leader, ship, aliens, projectiles)
    else:
        pygame.mixer.Sound('assets/death.wav').play()
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(settings, stats, screen, leader, ship, aliens, projectiles):
    """ Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit
            ship_hit(settings, stats, screen, leader, ship, aliens, projectiles)
            break


def update_aliens(settings, stats, screen, leader, ship, aliens, projectiles):
    """ update the positions of all aliens in the fleet"""
    check_fleet_edges(settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, leader, ship, aliens, projectiles)

    check_aliens_bottom(settings, stats, screen, leader, ship, aliens, projectiles)


def reset_game(settings, screen, stats, leader, ship, aliens, projectiles, hard=False):
    # Destroy existing projectiles and instantiate a new fleet
    projectiles.empty()

    aliens.empty()
    stats.reset_stats_soft()

    create_fleet(settings, screen, ship, aliens)
    ship.center_ship()
    sleep(1)


def fire_projectile(settings, screen, ship, projectiles):
    """ Fire a projectile if limit not reached"""

    # Create a new projectile and add it to the projectiles group
    if len(projectiles) < settings.projectile_limit:
        projectile = Projectile(settings, screen, ship)
        projectiles.add(projectile)
        pygame.mixer.Sound('assets/laser.wav').play()


def get_number_aliens(settings, alien_width):
    """ Determine the number of aliens that fit in a row."""
    available_space_x = settings.default_screen_width - 2 * alien_width
    return int(available_space_x / (2 * alien_width))


def get_number_stars(settings, star_width):
    available_space_x = settings.default_screen_width - 2 * star_width
    return int(available_space_x / (2 * star_width))


def get_number_rows(settings, ship_height, alien_height):
    """ Determine the number of rows of aliens that fit on the screen."""

    available_space_y = (settings.default_screen_height - (3 * alien_height) - ship_height)
    return int(available_space_y / (2 * alien_height))


def get_screen_rows(settings, star_height):

    available_space_y = (settings.default_screen_height - (2 * star_height))
    return int(available_space_y / (2 * star_height))


def create_alien(settings, screen, aliens, alien_number, row_number):
    """ Create an alien and place it in the row."""
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_star(settings, screen, stars, star_number, row_number):

    star = Star(settings, screen)
    star_width = star.rect.width
    star.x = star_width + 2 * star_width * star_number
    star.rect.x = star.x
    star.rect.y = star.rect.height + 2 * star.rect.height * row_number
    stars.add(star)


def render_stars(settings, screen, stars):
    star = Star(settings, screen)
    number_stars_x = get_number_stars(settings, star.rect.width)
    number_rows = get_screen_rows(settings, star.rect.height)

    for row_number in range(number_rows):
        for star_number in range(number_stars_x):
            create_star(settings, screen, stars, star_number, row_number)


def create_fleet(settings, screen, ship, aliens):
    """ Instantiate full fleet of aliens."""

    # Create an alien and find the number of aliens in a row
    # Spacing between each alien is equal to one alien width
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    


    # Create the first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the rwo
            create_alien(settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(settings, aliens):
    """ Respond appropriately if any aliens have reached and edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    """ Drop the entire fleet and change the fleet's direction"""
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1