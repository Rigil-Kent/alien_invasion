import pygame
from pygame.sprite import Sprite


class Star(Sprite):

    def __init__(self, settings, screen):
        super(Star, self).__init__()
        self.screen = screen
        self.settings = settings

        self.image = pygame.image.load('assets/mario-star-png-13.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def blitme(self):

        self.screen.blit(self.image, self.rect)