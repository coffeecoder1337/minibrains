import pygame
import config
from pygame.locals import *

pygame.init()

class MenuItem(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.width = 40
        self.height = 40
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 10
        self.image.fill(config.white)

class Menu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = config.width
        self.height = 60
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.image.fill(config.black)
        self.image.set_alpha(70)
        self.items = pygame.sprite.Group()
        self.item_gutter = 10

    def add_item(self):
        try:
            last_item = self.items.sprites()[-1]
            x = last_item.rect.x + last_item.width + self.item_gutter
        except:
            x = 40
        item = MenuItem(x)
        self.items.add(item)
