import sys

import pygame

from . import MAPS_DIR
from .location import Camera, Location
from .utils import map


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(size=(900, 900))
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        # TODO settings and injecting it to another classes

        map_reader = map.Reader('test_level.json', MAPS_DIR)
        self.location = Location(
            reader=map_reader,
            display=self.display,
            camera=self.camera,
        )

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    print(event.key, event.unicode)

            self.location.update()

            pygame.display.update()
            self.clock.tick(60)
