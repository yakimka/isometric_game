import math as m


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    result = m.floor(n * multiplier + 0.5) / multiplier
    if decimals == 0:
        result = int(result)
    return result
