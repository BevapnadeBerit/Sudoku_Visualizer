import os
import pygame
from helper_utils import *


class Settings:
    """
    The settings screen
    """
    def __init__(self, screen_size: tuple[int, int]):
        """
        Initializes a Menu object.
        :param screen_size: width and height of screen
        """
        self.sprite_groups = {
            "menu": pygame.sprite.Group(),
            "settings": pygame.sprite.Group(),
        }
        self.screen_size = screen_size
        self.middle = int(screen_size[0]/2)
        self.back_button_y = int(screen_size[1]/2 + 200)
        self.screen_size_button_offset_y = int(BIG_BUTTON_SIZE[1]/2 + SMALL_BUTTON_SIZE[1]/2 + 20)

        self.objects_pos = {
            "back": (self.middle, self.back_button_y),
            "screen": (self.middle, self.back_button_y - self.screen_size_button_offset_y),
        }

        self.objects = {
            "back": BackButton(self.objects_pos.get("back"), self, self.sprite_groups),
            "screen": ScreenSizeButton(self.objects_pos.get("screen"), self, self.sprite_groups)
        }

    def draw(self, surface: pygame.Surface):
        draw(surface, "gray", self.sprite_groups, "settings")

    def set_button(self, key: str, value):
        """
        Remove a keypair and set it anew.
        :param key: The key in the pair
        :param value: The value in the pair
        """
        self.objects.pop(key)
        self.objects[key] = value

    def kill_button(self, key: str):
        """
        Kill the object if not None and set its value to None
        :param key: Key to the object
        """
        if self.objects[key] is not None:
            self.objects[key].kill()
            self.objects[key] = None

    def close(self):
        """
        Kill all buttons
        """
        for key in [key for key in self.objects.keys()]:
            self.kill_button(key)


class BackButton(pygame.sprite.Sprite):
    """
    Button that returns to menu
    """

    def __init__(self, pos: tuple[int, int], settings: Settings, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a BackButton object.
        :param pos: screen position
        :param settings: settings object
        :param sprite_groups: sprite group dict
        """
        super().__init__(sprite_groups.get("settings"))
        self.settings = settings

        file_path = os.path.join("images", "back.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, SMALL_BUTTON_SIZE)

        self.image = pygame.Surface(SMALL_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self):
        """
        Call the settings to kill everything and go to the menu.
        """
        post(MENU)
        self.settings.close()


class ScreenSizeButton(pygame.sprite.Sprite):
    """
    Resizes the screen
    """
    def __init__(self, pos: tuple[int, int], settings: Settings, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a ScreenSizeButton object.
        :param pos: screen position
        :param settings: settings object
        :param groups: sprite group dict
        """
        super().__init__(sprite_groups.get("settings"))
        self.settings = settings

        if is_windowed(settings.screen_size):
            file_path = os.path.join("images", "fullscreen.png")
        else:
            file_path = os.path.join("images", "windowed.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self):
        """
        Changes from Windowed to Fullscreen and vice versa.
        Then goes back to the menu
        """
        post(FULLSCREEN)
        post(MENU)
        self.settings.close()


def is_windowed(screen_size):
    """
    Check if windowed
    :return: true if windowed, false if not
    """
    return screen_size == (WIDTH, HEIGHT)
