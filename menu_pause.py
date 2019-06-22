    # def pause(self):
    #     paused = True
    #     font_obj = pygame.font.Font(None, 25)
    #     text_surface_obj = font_obj.render('Игра на пазуе. Нажмите Enter для продолжения...', True, (0, 0, 0))
    #     text_rect_obj = text_surface_obj.get_rect()
    #     text_rect_obj.center = config.center_of_screen
    #     while paused:
    #         for e in pygame.event.get():
    #             if e.type == QUIT:
    #                 paused = False
    #                 self.is_running = False
    #             if e.type == KEYDOWN:
    #                 if e.key == K_RETURN:
    #                     paused = False
    #         self.screen.blit(text_surface_obj, text_rect_obj)
    #         pygame.display.update()
    #         self.clock.tick(60)

import pygame
import buttons
from pygame.locals import *

class Pause(pygame.sprite.Sprite):
    def __init__(self, screen, all_objects):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.width = 300
        self.height = 400
        self.image = pygame.Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center
        self.image.fill((119, 69, 235))
        self.paused = False
        self.clock = pygame.time.Clock()
        self.all_objects = all_objects
        self.buttons = pygame.sprite.Group()
        self.esc_btn = buttons.BaseButton((30, 30), (self.rect.width - 30, 0), (0, 0, 0), on_release=self.hide)
        self.buttons.add(self.esc_btn)
    
    def show(self):
        self.all_objects.add(self)
        self.paused = True
        self.run()
    
    def hide(self):
        self.all_objects.remove(self)
        self.paused = False

    def get_relative_mouse(self):
        return (self.mouse[0] - self.rect.x, self.mouse[1] - self.rect.y)
    
    def run(self):
        while self.paused:
            self.mouse = pygame.mouse.get_pos()
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        self.hide()
                if e.type == MOUSEBUTTONUP:
                    if e.button == 1:
                        self.esc_btn.check_release(self.get_relative_mouse())

            pygame.display.update()
            self.buttons.draw(self.image)
            self.all_objects.draw(self.screen)
            self.clock.tick(60)

