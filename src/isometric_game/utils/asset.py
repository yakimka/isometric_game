from functools import lru_cache
from pathlib import Path

import pygame


# libpng warning: iCCP: known incorrect sRGB profile
# mogrify some.png
# https://stackoverflow.com/a/22747902
@lru_cache(512)
def load_image(name, directory: Path, convert=True):
    image = pygame.image.load(str(directory / f'{name}.png'))
    if convert:
        image = image.convert_alpha()
    return image
