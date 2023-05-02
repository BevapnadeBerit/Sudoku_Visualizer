import pygame

# custom events main
FULLSCREEN = pygame.USEREVENT + 1
MENU = pygame.USEREVENT + 2
SETTINGS = pygame.USEREVENT + 3
GAME = pygame.USEREVENT + 4
MANUAL = pygame.USEREVENT + 5
AUTO = pygame.USEREVENT + 6

BIG_BUTTON_SIZE = (300, 100)
SMALL_BUTTON_SIZE = (150, 75)

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
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


def post(event: int):
    pygame.event.post(pygame.event.Event(event))