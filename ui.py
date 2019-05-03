import pygame
import images
from pygame.locals import *

class Ui:
    def __init__(self, rect):
        self.visible = True
        self.rect = rect
    
    def draw_health(self, life):
        for x in range(2, life + 2):
            rect = images.health.get_rect(topleft = (30 * x, 30))
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
