from typing import Protocol

import pygame
from pygame.math import Vector2

from .constants import Action, CAMERA_SPEED, CELL_CENTER, CELL_SIDE
from .sprite.player import PlayerSprite
from .sprite.tile import TileSprite
from .utils import map
from .utils.grid import isometric_to_grid_coordinates


class MapReader(Protocol):
    def read(self) -> map.Map:
        pass


class Location:
    def __init__(self, reader: MapReader, display, camera):
        self.reader = reader
        self.map = None
        self.display = display
        self.camera = camera

        self.player = pygame.sprite.GroupSingle()
        self.all_sprites = pygame.sprite.Group()

        self.build()

    def build(self):
        """
        Method for precache map etc.
        """
        self.map = self.reader.read()

        for layer in self.map.layers:
            for i, tile_id in enumerate(layer.data):
                if tile_id:
                    x = i % layer.height
                    y = i // layer.width
                    tile_ = self.map.tile_mapping[tile_id]
                    tile = TileSprite(grid_coordinates=(x, y), surface=tile_.surface)
                    self.all_sprites.add(tile)
            break

        player_sprite = PlayerSprite(grid_coordinates=(0, 0), location=self)
        self.player.add(player_sprite)
        self.all_sprites.add(player_sprite)

    def update(self):
        self.display.fill(self.map.background_color)
        self.get_inputs()
        self.camera.update()

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
