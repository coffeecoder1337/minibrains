import pygame
import images
from pygame.locals import *

class Ui:
    def __init__(self, rect):
        self.visible = True
        self.rect = rect
        self.x_gutter = 30
        self.y_gutter = 30
    
    def draw_health(self, life):
        offset = 2
        for x in range(offset, life + offset):
            rect = images.health.get_rect(topleft = (self.x_gutter * x, self.y_gutter))
            self.rect.blit(images.health, rect)

    def draw_head(self):
        rect = images.head.get_rect(topleft = (10, 20))
        self.rect.blit(images.head, rect)

    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = True

    def draw(self, life):
        self.draw_health(life)
        self.draw_head()
    
    def handle(self):
        pass
    
    def loop(self, life):
        self.handle()
        self.draw(life)
