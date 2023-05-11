import pygame
from helper_utils import *
from room import *
from sudoku import Sudoku
from grid import *


class Game(Room):
    """
    The game room
    """

    def __init__(self, screen_size: tuple[int, int], screen: pygame.Surface):
        """
        Initializes a Game object.
        :param screen_size: width and height of screen
        """
        super().__init__()
        self.sprite_groups = {
            "game_ui": pygame.sprite.Group(),
            "grid": pygame.sprite.Group(),
            "box": pygame.sprite.Group(),
            "square": pygame.sprite.Group(),
            "number": pygame.sprite.Group(),
            "background": pygame.sprite.Group(),
        }

        middle_x = int(screen_size[0] / 2)
        middle_y = int(screen_size[1] / 2)
        sidebar_offset_x = int(GRID_SIDE / 2 + BIG_BUTTON_SIZE[0] / 2 + 20)
        button_space_y = 20 + BIG_BUTTON_SIZE[1]

        self.objects_pos = {
            "grid": (middle_x, middle_y),
            "generate": (middle_x + sidebar_offset_x, middle_y - int(1.5 * button_space_y)),
            "solve": (middle_x + sidebar_offset_x, middle_y - int(0.5 * button_space_y)),
            "clear": (middle_x + sidebar_offset_x, middle_y + int(0.5 * button_space_y)),
            "reset": (middle_x + sidebar_offset_x, middle_y + int(1.5 * button_space_y)),
            "easy": (middle_x - sidebar_offset_x, middle_y - int(button_space_y)),
            "medium": (middle_x - sidebar_offset_x, middle_y),
            "hard": (middle_x - sidebar_offset_x, middle_y + int(button_space_y)),
        }

        self.objects = {
            "grid": Grid(screen_size, 3, 3, 3, 3, self.sprite_groups),
            "generate": GenerateButton(self.objects_pos["generate"], self, self.sprite_groups),
            "solve": SolveButton(self.objects_pos["solve"], self, self.sprite_groups),
            "clear": ClearButton(self.objects_pos["clear"], self, self.sprite_groups),
            "reset": ResetButton(self.objects_pos["reset"], self, self.sprite_groups),
            "easy": EasyButton(self.objects_pos["easy"], self, self.sprite_groups),
            "medium": MediumButton(self.objects_pos["medium"], self, self.sprite_groups),
            "hard": HardButton(self.objects_pos["hard"], self, self.sprite_groups),
        }
        self.sudoku = Sudoku(self.objects["grid"], self.objects_pos["grid"], self.sprite_groups, screen)

    def draw(self, surface: pygame.Surface):
        """
        Draw the game room
        :param surface: The surface to draw onto
        """
        draw(surface, "white", self.sprite_groups,
             "grid",
             "box",
             "background",
             "square",
             "number",
             "game_ui",
             )


class GenerateButton(GameButton):
    """
    Button that generates a new puzzle
    """

    def __init__(self, pos: tuple[int, int], game: Game, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a GenerateButton object.
        :param pos: screen position
        :param game: game object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "generate.png", sprite_groups)
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        post(GENERATE)


class SolveButton(GameButton):
    """
    Button that solves current puzzle with solver
    """

    def __init__(self, pos: tuple[int, int], game: Game, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a SolveButton object.
        :param pos: screen position
        :param game: game object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "solve.png", sprite_groups)
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        post(SOLVE)


class ClearButton(GameButton):
    """
    Button that removes all non-start values in puzzle
    """

    def __init__(self, pos: tuple[int, int], game: Game, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a ClearButton object.
        :param pos: screen position
        :param game: game object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "clear.png", sprite_groups)
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        post(CLEAR)


class ResetButton(GameButton):
    """
    Button that removes all values in puzzle
    """

    def __init__(self, pos: tuple[int, int], game: Game, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a ResetButton object.
        :param pos: screen position
        :param game: game object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "reset.png", sprite_groups)
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        post(RESET)


class EasyButton(GameButton):
    """
    Button that selects easy difficulty
    """

    def __init__(self, pos: tuple[int, int], game: Game, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a EasyButton object.
        :param pos: screen position
        :param game: game object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "easy.png", sprite_groups)
        self.game = game
        self.sprite_groups = sprite_groups

        self.pos = pos
        self.background = None

    def pressed(self):
        """
        Activates Easy Mode.
        Unpress other difficulty buttons.
        Mark this button as pressed.
        """
        if self.background is None:
            post(EASY)
            self.background = Rectangle(self.pos, BIG_BUTTON_SIZE, get_color("blue"), self.sprite_groups["background"])
            for difficulty in ["medium", "hard"]:
                self.game.objects[difficulty].unpressed()

    def unpressed(self):
        """
        Removes background if not None
        """
        if self.background is not None:
            self.background.kill()
            self.background = None


class MediumButton(GameButton):
    """
    Button that selects medium difficulty
    """

    def __init__(self, pos: tuple[int, int], game: Game, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a MediumButton object.
        :param pos: screen position
        :param game: game object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "medium.png", sprite_groups)
        self.game = game
        self.sprite_groups = sprite_groups

        self.pos = pos
        self.background = None

    def pressed(self):
        """
        Activates Medium Mode.
        Unpress other difficulty buttons.
        Mark this button as pressed.
        """
        if self.background is None:
            post(MEDIUM)
            self.background = Rectangle(self.pos, BIG_BUTTON_SIZE, get_color("blue"), self.sprite_groups["background"])
            for difficulty in ["easy", "hard"]:
                self.game.objects[difficulty].unpressed()

    def unpressed(self):
        """
        Removes background if not None
        """
        if self.background is not None:
            self.background.kill()
            self.background = None


class HardButton(GameButton):
    """
    Button that selects hard difficulty
    """

    def __init__(self, pos: tuple[int, int], game: Game, sprite_groups: dict[str, pygame.sprite.Group]):
        """
        Initializes a HardButton object.
        :param pos: screen position
        :param game: game object
        :param sprite_groups: sprite group dict
        """
        super().__init__(pos, BIG_BUTTON_SIZE, "hard.png", sprite_groups)
        self.game = game
        self.sprite_groups = sprite_groups

        self.pos = pos
        self.background = None

    def pressed(self):
        """
        Activates Hard Mode.
        Unpress other difficulty buttons.
        Mark this button as pressed.
        """
        if self.background is None:
            post(HARD)
            self.background = Rectangle(self.pos, BIG_BUTTON_SIZE, get_color("blue"), self.sprite_groups["background"])
            for difficulty in ["easy", "medium"]:
                self.game.objects[difficulty].unpressed()

    def unpressed(self):
        """
        Removes background if not None
        """
        if self.background is not None:
            self.background.kill()
            self.background = None
