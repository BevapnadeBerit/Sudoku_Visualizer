import os
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
GENERATE = pygame.USEREVENT + 7
SOLVE = pygame.USEREVENT + 8
CLEAR = pygame.USEREVENT + 9
RESET = pygame.USEREVENT + 10
EASY = pygame.USEREVENT + 11
MEDIUM = pygame.USEREVENT + 12
HARD = pygame.USEREVENT + 13

TITLE_SIZE = (598, 223)
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


def draw(surface: pygame.Surface, color: str, sprite_groups: dict[str, pygame.sprite.Group], *group_keys: str):
    """
    Draws a number of sprite groups onto a Surface with a background of given color.
    :param surface: Surface to draw onto
    :param color: color of the background
    :param sprite_groups: sprite group dict
    :param group_keys: keys to the sprite groups to draw
    :return:
    """
    surface.fill(get_color(color))
    for key in group_keys:
        sprite_groups.get(key).draw(surface)


def post(event: int):
    """
    Event post shortcut
    :param event: event to post
    """
    pygame.event.post(pygame.event.Event(event))


class Image(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], image: str,
                 group: pygame.sprite.Group):
        super().__init__(group)

        file_path = os.path.join("images", image)
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, size)

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos


class Rectangle(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int],
                 group: pygame.sprite.Group):
        super().__init__(group)

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = pos
