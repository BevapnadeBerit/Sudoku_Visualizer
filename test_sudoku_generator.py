import unittest
from sudoku_generator import SudokuGenerator

class TestSudokuGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = SudokuGenerator()

    def test_valid_puzzle(self):
        num_puzzles = 10  # Number of puzzles to generate and test

        for _ in range(num_puzzles):
            self.generator.generate_puzzle()
            grid = self.generator.grid

            for row in range(9):
                for col in range(9):
                    num = grid[row][col]
                    grid[row][col] = -1
                    
                    self.assertTrue(self.generator._SudokuGenerator__is_valid(grid, row, col, num))

                    grid[row][col] = num
                
    def test_is_valid_methods(self):
        # Fully solved Sudoku grid
        solved_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

        # Incomplete Sudoku grid
        incomplete_grid = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, -1, 7, 9]
        ]

        for grid_type, grid in [("solved", solved_grid), ("incomplete", incomplete_grid)]:
            for row in range(9):
                for col in range(9):
                    num = grid[row][col]

                    if num != -1:
                        grid[row][col] = -1

                        for i in range(1, 10):
                            if i != num:
                                self.assertFalse(self.generator._SudokuGenerator__is_valid(grid, row, col, i))

                        if grid_type == "solved":
                            self.assertTrue(self.generator._SudokuGenerator__is_valid(grid, row, col, num))

                        grid[row][col] = num

                    if grid_type == "incomplete" and num == -1:
                        for i in range(1, 10):
                            if i != 1:
                                self.assertFalse(self.generator._SudokuGenerator__is_valid(grid, row, col, i))

                        self.assertTrue(self.generator._SudokuGenerator__is_valid(grid, row, col, 1))

if __name__ == '__main__':
    unittest.main()
