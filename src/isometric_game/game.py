import sys

import pygame

from .location import Camera, Location


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(size=(900, 900))
        self.clock = pygame.time.Clock()
        self.camera = Camera()
        # TODO settings and injecting it to another classes

        # TODO make map format and read data from it
        #   choose level based on game state
        #   DI levels
        map = [['G' for _ in range(40)] for _ in range(40)]
        map[0][0] = 'GP'
        self.location = Location(
            map=map,
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
