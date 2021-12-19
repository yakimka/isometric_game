import pygame
from pygame import Vector2

from isometric_game import constants
from isometric_game.utils import map
from isometric_game.utils.grid import grid_to_isometric_coordinates


# TODO добавить файл с параметрами тайла
#   проходимый он или нет
#   приоритет (очередность) отрисовки
#   офсеты отрисовки (например у картинки игрока центр позиционирования должен приходиться на пятки,
#   а не на низ картинки)
#   анимация это или статический тайл
class TileSprite(pygame.sprite.Sprite):
    def __init__(self, *groups, grid_coordinates, tile: map.Tile, cell_side: int, alignment='midtop'):
        if alignment not in ['midtop', 'midbottom']:
            raise ValueError(f'alignment passed: {alignment}. Supports: midtop, midbottom')

        super().__init__(*groups)

        self.image = tile.surface
        self.shift = Vector2(0, 0)
        self.cell_side = cell_side
        self.alignment = alignment

        screen_coordinates = grid_to_isometric_coordinates(
            grid_coordinates,
            cell_side=self.cell_side,
            shift=self.shift
        )

        cell_top_offset = Vector2(0, int(self.cell_side / 2))  # y center of tile
        if alignment == 'midbottom':
            cell_top_offset.y *= -1

        kwargs = {self.alignment: screen_coordinates - cell_top_offset}
        self.rect = self.image.get_rect(**kwargs)

    def update(self, *, shift: Vector2):
        if self.shift != shift:
            delta = shift - self.shift
            # self.rect.midtop += delta
            setattr(self.rect, self.alignment, getattr(self.rect, self.alignment) + delta)
            self.shift = Vector2(shift)
