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
        # self.all_objects.add(self.menu)
        self.renderer = helperspygame.RendererPygame()
        self.all_objects.add(self.player)

        self.total_x = 0
        self.total_y = 0

    def add(self, obj, x, y):
        nx, ny = self.camera.reverse((x, y))
        temp_obj = obj(nx, ny)
        self.all_objects.add(temp_obj)
        self.platforms_group.add(temp_obj)
        temp_obj.selected = True
        return temp_obj

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

                # --- move ---
                if event.key in (K_a, K_LEFT):
                    self.player.direction = -1
                    self.player.left = True
                if event.key in (K_d, K_RIGHT):
                    self.player.direction = 1
                    self.player.right = True

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
                if event.key in (K_a, K_LEFT, K_d, K_RIGHT):
                    self.player.direction = 0
                    self.player.left = False
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
        
        for row in range(0, platforms_layer.num_tiles_x):
            for col in range(0, platforms_layer.num_tiles_y):
                if platforms_layer.content2D[col][row] is not None:
                    p = platforms.Platform(row * 32, col * 32)
                    self.platforms_group.add(p)
        self.total_x = platforms_layer.num_tiles_x * 32
        self.total_y = platforms_layer.num_tiles_y * 32

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
 
        # self.menu.items.draw(self.menu.image)

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
        renderer = helperspygame.RendererPygame()
        self.load_level()
        self.camera = camera.Camera(self.camera_configure, self.total_x, self.total_y)
        
        while self.is_running:
            self.handler()
            self.player.move(self.platforms_group)
            self.move()
            self.camera.update(self.player)
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

game = Game()

if __name__ == '__main__':
    game.run()
