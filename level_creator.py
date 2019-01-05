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

    def select(self):
        for object in self.all_objects:
            if (object.rect.x < self.mouse[0] < object.rect.right) and (object.rect.y < self.mouse[1] < object.rect.bottom):
                try:
                    object.selected = not object.selected
                except:
                    pass
                return object
        return None

    def move(self):
        for obj in self.all_objects:
            try:
                if obj.selected:
                    obj.rect.centerx = self.mouse[0]
                    obj.rect.centery = self.mouse[1]
            except:
                pass

    def save_level(self):
        pass

    def load_level(self):
        pass

    def handler(self):
        for event in pygame.event.get():
            self.mouse = pygame.mouse.get_pos()

            if event.type == QUIT:
                self.is_running = False

            if event.type == MOUSEBUTTONDOWN:
                self.selected_object = self.select()


            if event.type == KEYDOWN:
                if event.key == K_DELETE:
                    self.selected_object.kill()
                if event.key == K_t:
                    self.add(platforms.Platform, self.mouse[0], self.mouse[1], 'platforms')

    def draw(self):
        self.screen.fill(config.white)
        self.all_objects.draw(self.screen)
        self.menu.items.draw(self.screen)

    def run(self):
        while self.is_running:
            self.handler()
            self.move()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)


creator = Creator()

if __name__ == '__main__':
    creator.run()
