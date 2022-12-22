from functools import lru_cache
from pathlib import Path

import pygame


# libpng warning: iCCP: known incorrect sRGB profile
# mogrify some.png
# https://stackoverflow.com/a/22747902
@lru_cache(512)
def load_image(path: Path, convert=True):
    image = pygame.image.load(str(path))
    if convert:
        image = image.convert_alpha()
    return image


@lru_cache(512)
def load_cut_images(path, tile_width, tile_height, convert=True) -> tuple:
    surface = pygame.image.load(str(path))
    if convert:
        surface = surface.convert_alpha()

    tile_num_x = surface.get_width() // tile_width
    tile_num_y = surface.get_height() // tile_height

    tiles = []
    for row in range(tile_num_y):
        tiles.extend(
            surface.subsurface(
                (col * tile_width, row * tile_height, tile_width, tile_height)
            )
            for col in range(tile_num_x)
        )

    return tuple(tiles)
