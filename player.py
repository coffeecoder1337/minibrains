import pygame
import images
import pyganim
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
        self.selected = False

        self.right = False
        self.left = False

        self.jump_power = 10
        self.gravity = 0.3
        self.direction = 0
        self.up = False
        self.on_ground = False

        self.image.set_colorkey(Color('#000000'))

        ANIMATION_DELAY = 100
        anim = []
        for a in images.run_right:
            anim.append((a, ANIMATION_DELAY))
        self.anim_right = pyganim.PygAnimation(anim)
        self.anim_right.play()

        # anim = []
        # for a in images.idle:
        #     anim.append((a, ANIMATION_DELAY))
        # self.idle = pyganim.PygAnimation(anim)
        # self.idle.play()
        # self.idle.blit(self.image, (0, 0))

    def move(self, platforms):
        self.update()
        if self.up:
            if self.on_ground:
                self.speed_y = -self.jump_power

        if not self.on_ground:
            self.speed_y += self.gravity

        self.on_ground = False

        self.rect.y += self.speed_y
        self.collide(0, self.speed_y, platforms)
        self.rect.x += (self.speed * self.direction)
        self.collide(self.speed * self.direction, 0, platforms)

    def collide(self, speed_x, speed_y, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):
                if speed_x > 0:
                    self.rect.right = p.rect.left
                if speed_x < 0:
                    self.rect.left = p.rect.right

                if speed_y > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.speed_y = 0
                if speed_y < 0:
                    self.rect.top = p.rect.bottom
                    self.speed_y = 0
    
    def update(self):
        if self.right:
            self.image.fill(Color('#ffffff'))
            if self.up:
                pass
            else:
                self.anim_right.blit(self.image, (0, 0))
