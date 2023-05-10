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
        settings_button_offset_y = BIG_BUTTON_SIZE[1] + 20
        selection_offset_x = int(BIG_BUTTON_SIZE[0]/2 + 40)
        back_button_offset_y = int(BIG_BUTTON_SIZE[1]/2 + SMALL_BUTTON_SIZE[1]/2 + 40)

        self.objects_pos = {
            "title": (middle_x, play_button_y - title_offset_y),
            "play": (middle_x, play_button_y),
            "settings": (middle_x, play_button_y + settings_button_offset_y),
            "manual": (middle_x - selection_offset_x, play_button_y),
            "auto": (middle_x + selection_offset_x, play_button_y),
            "back": (middle_x, play_button_y + back_button_offset_y),
        }

        self.objects = {
            "title": Image(self.objects_pos["title"], TITLE_SIZE, "sudoku.png", self.sprite_groups["menu_ui"]),
            "play": PlayButton(self.objects_pos["play"], self, self.sprite_groups),
            "settings": SettingsButton(self.objects_pos["settings"], self, self.sprite_groups),
            "manual": None,
            "auto": None,
            "back": None,
        }

    def draw(self, surface: pygame.Surface):
        """
        Draw the menu room
        :param surface: The surface to draw onto
        """
        draw(surface, "gray", self.sprite_groups, "menu_ui")


class PlayButton(MenuButton):
    """
    Button that forwards to MANUAL/AUTO options
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
        Call the menu to make new buttons and remove unwanted ones
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
        Call the menu to kill everything and go to settings.
        """
        post(SETTINGS)
        self.menu.close()


class BackButton(MenuButton):
    """
    Button that returns to before the MANUAL/AUTO selection
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a BackButton object.
        :param pos: screen position
        :param menu: the menu object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, SMALL_BUTTON_SIZE, "back.png", sprite_groups)
        self.sprite_groups = sprite_groups
        self.menu = menu

    def pressed(self):
        """
        Returns to the original state of the menu
        """
        self.menu.set_button("play", PlayButton(self.menu.objects_pos.get("play"), self.menu, self.sprite_groups))
        self.menu.set_button("settings", SettingsButton(self.menu.objects_pos.get("settings"), self.menu, self.sprite_groups))
        for button_key in ["manual", "auto", "back"]:
            self.menu.kill_button(button_key)
