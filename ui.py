import pygame
from pygame.locals import *

class Ui:
    def __init__(self):
        self.visible = True
    
    def show(self):
        self.visible = True
        while self.visible:
            self.loop()
    
    def hide(self):
        self.visible = True

    def draw(self):
        pass
    
    def handle(self):
        pass
    
    def loop(self):
        self.handle()
        self.draw()
