import pygame.font
from pygame.sprite import Group
from ship import Ship
from colors import Color



class Leaderboard():
    """ Report scoring information"""

    def __init__(self, settings, screen, stats):
        """ Initialize scorekeeping attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        self.text_color = Color.BLACK
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_controls()


    def prep_controls(self):
        """ Show controls to user"""

        controls = ["Ctrl + R : Restart", "Ctrl + Q or ESC: Quit", "P: Play", "<-- or A: Move Ship Left", "--> or D: Move Ship Right", "SPACE: Fire projectile"]
        self.controls_imgs = []
        self.controls_rects = []
        for index, control_str  in enumerate(controls):
            self.controls_imgs.append(self.font.render(str(control_str), True, self.text_color, self.settings.default_bg_color))
            self.controls_rects.append(self.controls_imgs[index].get_rect())

            self.controls_rects[index].centerx = self.screen_rect.centerx
            self.controls_rects[index].top = self.controls_rects[index].height * index + 500



    def prep_score(self):
        """ Render the score into an image"""
        
        rounded_score = int(round(self.stats.score, -1))
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.default_bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        """ Turn the high score into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High Score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.default_bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        """ Turn the level into a rendered image."""
        self.level_image = self.font.render("Level " + str(self.stats.level), True, self.text_color, self.settings.default_bg_color)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left
        self.level_rect.top = self.score_rect.top

    def prep_ships(self):
        """ Show how many ships are left"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 140 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def show_score(self):
        """ Draw the score to the screen"""

        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def show_controls(self):

        for index, control in enumerate(self.controls_imgs):
            self.screen.blit(control, self.controls_rects[index])