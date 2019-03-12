import pygame
import images
from pygame.locals import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 32))
        # self.image = images.images['ground']
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))
        self.rect.x = x
        self.rect.y = y
        self.selected = False
        self.fixed = True

class UserPlatform(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = images.user_block
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.spike
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = images.exit
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y