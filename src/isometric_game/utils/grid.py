from pygame.math import Vector2


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
