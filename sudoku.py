import os
import pygame
from grid import Grid, Square, Box, square_collision, BOX_SIZE
from helper_utils import value_of_number_key


class Sudoku:
    def __init__(self, grid: Grid, grid_pos: tuple[int, int]):
        self.grid = grid
        self.grid_pos = grid_pos

    def insert_number(self, row: int, col: int, value: int):
        square = self.grid.boxes[row // 3][col // 3].squares[row % 3][col % 3]
        group = square.groups()[0]
        square.set_value(value, group)

    def is_number_valid(self, row: int, col: int, num: int) -> bool:
        # Check if the number is already in the same row or column
        for i in range(9):
            if self.grid.squares[row][i].value == num:
                return False
            if self.grid.squares[i][col].value == num:
                return False
        
        # Check if the number is already in the same box
        box = self._get_box(self.grid.squares[row][col])
        return not self._value_in_box(box, num)

    def _get_box(self, square: Square) -> Box:
        box_x = square.col // 3
        box_y = square.row // 3
        return self.grid.boxes[box_y][box_x]
    
    def _value_in_box(self, box: Box, value: int) -> bool:
        for square_row in box.squares:
            for square in square_row:
                if square.value == value:
                    return True
        return False

# Add the puzzle creation class later
# class PuzzleGenerator:
#     pass