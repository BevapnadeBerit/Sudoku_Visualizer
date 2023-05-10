import unittest
import time
from sudoku_generator import SudokuGenerator

class TestSudokuGenerator(unittest.TestCase):

    HINTS = 45 # Number of hints in each puzzle
    NUM_PUZZLES = 5 # Number of puzzles to generate and test

    def setUp(self):
        self.generator = SudokuGenerator()

    def test_valid_puzzle(self):
        durations = []

        for _ in range(self.NUM_PUZZLES):
            start_time = time.time()  # Start the timer
            self.generator.generate_puzzle(self.HINTS)
            grid = self.generator.grid
            end_time = time.time()  # Stop the timer

            self.assertTrue(self.generator._SudokuGenerator__is_valid_grid(grid),
                            msg=f"Invalid grid:\n{self.generator._SudokuGenerator__grid_to_str(grid)}")

            durations.append(end_time - start_time)

        average_time = sum(durations) / len(durations)
        max_time = max(durations)
        min_time = min(durations)
        print("\n")
        print(f"Average time: {average_time:.2f} seconds")
        print(f"Max time: {max_time:.2f} seconds")
        print(f"Min time: {min_time:.2f} seconds")

    def test_difficulty_levels(self):
        num_puzzles = 3
        for hints in [45, 35, 29]:
            for _ in range(num_puzzles):
                (puzzle, solution) = self.generator.generate_puzzle(hints)
                self.assertTrue(self.generator._SudokuGenerator__is_valid_grid(self.generator.grid))

                # Check that the solution is equal to self.solution
                self.generator._SudokuGenerator__random_solve(puzzle)
                self.generator.print_puzzle()
                self.generator.print_solution()
                self.assertEqual(puzzle, solution)

    def test_remove_numbers(self):
        num_puzzles = 3
        hints_range = [45, 35, 29]

        for hints in hints_range:
            start_time = time.time()  # Start the timer

            for _ in range(num_puzzles):
                self.generator.generate_puzzle(hints)
                grid = self.generator.grid
                solution = self.generator.solution

                num_remaining_hints = 0
                for row in range(9):
                    for col in range(9):
                        cell = grid[row][col]
                        if cell != -1:
                            num_remaining_hints += 1
                            self.assertEqual(cell, solution[row][col],
                                            msg=f"Number {cell} at position ({row}, {col}) in the puzzle is not equal to the number {solution[row][col]} in the solution")

                self.assertEqual(num_remaining_hints, hints)

            end_time = time.time()  # Stop the timer
            print(f"test_remove_numbers ({hints} hints): {end_time - start_time:.2f} seconds")
                
    def test_is_valid_methods(self):
        start_time = time.time()  # Start the timer

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

        end_time = time.time()  # Stop the timer
        print(f"test_is_valid_methods: {end_time - start_time:.2f} seconds")

if __name__ == '__main__':
    unittest.main()
