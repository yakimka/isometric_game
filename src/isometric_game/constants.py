from enum import Enum

import pygame

CELL_WIDTH = 128
CELL_HEIGHT = int(CELL_WIDTH / 2)
CELL_SIDE = 64  # Cartesian cell width
CELL_CENTER_FROM_TOP = int(CELL_SIDE / 2)
TILE_WIDTH = CELL_WIDTH
TILE_HEIGHT = TILE_WIDTH

K_ц = 1094
K_ы = 1099
K_ф = 1092
K_в = 1074


class Action(Enum):
    CAMERA_UP = [pygame.K_w, K_ц]
    CAMERA_DOWN = [pygame.K_s, K_ы]
    CAMERA_LEFT = [pygame.K_a, K_ф]
    CAMERA_RIGHT = [pygame.K_d, K_в]

    PLAYER_UP = [pygame.K_UP]
    PLAYER_DOWN = [pygame.K_DOWN]
    PLAYER_LEFT = [pygame.K_LEFT]
    PLAYER_RIGHT = [pygame.K_RIGHT]

    @classmethod
    def check(cls, action, keys):
        return any(keys[key] for key in action.value)


CAMERA_SPEED = 10
