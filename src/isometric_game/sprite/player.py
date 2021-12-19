import pygame
from pygame.math import Vector2

from isometric_game import STATIC_IMAGES_DIR
from isometric_game.constants import Action
from isometric_game.utils.asset import load_image
from isometric_game.utils.grid import (
    cartesian_to_isometric, cell_origin_coordinates, grid_to_isometric_coordinates,
)


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, grid_coordinates, location):
        super().__init__()

        self.location = location
        self.image_bottom_offset = 8
        self.image = load_image(STATIC_IMAGES_DIR / 'farmer.png')

        self.shift = Vector2(0, 0)
        # TODO maybe set in tile options
        player_image_offset = Vector2(0, self.image_bottom_offset)

        screen_coordinates = grid_to_isometric_coordinates(
            grid=grid_coordinates,
            cell_side=self.location.CELL_SIDE,
            shift=self.shift,
        )
        self.pos = screen_coordinates + player_image_offset
        self.last_pos = Vector2(self.pos)
        self.next_pos = Vector2(self.pos)
        self.walk_buffer = 50
        self.last_update = pygame.time.get_ticks()
        # speed must be even
        self.speed = 2
        self.direction = Vector2(0, 0)
        self.between_tiles = False

        self.rect = self.image.get_rect(midbottom=self.pos)

    def update(self, *, shift: Vector2):
        if self.shift != shift:
            delta = shift - self.shift
            self.shift = Vector2(shift)
            self.pos += delta
            self.last_pos += delta
            self.next_pos += delta

        self.get_inputs()
        if self.pos != self.next_pos:
            delta = self.next_pos - self.pos
            if delta.length() > cartesian_to_isometric(self.direction * self.speed).length():
                self.pos += cartesian_to_isometric(self.direction * self.speed)
            else:
                self.pos = Vector2(self.next_pos)
                self.direction = Vector2(0, 0)
                self.between_tiles = False

        self.rect.midbottom = self.pos

    def get_inputs(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if now - self.last_update > self.walk_buffer:
            self.last_update = now
            new_direction = Vector2(0, 0)
            if self.direction.y == 0:
                if Action.check(Action.PLAYER_LEFT, keys):
                    new_direction = Vector2(-1, 0)
                elif Action.check(Action.PLAYER_RIGHT, keys):
                    new_direction = Vector2(1, 0)
            if self.direction.x == 0:
                if Action.check(Action.PLAYER_UP, keys):
                    new_direction = Vector2(0, -1)
                elif Action.check(Action.PLAYER_DOWN, keys):
                    new_direction = Vector2(0, 1)

            if new_direction != Vector2(0, 0):
                self.direction = new_direction
                self.between_tiles = True

                self.last_pos = cell_origin_coordinates(
                    self.location.screen_to_world_coordinates(self.rect.midbottom),
                    cell_side=self.location.CELL_SIDE,
                ) + Vector2(0, self.image_bottom_offset)
                self.next_pos = (
                        self.last_pos
                        + cartesian_to_isometric(self.direction * self.location.CELL_SIDE)
                        + self.shift
                )
