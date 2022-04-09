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


def load_cut_image(path: Path, x, y, w, h, convert=True):
    image = load_image(path, convert)
    return image.subsurface((x, y, w, h))
