from grid import Grid, Square, Box


class Sudoku:
    """
    A representation of a Sudoku game.
    """
    def __init__(self, grid: Grid, grid_pos: tuple[int, int]):
        """
        Initializes a Sudoku object.

        :param grid: The Grid object to be used in the Sudoku game.
        :param grid_pos: The position of the Grid object.
        """
        self.grid = grid
        self.grid_pos = grid_pos
        self.empty_squares = 81

    def get_number(self, row: int, col: int) -> int:
        """
        Gets the number at the specified row and column of the Sudoku grid.

        :param row: The row of the number.
        :param col: The column of the number.
        :return: The number at the specified position, or -1 if there is no number.
        """
        square = self._get_square(row, col)
        return square.value

    def insert_number(self, row: int, col: int, value: int):
        """
        Inserts a number in a specified row and column of the Sudoku grid.

        :param row: The row in which the number should be inserted.
        :param col: The column in which the number should be inserted.
        :param value: The value of the number to be inserted.
        :return: True if the number was successfully inserted, False otherwise.
        """
        if value not in range(1, 10):
            return False
        square = self._get_square(row, col)
        if not self.is_number_valid(row, col, value):
            square.set_validity(False)
            square.set_value(value)
            return True
        square.set_validity(True)
        square.set_value(value)
        return True
    
    def remove_number(self, row: int, col: int):
        """
        Removes a number from a specified row and column of the Sudoku grid.

        :param row: The row from which the number should be removed.
        :param col: The column from which the number should be removed.
        """
        square = self._get_square(row, col)
        square.reset()

    def reset(self):
        """
        Removes all the values from Squares in the grid.
        """
        for row in range(9):
            for col in range(9):
                self.remove_number(row, col)

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
