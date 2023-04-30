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

    def is_valid(self, square: Square, value: int) -> bool:
        box = self._get_box(square)
        if self._value_in_box(box, value):
            return False

        if self._value_in_row(square, value):
            return False

        if self._value_in_column(square, value):
            return False

        return True

    def _get_box(self, square: Square) -> Box:
        box_x = (square.pos[0] - self.grid_pos[0] + BOX_SIZE // 2) // BOX_SIZE
        box_y = (square.pos[1] - self.grid_pos[1] + BOX_SIZE // 2) // BOX_SIZE
        return self.boxes[box_x][box_y]
    
    def _value_in_box(self, box: Box, value: int) -> bool:
        for square_row in box.squares:
            for square in square_row:
                if square.value == value:
                    return True
        return False
    
    def _value_in_row(self, square: Square, value: int) -> bool:
        for box_row in self.grid.boxes:
            for box in box_row:
                for square_row in box.squares:
                    if square in square_row:
                        for sq in square_row:
                            if sq.value == value:
                                return True
        return False

    def _value_in_column(self, square: Square, value: int) -> bool:
        for box_col in self.grid.boxes:
            for box in box_col:
                for square_col_idx in range(len(box.squares)):
                    if square in box.squares[square_col_idx]:
                        for square_col in box_col:
                            if square_col.squares[square_col_idx].value == value:
                                return True
        return False

# Add the puzzle creation class later
# class PuzzleGenerator:
#     pass