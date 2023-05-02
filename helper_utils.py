import pygame

colors = {
    "white": (255, 255, 255),
    "black": (255, 255, 255),
    "gray": (140, 140, 140),
    "red": (255, 102, 102),
    "blue": (173, 216, 230),
    "green": (102, 255, 102),
}


def value_of_number_key(key: int) -> int:
    """
    Returns the represented value of a Event.key that is a number.
    :param key: The Event.key to be translated
    :return: The translated value
    """
    return key - pygame.K_1 + 1


def get_color(color: str) -> tuple[int, int, int] | None:
    if color in colors.keys():
        return colors[color]
    else:
        return None
