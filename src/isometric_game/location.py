from typing import Protocol, Tuple

import pygame
from pygame.math import Vector2

from .constants import Action, CAMERA_SPEED
from .sprite.player import PlayerSprite
from .sprite.tile import TileSprite
from .utils import map
from .utils.grid import isometric_to_grid_coordinates


class MapReader(Protocol):
    def read(self) -> map.Map:
        pass


class Location:
    CELL_WIDTH: int
    CELL_HEIGHT: int
    CELL_SIDE: int  # Cartesian cell width
    CELL_CENTER: Tuple[int, int]

    def __init__(self, reader: MapReader, display, camera):
        self.reader = reader
        self.map = None
        self.display = display
        self.camera = camera

        self.player = pygame.sprite.GroupSingle()
        self.sprite_groups = []

        self.build()

    def build(self):
        """
        Build map
        """
        self.map = self.reader.read()
        self.CELL_WIDTH = self.map.tile_width
        self.CELL_HEIGHT = int(self.CELL_WIDTH / 2)
        self.CELL_SIDE = int(self.CELL_WIDTH / 2)  # Cartesian cell width
        self.CELL_CENTER = (int(self.CELL_WIDTH / 2), int(self.CELL_HEIGHT / 2))

        groups = []
        for layer in self.map.layers:
            group = pygame.sprite.Group()
            for i, tile_id in enumerate(layer.data):
                if tile_id:
                    x = i % layer.height
                    y = i // layer.width
                    tile = self.map.tile_mapping[tile_id]
                    tile_sprite = TileSprite(
                        grid_coordinates=(x, y),
                        tile=tile,
                        cell_side=self.CELL_SIDE,
                        alignment=layer.alignment
                    )
                    group.add(tile_sprite)
            groups.append(group)

        player_sprite = PlayerSprite(grid_coordinates=(0, 0), location=self)
        self.player.add(player_sprite)
        groups.insert(1, self.player)  # insert player after ground layer
        self.sprite_groups = groups

    def update(self):
        self.display.fill(self.map.background_color)
        self.get_inputs()
        self.camera.update()

        for group in self.sprite_groups:
            group.update(shift=self.camera.shift)
            # TODO drawing order is important
            group.draw(self.display)

    def get_inputs(self):
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            print(
                isometric_to_grid_coordinates(
                    self.get_coordinates_under_cursor(),
                    cell_side=self.CELL_SIDE,
                )
            )

    def get_coordinates_under_cursor(self):
        return self.screen_to_world_coordinates(pygame.mouse.get_pos())

    def screen_to_world_coordinates(self, isometric):
        """
        Calculate "world" isometric coordinates
        """
        return isometric + Vector2(self.CELL_CENTER) - self.camera.shift


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
