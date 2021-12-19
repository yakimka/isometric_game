import pygame
from pygame import Vector2

from isometric_game import constants
from isometric_game.utils.grid import grid_to_isometric_coordinates


# TODO добавить файл с параметрами тайла
#   проходимый он или нет
#   приоритет (очередность) отрисовки
#   офсеты отрисовки (например у картинки игрока центр позиционирования должен приходиться на пятки,
#   а не на низ картинки)
#   анимация это или статический тайл
class TileSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, grid_coordinates, surface):
        super().__init__(*groups)

        self.image = surface
        self.shift = Vector2(0, 0)

        screen_coordinates = grid_to_isometric_coordinates(
            grid_coordinates,
            cell_side=constants.CELL_SIDE,
            shift=self.shift
        )
        _, y = constants.CELL_CENTER
        cell_top_offset = Vector2(0, y)
        self.rect = self.image.get_rect(midtop=screen_coordinates - cell_top_offset)

    def update(self, *, shift: Vector2):
        if self.shift != shift:
            delta = shift - self.shift
            self.rect.midtop += delta
            self.shift = Vector2(shift)
