import os

import pygame

BIG_BUTTON_SIZE = (300, 100)
SMALL_BUTTON_SIZE = (200, 100)


class Menu:
    """
    The menu screen
    """
    def __init__(self, screen_size: tuple[int, int], groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a Menu object.
        :param screen_size: width and height of screen
        :param groups: sprite group dict
        """
        self.middle = int(screen_size[0] / 2)
        self.play_button_y = int(screen_size[1]/2)
        self.settings_button_offset_y = BIG_BUTTON_SIZE[1] + 20
        self.selection_offset_x = BIG_BUTTON_SIZE[0] + 100
        self.back_button_offset_y = SMALL_BUTTON_SIZE[1] + 100

        self.button_pos = {
            "play": (self.middle, self.play_button_y),
            "settings": (self.middle, self.play_button_y + self.settings_button_offset_y),
            "manual": (self.middle - self.selection_offset_x, self.play_button_y),
            "auto": (self.middle + self.selection_offset_x, self.play_button_y),
            "back": (self.middle, self.play_button_y + self.back_button_offset_y),
        }

        self.buttons = {
            "play": PlayButton(self.button_pos.get("play"), self, groups),
            "settings": SettingsButton(self.button_pos.get("settings"), self, groups),
            "manual": None,
            "auto": None,
            "back": None,
        }

    def kill_button(self, key: str):
        """
        Kill the object if not None and set its value in self.buttons to None
        :param key: Key to the object
        """
        if self.buttons[key] is not None:
            self.buttons[key].kill()
            self.buttons[key] = None


class PlayButton(pygame.sprite.Sprite):
    """
    Button that forwards to MANUAL/AUTO options
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a PlayButton object.
        :param pos: screen position
        :param groups: sprite group dict
        """
        print(1)
        super().__init__(groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "play.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self, groups: dict[str, pygame.sprite.Group]):
        """
        Call the menu to make new buttons and remove unwanted ones
        :param groups: sprite group dict
        """
        self.menu.manual_button = ManualButton(self.menu.button_pos.get("manual"), self.menu, groups)
        self.menu.auto_button = AutoButton(self.menu.button_pos.get("auto"), self.menu, groups)
        self.menu.back_button = BackButton(self.menu.button_pos.get("back"), self.menu, groups)
        self.menu.kill_button("settings")
        self.menu.kill_button("play")


class SettingsButton(pygame.sprite.Sprite):
    """
    Button that opens settings
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a SettingsButton object.
        :param pos: screen position
        :param groups: sprite group dict
        """
        super().__init__(groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "settings.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self, groups: dict[str, pygame.sprite.Group]):
        """
        Call the menu to kill everything and go to settings.
        :param groups: sprite group dict
        """


class ManualButton(pygame.sprite.Sprite):
    """
    Button that opens game in MANUAL mode
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a ManualButton object.
        :param pos: screen position
        :param groups: sprite group dict
        """
        super().__init__(groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "manual.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self, groups: dict[str, pygame.sprite.Group]):
        """
        Call the menu to kill everything and go to game in MANUAL mode.
        :param groups: sprite group dict
        """


class AutoButton(pygame.sprite.Sprite):
    """
    Button that opens game in AUTO mode
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a AutoButton object.
        :param pos: screen position
        :param groups: sprite group dict
        """
        super().__init__(groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "auto.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, BIG_BUTTON_SIZE)

        self.image = pygame.Surface(BIG_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self, groups: dict[str, pygame.sprite.Group]):
        """
        Call the menu to kill everything and go to game in AUTO mode.
        :param groups: sprite group dict
        """


class BackButton(pygame.sprite.Sprite):
    """
    Button that returns to before the MANUAL/AUTO selection
    """
    def __init__(self, pos: tuple[int, int], menu: Menu, groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a BackButton object.
        :param pos: screen position
        :param menu: the menu
        :param groups: sprite group dict
        """
        super().__init__(groups.get("menu"))
        self.menu = menu

        file_path = os.path.join("images", "back.png")
        image = pygame.image.load(file_path).convert_alpha()
        image = pygame.transform.scale(image, SMALL_BUTTON_SIZE)

        self.image = pygame.Surface(SMALL_BUTTON_SIZE, pygame.SRCALPHA)
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def pressed(self, groups: dict[str, pygame.sprite.Group]):
        self.menu.play_button = PlayButton(self.menu.button_pos.get("play"), self.menu, groups)
        for button_key in ["manual", "auto", "back"]:
            self.menu.kill_button(button_key)
