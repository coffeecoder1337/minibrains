import pygame
from pygame.locals import *
import config


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((32, 64))
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0))
        self.start_x = x
        self.start_y = y
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.speed = 5
        self.speed_y = 2

        self.jump_power = 10
        self.gravity = 0.3
        self.direction = 0
        self.up = False
        self.on_ground = False

    def move(self):
        self.rect.x += (self.speed * self.direction)
        if not self.on_ground:
            self.speed_y += self.gravity
            self.rect.y += self.speed_y
