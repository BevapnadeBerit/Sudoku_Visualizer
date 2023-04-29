import os
import pygame
from grid import Grid, Square, Box, square_collision
from helper_utils import value_of_number_key


class Sudoku:
    def __init__(self, grid: Grid, grid_pos: tuple[int, int]):
        self.grid = grid
        self.grid_pos = grid_pos

    def insert_number(self, square: Square, value: int):
        group = square.groups()[0]
        square.set_value(value, group)

    def is_number_valid(self, row: int, col: int, num: int) -> bool:
        pass

# Add the puzzle creation class later
# class PuzzleGenerator:
#     pass