import pygame
import config
from pygame.locals import *

pygame.init()


class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = config.width
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.image.fill(config.black)
        self.image.set_alpha(70)
