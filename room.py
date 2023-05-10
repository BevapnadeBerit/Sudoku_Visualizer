import pygame
import os
from helper_utils import *


class Room:
    """
    A room superclass
    """
    def __init__(self):
        """
        Initializes a Room object.
        """
        self.sprite_groups = {}
        self.objects_pos = {}
        self.objects = {}

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


class Button(pygame.sprite.Sprite):
    """
    A button superclass
    """
    def __init__(self, pos: tuple[int, int], button_size: tuple[int, int], filename: str, group_name: str,
                 sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a Button object.
        """
        super().__init__(sprite_groups[group_name])
        file_path = os.path.join("images", filename)
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, button_size)

        self.image = pygame.Surface(button_size, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos


class MenuButton(Button):
    """
    A superclass for buttons in a menu room
    """
    def __init__(self, pos: tuple[int, int], button_size: tuple[int, int], filename: str,
                 sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a MenuButton object.
        """
        super().__init__(pos, button_size, filename, "menu_ui", sprite_groups)


class SettingsButton(Button):
    """
    A superclass for buttons in a settings room
    """
    def __init__(self, pos: tuple[int, int], button_size: tuple[int, int], filename: str,
                 sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a SettingsButton object.
        """
        super().__init__(pos, button_size, filename, "settings_ui", sprite_groups)


class GameButton(Button):
    """
    A superclass for buttons in a game room
    """
    def __init__(self, pos: tuple[int, int], button_size: tuple[int, int], filename: str,
                 sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a GameButton object.
        """
        super().__init__(pos, button_size, filename, "game_ui", sprite_groups)
