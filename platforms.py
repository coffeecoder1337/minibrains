import pygame
from pygame.locals import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))
        self.rect.x = x
        self.rect.y = y