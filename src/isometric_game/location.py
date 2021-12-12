import pygame
from pygame.math import Vector2

from . import STATIC_IMAGES_DIR
from .constants import Action, CAMERA_SPEED, CELL_SIDE
from .sprite.player import PlayerSprite
from .utils.asset import load_image
from .utils.grid import cartesian_to_isometric, isometric_to_cartesian
from .utils.math import round_half_up


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
        grass_img = load_image('grass', STATIC_IMAGES_DIR).convert_alpha()
        self.tiles_database['G'] = grass_img

    def build(self):
        """
        Method for precache map etc.
        """

    def update(self):
        # TODO get color from map
        self.display.fill((0, 0, 0))
        self.get_inputs()
        self.camera.update()

        for x, row in enumerate(self.map):
            for y, tile_sign in enumerate(row):
                if tile_sign[0] in self.tiles_database:
                    tile = self.tiles_database[tile_sign[0]]
                    pos = cartesian_to_isometric((Vector2(x, y) * CELL_SIDE) - Vector2(10, 10))
                    self.display.blit(tile, self.camera.shift + pos)
                if tile_sign[-1] == 'P' and self.player.sprite is None:
                    player_sprite = PlayerSprite(grid_coordinates=(x, y))
                    self.player.add(player_sprite)

        self.player.update(shift=self.camera.shift)
        self.player.draw(self.display)

    def get_inputs(self):
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            pos = pygame.mouse.get_pos()
            pos = isometric_to_cartesian(pos - self.camera.shift)
            print(round_half_up(pos[0] / CELL_SIDE) - 1, round_half_up(pos[1] / CELL_SIDE))


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
