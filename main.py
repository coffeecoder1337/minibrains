import pygame
import config
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode(config.size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.is_running = True

    def handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False

    def draw(self):
        self.screen.fill(config.white)

    def run(self):
        while self.is_running:
            self.handler()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)

game = Game()

if __name__ == '__main__':
    game.run()
