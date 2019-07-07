import pygame
from pygame.sprite import Sprite


class Projectile(Sprite):
    """ Manage projectiles fired from ship or actor"""

    def __init__(self, settings, screen, ship):
        """ Create a projectile object at the ship's current position"""
        super(Projectile, self).__init__()
        self.screen = screen

        # Create a projectile rect at (0, 0) and set correct position
        self.rect = pygame.Rect(0, 0, settings.projectile_width, settings.projectile_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the projectile's position as a decimal value
        self.y = float(self.rect.y)

        self.color = settings.projectile_color
        self.speed_factor = settings.projectile_speed_factor


    def update(self):
        """ Move the projectile up the screen."""

        # Update the decimal position of the projectile
        self.y -= self.speed_factor

        # Update the rect position
        self.rect.y = self.y



    def draw(self):
        """ Draw the projectile to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)