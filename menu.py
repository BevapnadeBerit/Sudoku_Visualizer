import os
import pygame

from helper_utils import *


class Menu:
    """
    The menu screen
    """
    def __init__(self, screen_size: tuple[int, int]):
        """
        Initializes a Menu object.
        :param screen_size: width and height of screen
        """
        self.sprite_groups = {
            "menu": pygame.sprite.Group(),
        }

        middle = int(screen_size[0]/2)
        play_button_y = int(screen_size[1]/2)
        title_offset_y = BIG_BUTTON_SIZE[1]/2 + TITLE_SIZE[1]/2 + 20
        settings_button_offset_y = BIG_BUTTON_SIZE[1] + 20
        selection_offset_x = int(BIG_BUTTON_SIZE[0]/2 + 40)
        back_button_offset_y = int(BIG_BUTTON_SIZE[1]/2 + SMALL_BUTTON_SIZE[1]/2 + 40)

        self.objects_pos = {
            "title": (middle, play_button_y - title_offset_y),
            "play": (middle, play_button_y),
            "settings": (middle, play_button_y + settings_button_offset_y),
            "manual": (middle - selection_offset_x, play_button_y),
            "auto": (middle + selection_offset_x, play_button_y),
            "back": (middle, play_button_y + back_button_offset_y),
        }

        self.objects = {
            "title": Image(self.objects_pos["title"], TITLE_SIZE, "sudoku_title.png", self.sprite_groups["menu"]),
            "play": PlayButton(self.objects_pos["play"], self, self.sprite_groups),
            "settings": SettingsButton(self.objects_pos["settings"], self, self.sprite_groups),
            "manual": None,
            "auto": None,
            "back": None,
        }

    def draw(self, surface: pygame.Surface):
        draw(surface, "gray", self.sprite_groups, "menu")
        
    def draw_settings(self, surface: pygame.Surface):
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


class PlayButton(pygame.sprite.Sprite):
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
        super().__init__(sprite_groups.get("menu"))
        self.menu = menu
        self.sprite_groups = sprite_groups

        file_path = os.path.join("images", "play.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self):
        """
        Call the menu to make new buttons and remove unwanted ones
        """
        self.menu.set_button("manual", ManualButton(self.menu.objects_pos.get("manual"), self.menu, self.sprite_groups))
        self.menu.set_button("auto", AutoButton(self.menu.objects_pos.get("auto"), self.menu, self.sprite_groups))
        self.menu.set_button("back", BackButton(self.menu.objects_pos.get("back"), self.menu, self.sprite_groups))
        self.menu.kill_button("settings")
        self.menu.kill_button("play")


class SettingsButton(pygame.sprite.Sprite):
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
        super().__init__(sprite_groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "settings.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self):
        """
        Call the menu to kill everything and go to settings.
        """
        post(SETTINGS)
        self.menu.close()


class ManualButton(pygame.sprite.Sprite):
    """
    Button that opens game in MANUAL mode
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a ManualButton object.
        :param pos: screen position
        :param menu: the menu object
        :param sprite_groups: sprite group dict
        """
        super().__init__(sprite_groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "manual.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self):
        """
        Call the menu to kill everything and go to game in MANUAL mode.
        """
        post(MANUAL)
        post(GAME)
        self.menu.close()


class AutoButton(pygame.sprite.Sprite):
    """
    Button that opens game in AUTO mode
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a AutoButton object.
        :param pos: screen position
        :param menu: the menu object
        :param sprite_groups: sprite group dict
        """
        super().__init__(sprite_groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "auto.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self):
        """
        Call the menu to kill everything and go to game in AUTO mode.
        """
        post(AUTO)
        post(GAME)
        self.menu.close()


class BackButton(pygame.sprite.Sprite):
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
        super().__init__(sprite_groups.get("menu"))
        self.sprite_groups = sprite_groups
        self.menu = menu

        file_path = os.path.join("images", "back.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, SMALL_BUTTON_SIZE)

        self.image = pygame.Surface(SMALL_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self):
        """
        Returns to the original state of the menu
        """
        self.menu.set_button("play", PlayButton(self.menu.objects_pos.get("play"), self.menu, self.sprite_groups))
        self.menu.set_button("settings", SettingsButton(self.menu.objects_pos.get("settings"), self.menu, self.sprite_groups))
        for button_key in ["manual", "auto", "back"]:
            self.menu.kill_button(button_key)
