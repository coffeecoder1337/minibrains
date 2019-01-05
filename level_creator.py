import pygame
from pygame.locals import *
import menu
import player
import platforms
import config


class Creator:
    def __init__(self):
        pygame.display.set_caption("MiniBrains | Level Creator")

        # screen
        self.screen = pygame.display.set_mode(config.creator_size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.is_running = True

        # objects
        self.all_objects = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.menu = menu.Menu()

        # add objects
        self.all_objects.add(self.menu)

    def add(self):
        pass

    def remove(self):
        pass

    def move(self):
        pass

    def save_level(self):
        pass

    def load_level(self):
        pass

    def handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False

    def draw(self):
        self.screen.fill(config.white)
        self.all_objects.draw(self.screen)
        self.menu.items.draw(self.screen)

    def run(self):
        while self.is_running:
            self.handler()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)


creator = Creator()

if __name__ == '__main__':
    creator.run()
