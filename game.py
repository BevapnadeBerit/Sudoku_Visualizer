import pygame
from helper_utils import *
from room import *
from sudoku import Sudoku
from grid import *


class Game(Room):
    """
    The game room
    """

    def __init__(self, screen_size: tuple[int, int]):
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
            "square_background": pygame.sprite.Group(),
        }

        middle_x = int(screen_size[0]/2)
        middle_y = int(screen_size[1]/2)
        sidebar_offset_x = int(GRID_SIDE/2 + BIG_BUTTON_SIZE[0]/2 + 20)
        button_space_y = 20 + BIG_BUTTON_SIZE[1]

        self.objects_pos = {
            "grid": (middle_x, middle_y),
            "generate": (middle_x + sidebar_offset_x, middle_y - int(1.5*button_space_y)),
            "solve": (middle_x + sidebar_offset_x, middle_y - int(0.5*button_space_y)),
            "clear": (middle_x + sidebar_offset_x, middle_y + int(0.5*button_space_y)),
            "reset": (middle_x + sidebar_offset_x, middle_y + int(1.5*button_space_y)),
        }

        self.objects = {
            "grid": Grid(screen_size, 3, 3, 3, 3, self.sprite_groups),
            "generate": GenerateButton(self.objects_pos["generate"], self, self.sprite_groups),
            "solve": SolveButton(self.objects_pos["solve"], self, self.sprite_groups),
            "clear": ClearButton(self.objects_pos["clear"], self, self.sprite_groups),
            "reset": ResetButton(self.objects_pos["reset"], self, self.sprite_groups),
        }
        self.sudoku = Sudoku(self.objects["grid"], self.objects_pos["grid"])

    def draw(self, surface: pygame.Surface):
        """
        Draw the game room
        :param surface: The surface to draw onto
        """
        draw(surface, "white", self.sprite_groups,
             "grid",
             "box",
             "square_background",
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
        super().__init__(pos, BIG_BUTTON_SIZE, "generate.png", sprite_groups)  # <-- Insert image
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        pass


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
        super().__init__(pos, BIG_BUTTON_SIZE, "solve.png", sprite_groups)  # <-- Insert image
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        pass


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
        super().__init__(pos, BIG_BUTTON_SIZE, "clear.png", sprite_groups)  # <-- Insert image
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        pass


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
        super().__init__(pos, BIG_BUTTON_SIZE, "reset.png", sprite_groups)  # <-- Insert image
        self.game = game
        self.sprite_groups = sprite_groups

    def pressed(self):
        pass
