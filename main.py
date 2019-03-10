import pygame
import config
import menu
import player
import platforms
import json
import camera
import tmxreader
import helperspygame
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        pygame.display.set_icon(pygame.image.load('robot.png'))
        pygame.display.set_caption('MiniBrains')

        # --- level ---
        self.level_now = 1

        # --- screen ---
        self.screen = pygame.display.set_mode(config.size)
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.is_running = True

        # --- objects ---
        self.all_objects = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.menu = menu.Menu()
        self.player = player.Player(100, 100)

        # --- add objects ---
        self.all_objects.add(self.menu)
        self.all_objects.add(self.player)

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

    def load_level(self):
        with open(f'levels/{self.level_now}.json', 'r') as f:
            data = json.load(f)
        for platform in data['platforms']:
            p = platforms.Platform(platform['x'], platform['y'])
            self.platforms_group.add(p)
            self.all_objects.add(p)

    def draw(self):
        self.screen.fill(config.white)
        # self.all_objects.draw(self.screen)
        for a in self.all_objects:
            if not a.fixed:
                self.screen.blit(a.image, self.camera.apply(a))
        self.menu.items.draw(self.menu.image)

    def camera_configure(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + config.width / 2, -t + config.height / 2

        l = min(0, l)
        l = max(-(camera.width - config.width), l)
        t = max(-(camera.height - config.height), t)
        t = min(0, t)

        return Rect(l, t, w, h) 

    def run(self):
        # total_level_width  = len(level[0]) * config.width
        total_level_width = 2400
        # total_level_height = len(level) * config.height
        total_level_height = 600
        
        self.camera = camera.Camera(self.camera_configure, total_level_width, total_level_height)
        self.load_level()
        while self.is_running:
            self.handler()
            self.player.move(self.platforms_group)
            self.camera.update(self.player)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

game = Game()

if __name__ == '__main__':
    game.run()
