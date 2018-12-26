import pygame
import config
import menu
import player
import platforms
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        pygame.display.set_icon(pygame.image.load('robot.png'))
        pygame.display.set_caption('MiniBrains')

        # screen
        self.screen = pygame.display.set_mode(config.size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.is_running = True

        # objects
        self.all_objects = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.menu = menu.Menu()
        self.temp = platforms.Platform(100, 300)
        self.player = player.Player(100, 100)

        # add objects
        self.all_objects.add(self.menu)
        self.all_objects.add(self.player)
        self.platforms_group.add(self.temp)
        self.all_objects.add(self.temp)

    def handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False

            if event.type == KEYDOWN:

                # --- move ---
                if event.key in (K_a, K_LEFT):
                    self.player.direction = -1
                if event.key in (K_d, K_RIGHT):
                    self.player.direction = 1

                # --- jump ---
                if event.key in (K_w, K_SPACE, K_UP):
                    self.player.up = True

            if event.type == KEYUP:

                # --- stop move ---
                if event.key in (K_a, K_LEFT, K_d, K_RIGHT):
                    self.player.direction = 0

                # --- stop jump ---
                if event.key in (K_w, K_SPACE, K_UP):
                    self.player.up = False

    def draw(self):
        self.screen.fill(config.white)
        self.all_objects.draw(self.screen)
        self.menu.items.draw(self.menu.image)

    def run(self):
        while self.is_running:
            self.handler()
            self.player.move(self.platforms_group)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

game = Game()

if __name__ == '__main__':
    game.run()
