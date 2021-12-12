from pygame.math import Vector2

from .math import round_half_up


def cartesian_to_isometric(cartesian):
    """
    Convert cartesian coordinates to isometric
    https://www.youtube.com/watch?v=KvSjJ-kdGio
    """
    x, y = tuple(cartesian)
    return Vector2(
        x - y,
        (x + y) / 2
    )


def isometric_to_cartesian(isometric):
    """
    Convert isometric coordinates to cartesian
    https://www.youtube.com/watch?v=KvSjJ-kdGio
    """
    x, y = tuple(isometric)
    converted = Vector2((x + y * 2) / 2, 0)
    converted.y = -x + converted.x
    return converted


def isometric_to_grid_coordinates(isometric, cell_side, camera_shift, tile_shift=(0, 0)):
    pos = isometric + Vector2(tile_shift)
    x, y = isometric_to_cartesian(pos - camera_shift)
    return round_half_up(x / cell_side) - 1, round_half_up(y / cell_side)


def grid_to_isometric_coordinates(grid, cell_side, camera_shift):
    screen = cartesian_to_isometric(Vector2(grid) * cell_side)
    return screen + camera_shift


def cell_origin_coordinates(isometric, cell_side, camera_shift, tile_shift=(0, 0)):
    """
    Get cell origin (topleft, midbottom, etc.) coordinates by any coordinates in that cell.

    Simply convert screen coordinates to cell and back.
    """
    grid = isometric_to_grid_coordinates(
        isometric,
        cell_side,
        camera_shift,
        tile_shift
    )
    return grid_to_isometric_coordinates(grid, cell_side, camera_shift=(0, 0))
