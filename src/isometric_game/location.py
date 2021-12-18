import pygame
from pygame.math import Vector2

from . import STATIC_IMAGES_DIR
from .constants import Action, CAMERA_SPEED, CELL_SIDE, CELL_CENTER
from .sprite.player import PlayerSprite
from .sprite.tile import TileSprite
from .utils.asset import load_image
from .utils.grid import isometric_to_cartesian, isometric_to_grid_coordinates


class Location:
    def __init__(self, map, display, camera):
        self.map = map
        self.display = display
        self.camera = camera

        self.tiles_database = {}
        self.load_tiles_database()

        self.player = pygame.sprite.GroupSingle()
        self.all_sprites = pygame.sprite.Group()

        self.build()

    def load_tiles_database(self):
        # TODO load all resources for map
        #   resource must be with additional information
        grass_img = load_image('grass2', STATIC_IMAGES_DIR).convert_alpha()
        self.tiles_database['G'] = grass_img

    def build(self):
        """
        Method for precache map etc.
        """
        self.builded = False

    def update(self):
        # TODO get color from map
        self.display.fill((0, 0, 0))
        self.get_inputs()
        self.camera.update()

        # TODO refactor
        if not self.builded:
            for x, row in enumerate(self.map):
                for y, tile_sign in enumerate(row):
                    # if tile_sign[0] in self.tiles_database:
                    #     tile = self.tiles_database[tile_sign[0]]
                    #     pos = cartesian_to_isometric((Vector2(x, y) * CELL_SIDE) - Vector2(10, 10))
                    #     self.display.blit(tile, self.camera.shift + pos)
                    if tile_sign[0] in self.tiles_database:
                        tile = TileSprite(grid_coordinates=(x, y), name='grass2')
                        self.all_sprites.add(tile)
                    if tile_sign[-1] == 'P' and self.player.sprite is None:
                        player_sprite = PlayerSprite(grid_coordinates=(x, y), location=self)
                        self.player.add(player_sprite)
                        self.all_sprites.add(player_sprite)
            self.builded = True

        self.all_sprites.update(shift=self.camera.shift)
        self.all_sprites.draw(self.display)
        self.player.draw(self.display)

    def get_inputs(self):
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            print(
                isometric_to_grid_coordinates(
                    self.get_coordinates_under_cursor(),
                    cell_side=CELL_SIDE,
                )
            )

    def get_coordinates_under_cursor(self):
        return self.screen_to_world_coordinates(pygame.mouse.get_pos())

    def screen_to_world_coordinates(self, isometric):
        """
        Calculate "world" isometric coordinates
        """
        return isometric + Vector2(CELL_CENTER) - self.camera.shift


class Camera:
    def __init__(self, shift=(0, 0)):
        self.shift = Vector2(shift)

    def update(self):
        self.get_inputs()

    def get_inputs(self):
        keys = pygame.key.get_pressed()
        if Action.check(Action.CAMERA_UP, keys):
            self.shift.y += CAMERA_SPEED
        if Action.check(Action.CAMERA_DOWN, keys):
            self.shift.y += -CAMERA_SPEED
        if Action.check(Action.CAMERA_LEFT, keys):
            self.shift.x += CAMERA_SPEED
        if Action.check(Action.CAMERA_RIGHT, keys):
            self.shift.x += -CAMERA_SPEED
