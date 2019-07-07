from colors import Color

class Config(object):
    def __init__(self):
        self.default_screen_height = 800
        self.default_screen_width = 1200
        self.default_size = (self.default_screen_width, self.default_screen_height)
        self.default_name = "Alien Invasion"
        self.default_bg_color = Color.GRAY
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Projectile settings
        self.projectile_speed_factor = 2
        self.projectile_width = 3
        self.projectile_height = 15
        self.projectile_color = Color.RED
        self.projectile_limit = 3

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """ Initialize settings that change throughout the game."""
        self.ship_speed_factor = 1.5
        self.projectile_speed_factor = 2
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 10


    def increase_speed(self):
        """ Increase speed settings"""
        self.ship_speed_factor *= self.speedup_scale
        self.projectile_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)


    def change_default_screen_height(height):
        self.default_screen_height = height

    def change_default_screen_width(width):
        self.default_screen_width = width

    def change_default_bg_color(Color):
        self.default_bg_color = Color

    def change_default_name(name):
        self.default_name = name