import os
import pygame
from room import *
from helper_utils import *


class Menu(Room):
    """
    The menu screen
    """
    def __init__(self, screen_size: tuple[int, int]):
        """
        Initializes a Menu object.
        :param screen_size: width and height of screen
        """
        super().__init__()
        self.sprite_groups = {
            "menu_ui": pygame.sprite.Group(),
        }

        middle_x = int(screen_size[0]/2)
        play_button_y = int(screen_size[1]/2)
        title_offset_y = BIG_BUTTON_SIZE[1]/2 + TITLE_SIZE[1]/2 + 40
        big_button_offset_y = BIG_BUTTON_SIZE[1] + 20

        self.objects_pos = {
            "title": (middle_x, play_button_y - title_offset_y),
            "play": (middle_x, play_button_y),
            "settings": (middle_x, play_button_y + 1*big_button_offset_y),
        }

        self.objects = {
            "title": Image(self.objects_pos["title"], TITLE_SIZE, "sudoku.png", self.sprite_groups["menu_ui"]),
            "play": PlayButton(self.objects_pos["play"], self, self.sprite_groups),
            "settings": SettingsButton(self.objects_pos["settings"], self, self.sprite_groups),
        }

    def draw(self, surface: pygame.Surface):
        """
        Draw the menu room
        :param surface: The surface to draw onto
        """
        draw(surface, "gray", self.sprite_groups, "menu_ui")


class PlayButton(MenuButton):
    """
    Button that enters the game room
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a PlayButton object.
        :param pos: screen position
        :param menu: the menu object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "play.png", sprite_groups)
        self.menu = menu
        self.sprite_groups = sprite_groups

    def pressed(self):
        """
        Close the menu and go to the game room
        """
        post(GAME)
        self.menu.close()


class SettingsButton(MenuButton):
    """
    Button that opens settings
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a SettingsButton object.
        :param pos: screen position
        :param menu: the menu object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "settings.png", sprite_groups)
        self.menu = menu

    def pressed(self):
        """
        Close the menu and go to settings.
        """
        post(SETTINGS)
        self.menu.close()
