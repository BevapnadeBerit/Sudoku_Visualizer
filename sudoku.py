from grid import Grid, Square, Box
from sudoku_generator import SudokuGenerator
import pygame
from helper_utils import *


class Sudoku:
    """
    A representation of a Sudoku game.
    """
    def __init__(self, grid: Grid, grid_pos: tuple[int, int], sprite_groups: dict[str, pygame.sprite.Group], 
                 screen: pygame.Surface):
        """
        Initializes a Sudoku object.

        :param grid: The Grid object to be used in the Sudoku game.
        :param grid_pos: The position of the Grid object.
        """
        self.sprite_groups = sprite_groups
        self.screen = screen
        self.grid = grid
        self.grid_pos = grid_pos
        self.empty_squares = 81
        self.solved = False

    def update_screen(self):
        draw(self.screen, "white", self.sprite_groups,
            "grid",
            "box",
            "background",
            "square",
            "number",
            "game_ui",
            )
        pygame.display.flip()

    def puzzle_to_grid(self, matrix: list[list[int]]) -> None:
        self.reset()
        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                if value != -1:
                    square = self._get_square(row_idx, col_idx)
                    square.set_value(value)
                    square.set_static(True)

    def grid_to_list(self) -> list[list[int]]:
        """
        Converts the Sudoku grid into a list of lists representation.

        :return: The grid represented as a list of lists.
        """
        grid_list = []
        for row in range(9):
            row_list = []
            for col in range(9):
                value = self.get_number(row, col)
                row_list.append(value)
            grid_list.append(row_list)
        return grid_list

    def generate_puzzle(self, difficulty: str) -> None:
        if difficulty == "EASY":
            hints = 45
        elif difficulty == "MEDIUM":
            hints = 35
        elif difficulty == "HARD":
            hints = 29
        else:
            raise ValueError("Invalid difficulty level!")
        generator = SudokuGenerator()
        puzzle = generator.generate_puzzle(hints)[0]
        self.puzzle_to_grid(puzzle)

    def demo(self) -> None:
        hard_sudoku = [    
            [5, 3, -1, -1, 7, -1, -1, -1, -1],
            [6, -1, -1, 1, 9, 5, -1, -1, -1],
            [-1, 9, 8, -1, -1, -1, -1, 6, -1],
            [8, -1, -1, -1, 6, -1, -1, -1, 3],
            [4, -1, -1, 8, -1, 3, -1, -1, 1],
            [7, -1, -1, -1, 2, -1, -1, -1, 6],
            [-1, 6, -1, -1, -1, -1, 2, 8, -1],
            [-1, -1, -1, 4, 1, 9, -1, -1, 5],
            [-1, -1, -1, -1, 8, -1, -1, 7, 9]
        ]
        self.puzzle_to_grid(hard_sudoku)
        self.solve()

    def solve(self) -> bool:
        """
        Solves the Sudoku using backtracking.
        """
        self.grid_matrix = self.grid_to_list()  # Translate the grid to a matrix
        return self._solve_matrix()

    def _solve_matrix(self) -> bool:
        """
        Solves the Sudoku grid matrix using backtracking.

        :return: True if the Sudoku grid matrix can be solved, False otherwise.
        """
        for row in range(9):
            for col in range(9):
                if self.grid_matrix[row][col] == -1:  # Check if the square is empty
                    for num in range(1, 10):  # Try numbers from 1 to 9
                        if self._is_number_valid_matrix(row, col, num):  # Check if the number is valid
                            # Assign the number to the square and insert it in the grid
                            self.grid_matrix[row][col] = num
                            self._get_square(row, col).set_value(num)
                            self.update_screen()

                            if self._solve_matrix():  # Recursively try to solve the rest of the grid
                                return True

                            # If the recursive call fails, remove the number from the square and the grid
                            self.grid_matrix[row][col] = -1
                            self._get_square(row, col).reset()
                            #self.update_screen()

                    return False  # If no number can be inserted in the current square, backtrack

        # If all the squares are filled, the Sudoku is solved
        self.update_square_validities()
        self.solved = self.is_grid_valid()
        return self.solved

    def _is_number_valid_matrix(self, row: int, col: int, num: int) -> bool:
        """
        Checks if a number is valid to be inserted in a specified row and  
        column of the Sudoku grid matrix according to the rules of Sudoku.

        :param row: The row to check.
        :param col: The column to check.
        :param num: The number to check.
        :return: True if the number is valid, False otherwise.
        """
        # Check if the number is already in the same row or column
        if num in self.grid_matrix[row] or num in (self.grid_matrix[i][col] for i in range(9)):
            return False

        # Check if the number is already in the same 3x3 box
        box_start_row, box_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid_matrix[i + box_start_row][j + box_start_col] == num:
                    return False

        return True

    def get_number(self, row: int, col: int) -> int:
        """
        Gets the number at the specified row and column of the Sudoku grid.

        :param row: The row of the number.
        :param col: The column of the number.
        :return: The number at the specified position, or -1 if there is no number.
        """
        square = self._get_square(row, col)
        return square.value
    
    def manually_insert_number(self, square: Square, value: int, hint: bool = False):
        if square.static:
            return False
        
        square.set_value(value)
        if self.empty_squares == 0:  # If this was the last empty square
            self.update_square_validities()  # Update validities to make sure the grid is valid
            if self.is_grid_valid():
                self.solved = True  # Set the win condition to True

        return True

    def auto_insert_number(self, square: Square, value: int, force: bool = False):
        """
        Inserts a number in a specified square of the Sudoku grid.

        :param square: The square in which the number should be inserted.
        :param value: The value of the number to be inserted.
        :param force: If True, the number will be inserted even if it's not valid.
        :return: True if the number was successfully inserted, False otherwise.
        """
        if square.static:
            return False
        #if value not in range(1, 10):
           # return False

        """if force or self.is_number_valid(square.row, square.col, value):
            if square.value == -1:  # Decrease the number of empty squares only if the square was empty
                self.empty_squares -= 1

            square.set_validity(True)
            square.set_value(value)
        else:
            square.set_validity(False)
            square.set_value(value)"""
        square.set_value(value)
        #self.update_screen()
        return True
    
    def remove_number(self, row: int, col: int):
        """
        Removes a number from a specified row and column of the Sudoku grid.
        Skips hints.

        :param row: The row from which the number should be removed.
        :param col: The column from which the number should be removed.
        """
        square = self._get_square(row, col)
        if not square.static:
            square.reset()

    def clear(self):
        """
        Removes all the values from Squares in the grid, except hints.
        """
        for row in range(9):
            for col in range(9):
                self.remove_number(row, col)
        self.update_square_validities()
        solved = self.is_grid_valid()
        self.solved = solved

    def reset(self):
        for row in range(9):
            for col in range(9):
                square = self._get_square(row, col)
                square.reset()
        self.solved = False

    def is_number_valid(self, row: int, col: int, num: int) -> bool:
        """
        Checks if a number is valid to be inserted in a specified row and  
        column of the Sudoku grid according to the rules of Sudoku.

        :param row: The row to check.
        :param col: The column to check.
        :param num: The number to check.
        :return: True if the number is valid, False otherwise.
        """
        # Check if the number is already in the same row or column
        if self._value_in_row(row, num, exclude_col=col):
            return False
        if self._value_in_col(col, num, exclude_row=row):
            return False
            
        # Check if the number is already in the same box
        box = self._get_box(self._get_square(row, col))
        return not self._value_in_box(box, num, exclude_row=row, exclude_col=col)
    
    def find_empty_square(self) -> Square | None:
        """
        Finds the next empty square in the Sudoku grid.
        :return: The next empty Square, or None if there are no more empty squares.
        """
        for row in range(9):
            for col in range(9):
                if self.get_number(row, col) == -1:
                    return self._get_square(row, col)
        return None
    
    def is_grid_valid(self) -> bool:
        """
        Checks the whole grid and returns True if all Squares are valid, False otherwise.
        Squares are only valid if they are not empty and have a valid number.

        :return: True if all Squares are valid, False otherwise.
        """
        for row in range(9):
            for col in range(9):
                square = self._get_square(row, col)
                if not square.valid:
                    return False
        return True

    def update_square_validities(self):
        """
        Updates all the Square's validities by calling is_number_valid on all of them.
        WARNING: Destructive, since it will set previously valid Squares as invalid based
        on later insertions.
        """
        for row in range(9):
            for col in range(9):
                value = self.get_number(row, col)
                if value != -1:
                    validity = self.is_number_valid(row, col, value)
                    self._get_square(row, col).set_validity(validity)
    
    def _get_square(self, row: int, col: int) -> Square:
        """
        Returns the Square object at a specified row and column of the Sudoku grid.

        :param row: The row of the Square object.
        :param col: The column of the Square object.
        :return: The Square object at the specified position.
        """
        return self.grid.boxes[row // 3][col // 3].squares[row % 3][col % 3]

    def _get_box(self, square: Square) -> Box:
        """
        Returns the Box object to which a specified Square object belongs.

        :param square: The Square object.
        :return: The Box object to which the specified Square object belongs.
        """
        box_row = square.row // 3
        box_col = square.col // 3
        return self.grid.boxes[box_row][box_col]
    
    def _value_in_row(self, row: int, num: int, exclude_col: int = None) -> bool:
        """
        Checks if a number is already in the same row.

        :param row: The row to check.
        :param num: The number to check.
        :param exclude_col: The column to exclude from the check.
        :return: True if the number is already in the same row, False otherwise.
        """
        for i in range(9):
            if i != exclude_col and self.get_number(row, i) == num:
                return True
        return False


    def _value_in_col(self, col: int, num: int, exclude_row: int = None) -> bool:
        """
        Checks if a number is already in the same column.

        :param col: The column to check.
        :param num: The number to check.
        :param exclude_row: The row to exclude from the check.
        :return: True if the number is already in the same column, False otherwise.
        """
        for i in range(9):
            if i != exclude_row and self.get_number(i, col) == num:
                return True
        return False

    def _value_in_box(self, box: Box, value: int, exclude_row: int = None, exclude_col: int = None) -> bool:
        """
        Checks if a value is already in any of the Squares of a specified Box object.

        :param box: The Box object.
        :param value: The value to check.
        :param exclude_row: The row to exclude from the check.
        :param exclude_col: The column to exclude from the check.
        :return: True if the value is already in the Box object, False otherwise.
        """
        for row_idx, square_row in enumerate(box.squares):
            for col_idx, square in enumerate(square_row):
                if (row_idx != exclude_row % 3 or col_idx != exclude_col % 3) and square.value == value:
                    return True
        return False
