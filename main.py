import pygame
import config
import menu
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        pygame.display.set_icon(pygame.image.load('robot.png'))
        pygame.display.set_caption('MiniBrains')

        self.screen = pygame.display.set_mode(config.size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.all_objects = pygame.sprite.Group()
        self.menu = menu.Menu()

        self.all_objects.add(self.menu)

    def handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False

    def draw(self):
        self.screen.fill(config.white)
        self.all_objects.draw(self.screen)
        self.menu.items.draw(self.menu.image)

    def run(self):
        while self.is_running:
            self.handler()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

game = Game()

if __name__ == '__main__':
    game.run()
