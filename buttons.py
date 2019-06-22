import pygame
from pygame.locals import *


class BaseButton(pygame.sprite.Sprite):
    def __init__(self, size, coords, color, on_press = None, on_release = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.on_press = on_press
        self.on_release = on_release
        self.image.fill(color)

    def _check(self, mouse):
        if (self.rect.x < mouse[0] < self.rect.right) and (self.rect.y < mouse[1] < self.rect.bottom):
            return True
        return False
    
    def check_press(self, mouse):
        if self._check(mouse):
            self.on_press()

    def check_release(self, mouse):
        if self._check(mouse):
            self.on_release()