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

    def add(self, obj, x, y, state = None):
        temp_obj = obj(x, y)
        self.all_objects.add(temp_obj)
        if state == 'platform':
            self.platforms_group.add(temp_obj)

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
            mouse = pygame.mouse.get_pos()

            if event.type == QUIT:
                self.is_running = False

            if event.type == KEYDOWN:
                if event.key == K_t:
                    self.add(platforms.Platform, mouse[0], mouse[1], 'platform')

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
