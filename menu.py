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
            x = self.items.sprites()[-1].rect.x + 40 + self.item_gutter # 1 слагаемое - х координата последнего элемента меню, 2 - ширина элемента меню, 3 - отступ между элементами
        except:
            x = 40
        item = MenuItem(x)
        self.items.add(item)
