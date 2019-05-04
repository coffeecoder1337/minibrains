import pygame
import config
import menu
import player
import platforms
import json
import camera
import tmxreader
import helperspygame
import os
import ui
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
        self.ui = ui.Ui(self.screen)

        # --- objects ---
        self.all_objects = pygame.sprite.Group()
        self.platforms_group = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()

        # --- add objects ---
        self.renderer = helperspygame.RendererPygame()
        # --- text ---
        self.font_obj = pygame.font.Font(None, 25)

        self.total_x = 0
        self.total_y = 0

    def add(self, obj, x, y):
        nx, ny = self.camera.reverse((x, y))
        temp_obj = obj(nx, ny)
        self.all_objects.add(temp_obj)
        self.platforms_group.add(temp_obj)
        temp_obj.selected = True
        return temp_obj

    def check_win(self):
        if pygame.sprite.collide_rect(self.player, self.exit):
            if not self.is_last_level():
                self.next_level()
            else:
                self.draw_win()

    def reset(self):
        self.all_objects.empty()
        self.platforms_group.empty()
        self.spikes.empty()
        self.player.platform_count = 0
        self.player.life = 3

    def full_restart(self):
        self.reset()
        self.level_now = 1
        self.load_level()

    def draw_win(self):
        paused = True
        font_obj = pygame.font.Font(None, 25)
        text_surface_obj = font_obj.render('Вы выиграли. ESC - выход из игры, Enter - начать заново', True, (0, 0, 0))
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = config.center_of_screen
        while paused:
            for e in pygame.event.get():
                if e.type == QUIT:
                    paused = False
                    self.is_running = False
                if e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        paused = False
                        self.full_restart()
                    if e.key == K_ESCAPE:
                        paused = False
                        self.is_running = False
            self.screen.blit(text_surface_obj, text_rect_obj)
            pygame.display.update()
            self.clock.tick(60)

    def restart(self):
        self.player.rect.x = self.start_x
        self.player.rect.y = self.start_y - 64

    def is_last_level(self):
        if self.get_last_level() == self.level_now:
            return True
        return False

    def get_last_level(self):
        lst = [int(file.split('.')[0]) for file in os.listdir('levels')]
        if not lst:
            return 0
        return max(lst)

    def pause(self):
        paused = True
        font_obj = pygame.font.Font(None, 25)
        text_surface_obj = font_obj.render('Игра на пазуе. Нажмите Enter для продолжения...', True, (0, 0, 0))
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = config.center_of_screen
        while paused:
            for e in pygame.event.get():
                if e.type == QUIT:
                    paused = False
                    self.is_running = False
                if e.type == KEYDOWN:
                    if e.key == K_RETURN:
                        paused = False
            self.screen.blit(text_surface_obj, text_rect_obj)
            pygame.display.update()
            self.clock.tick(60)

    def next_level(self):
        self.reset()
        self.level_now += 1
        self.load_level()

    def chek_lose(self):
        if self.player.life < 1:
            self.full_restart()

    def check_hit(self):
        for object in self.platforms_group:
            nx, ny = self.camera.reverse(self.mouse)
            if (object.rect.x < nx < object.rect.right) and (object.rect.y < ny < object.rect.bottom):
                self.unselect()
                return object
        return False

    def unselect(self):
        for pl in self.platforms_group:
            pl.selected = False

    def move(self):
        for pl in self.platforms_group:
            if pl.selected:
                x, y = self.camera.reverse(self.mouse)
                pl.rect.centerx = x
                pl.rect.centery = y

    def check_selected(self):
        for pl in self.platforms_group:
            if pl.selected:
                return pl
        return False

    def handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.unselect()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3:
                    pl = self.check_hit()
                    if pl:
                        pl.kill()
                        self.player.platform_count -= 1

                if event.button == 1:
                    pl = self.check_hit()
                    if pl:
                        pl.selected = True

            if event.type == KEYDOWN:
                # --- pause ---
                if event.key == K_ESCAPE:
                    self.pause()

                # --- move ---
                if event.key in (K_a, K_LEFT):
                    self.player.direction = -1
                    self.player.left = True
                    self.player.right = False
                if event.key in (K_d, K_RIGHT):
                    self.player.direction = 1
                    self.player.right = True
                    self.player.left = False

                # --- place platform ---
                if event.key == K_e:

                    pl = self.check_selected()
                    if not pl:
                        if self.player.platform_count < self.player.max_platform_count:
                            self.add(platforms.UserPlatform, self.mouse[0], self.mouse[1])
                            self.player.platform_count += 1
                    else:
                        pl.kill()
                        self.player.platform_count -= 1

                # --- jump ---
                if event.key in (K_w, K_SPACE, K_UP):
                    self.player.up = True

            if event.type == KEYUP:

                # --- stop move ---
                if event.key in (K_a, K_LEFT):
                    if not self.player.right:
                        self.player.direction = 0
                    self.player.left = False

                if event.key in (K_d, K_RIGHT):
                    if not self.player.left:
                        self.player.direction = 0
                    self.player.right = False

                # --- stop jump ---
                if event.key in (K_w, K_SPACE, K_UP):
                    self.player.up = False

    def load_level(self):
        world_map = tmxreader.TileMapParser().parse_decode(f'levels/{self.level_now}.tmx')
        resources = helperspygame.ResourceLoaderPygame()
        resources.load(world_map)

        self.sprite_layers = helperspygame.get_layers_from_map(resources)

        platforms_layer = self.sprite_layers[0]
        spike_layer = self.sprite_layers[1]

        for row in range(0, platforms_layer.num_tiles_x):
            for col in range(0, platforms_layer.num_tiles_y):
                if platforms_layer.content2D[col][row] is not None:
                    p = platforms.Platform(row * 32, col * 32)
                    self.platforms_group.add(p)

                if spike_layer.content2D[col][row] is not None:
                    s = platforms.Spike(row * 32, col * 32)
                    self.spikes.add(s)
        exit_layer = self.sprite_layers[3]

        for exit in exit_layer.objects:
            try:
                x = exit.x
                y = exit.y
            except:
                pass
            else:
                self.exit = platforms.Exit(x, y)
                self.all_objects.add(self.exit)

        player_layer = self.sprite_layers[2]
        for pl in player_layer.objects:
            try:
                self.start_x = pl.x
                self.start_y = pl.y - 64
            except:
                pass
            else:
                self.player = player.Player(self.start_x, self.start_y)
                self.all_objects.add(self.player)

        self.total_x = platforms_layer.num_tiles_x * 32
        self.total_y = platforms_layer.num_tiles_y * 32
        self.camera = camera.Camera(self.camera_configure, self.total_x, self.total_y)

    def draw(self):
        self.mouse = pygame.mouse.get_pos()
        self.screen.fill(config.white)
        # self.all_objects.draw(self.screen)
        for sprite_layer in self.sprite_layers:
                if not sprite_layer.is_object_group:
                   self.renderer.render_layer(self.screen, sprite_layer)

        for a in self.all_objects:
            self.screen.blit(a.image, self.camera.apply(a))

        center_offset = self.camera.reverse(config.center_of_screen)
        self.renderer.set_camera_position_and_size(center_offset[0], center_offset[1], \
                                                  config.width, config.height, "center")
        if self.ui.visible:
            self.ui.loop(self.player.life)

    def camera_configure(self, camera, target_rect):
        l, t, _, _ = target_rect
        _, _, w, h = camera
        l, t = -l + config.width / 2, -t + config.height / 2

        l = min(0, l)
        l = max(-(camera.width - config.width), l)
        t = max(-(camera.height - config.height), t)
        t = min(0, t)

        return Rect(l, t, w, h)

    def check_player_collide(self):
        for s in self.spikes:
            if pygame.sprite.collide_rect(self.player, s):
                self.player.life -= 1
                self.restart()
    def run(self):
        renderer = helperspygame.RendererPygame()
        self.load_level()


        while self.is_running:
            self.handler()
            self.player.move(self.platforms_group, self.spikes)
            self.move()
            self.check_player_collide()
            self.chek_lose()
            self.check_win()
            self.camera.update(self.player)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

game = Game()

if __name__ == '__main__':
    game.run()
