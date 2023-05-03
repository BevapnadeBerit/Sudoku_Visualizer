import pygame


# base settings
WIDTH = 1280
HEIGHT = 720
FPS = 60

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
    "gray": (200, 200, 200),
    "red": (255, 102, 102),
    "blue": (173, 216, 230),
    "green": (102, 255, 102),
    "grid": (140, 140, 140),
}


def value_of_number_key(key: int) -> int:
    """
    Returns the represented value of a Event.key that is a number.
    :param key: The Event.key to be translated
    :return: The translated value
    """
    return key - pygame.K_1 + 1


def get_color(color: str) -> tuple[int, int, int] | None:
    """
    Returns the RGB tuple of given color
    :param color: The given color
    :return: RGB tuple
    """
    if color in colors.keys():
        return colors[color]
    else:
        return None


def post(event: int):
    """
    Event post shortcut
    :param event: event to post
    """
    pygame.event.post(pygame.event.Event(event))