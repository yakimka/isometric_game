import pygame
from pygame.math import Vector2

from isometric_game import constants, STATIC_IMAGES_DIR
from isometric_game.constants import Action, CELL_SIDE
from isometric_game.utils.asset import load_image
from isometric_game.utils.grid import cartesian_to_isometric, isometric_to_cartesian


class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, grid_coordinates):
        super().__init__()

        self.image_bottom_offset = 8
        self.image = load_image('farmer', STATIC_IMAGES_DIR).convert_alpha()

        pos = cartesian_to_isometric(Vector2(grid_coordinates) * constants.CELL_WIDTH)
        cell_top_offset = Vector2(0, constants.CELL_CENTER_FROM_TOP)
        # TODO maybe set in tile options
        player_image_offset = Vector2(0, self.image_bottom_offset)

        self.pos = pos + cell_top_offset + player_image_offset
        self.last_pos = Vector2(self.pos)
        self.next_pos = Vector2(self.pos)
        self.walk_buffer = 50
        self.last_update = pygame.time.get_ticks()
        # speed must be even
        self.speed = 2
        self.direction = Vector2(0, 0)
        self.between_tiles = False

        self.rect = self.image.get_rect(bottomleft=self.pos)
        self.shift = Vector2(0, 0)

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

        self.rect.bottomleft = self.pos

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
                cart = isometric_to_cartesian(self.rect.bottomleft - self.shift)
                current_index = cart.x // CELL_SIDE, cart.y // CELL_SIDE
                self.last_pos = cartesian_to_isometric(
                    Vector2(current_index) * CELL_SIDE
                ) + Vector2(0, 42)
                self.next_pos = self.last_pos + cartesian_to_isometric(self.direction * CELL_SIDE) + self.shift
