from pathlib import Path

import pygame


def load_image(name, directory: Path):
    return pygame.image.load(str(directory / f'{name}.png'))
