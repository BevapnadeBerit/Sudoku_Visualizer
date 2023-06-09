import os
import pygame
from room import *
from helper_utils import *


class Settings(Room):
    """
    The settings screen
    """
    def __init__(self, screen_size: tuple[int, int]):
        """
        Initializes a Menu object.
        :param screen_size: width and height of screen
        """
        super().__init__()
        self.sprite_groups = {
            "settings_ui": pygame.sprite.Group(),
        }
        self.screen_size = screen_size

        middle_x = int(screen_size[0]/2)
        back_button_y = int(screen_size[1]/2 + 200)
        screen_size_button_offset_y = int(BIG_BUTTON_SIZE[1]/2 + SMALL_BUTTON_SIZE[1]/2 + 20)

        self.objects_pos = {
            "back": (middle_x, back_button_y),
            "screen": (middle_x, back_button_y - screen_size_button_offset_y),
        }

        self.objects = {
            "back": BackButton(self.objects_pos.get("back"), self, self.sprite_groups),
            "screen": ScreenSizeButton(self.objects_pos.get("screen"), self, self.sprite_groups)
        }

    def draw(self, surface: pygame.Surface):
        """
        Draw the settings room
        :param surface: The surface to draw onto
        """
        draw(surface, "gray", self.sprite_groups, "settings_ui")


class BackButton(SettingsButton):
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
        super().__init__(pos, SMALL_BUTTON_SIZE, "back.png", sprite_groups)
        self.settings = settings

    def pressed(self):
        """
        Call the settings to kill everything and go to the menu.
        """
        post(MENU)
        self.settings.close()


class ScreenSizeButton(SettingsButton):
    """
    Resizes the screen
    """
    def __init__(self, pos: tuple[int, int], settings: Settings, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a ScreenSizeButton object.
        :param pos: screen position
        :param settings: settings object
        :param sprite_groups: sprite group dict
        """
        self.settings = settings
        if is_windowed(settings.screen_size):
            filename = "fullscreen.png"
        else:
            filename = "windowed.png"
        super().__init__(pos, BIG_BUTTON_SIZE, filename, sprite_groups)

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
