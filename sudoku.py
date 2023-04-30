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

    def insert_number(self, row: int, col: int, value: int):
        """
        Inserts a number in a specified row and column of the Sudoku grid.

        :param row: The row in which the number should be inserted.
        :param col: The column in which the number should be inserted.
        :param value: The value of the number to be inserted.
        :return: True if the number was successfully inserted, False otherwise.
        """
        if not self.is_number_valid(row, col, value):
            return False
        square = self.grid.boxes[row // 3][col // 3].squares[row % 3][col % 3]
        group = square.groups()[0]
        square.set_value(value, group)
        return True
    
    def remove_number(self, row: int, col: int):
        """
        Removes a number from a specified row and column of the Sudoku grid.

        :param row: The row from which the number should be removed.
        :param col: The column from which the number should be removed.
        """
        square = self.grid.boxes[row // 3][col // 3].squares[row % 3][col % 3]
        group = square.groups()[0]
        square.set_value(-1, group)

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
        for i in range(9):
            if self.grid.boxes[row // 3][i // 3].squares[row % 3][i % 3].value == num:
                return False
            if self.grid.boxes[i // 3][col // 3].squares[i % 3][col % 3].value == num:
                return False
            
        # Check if the number is already in the same box
        box = self._get_box(self.grid.boxes[row // 3][col // 3].squares[row % 3][col % 3])
        return not self._value_in_box(box, num)

    def _get_box(self, square: Square) -> Box:
        """
        Returns the Box object to which a specified Square object belongs.

        :param square: The Square object.
        :return: The Box object to which the specified Square object belongs.
        """
        box_x = square.col // 3
        box_y = square.row // 3
        return self.grid.boxes[box_y][box_x]
    
    def _value_in_box(self, box: Box, value: int) -> bool:
        """
        Checks if a value is already in any of the Squares of a specified Box object.

        :param box: The Box object.
        :param value: The value to check.
        :return: True if the value is already in the Box object, False otherwise.
        """
        for square_row in box.squares:
            for square in square_row:
                if square.value == value:
                    return True
        return False

# Add the puzzle creation class later
# class PuzzleGenerator:
#     pass