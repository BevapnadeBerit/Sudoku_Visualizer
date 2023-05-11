# Generated with ChatGPT

import unittest
from grid import Grid, Square, Box
from sudoku import Sudoku

import pygame

pygame.init()
pygame.display.set_mode((1, 1))

import random


class TestSudoku(unittest.TestCase):

    def setUp(self):
        grid_pos = (0, 0)
        self.grid = Grid(grid_pos, 3, 3, 3, 3)
        self.sudoku = Sudoku(self.grid, grid_pos)

    def test_insert_number_full_grid(self):
        # Insert random values in all squares
        for row in range(9):
            for col in range(9):
                value = random.randint(1, 9)
                self.sudoku.insert_number(row, col, value)
                square = self.sudoku._get_square(row, col)
                # Check if the empty_squares count is decreased correctly
                if square.value == -1:
                    expected_empty_squares = self.sudoku.empty_squares + 1
                else:
                    expected_empty_squares = self.sudoku.empty_squares
                self.assertEqual(self.sudoku.empty_squares, expected_empty_squares)

    def test_insert_out_of_range_numbers(self):
        for num in range(-10, 20):
            if num not in range(1, 10):
                for row in range(9):
                    for col in range(9):
                        self.assertFalse(self.sudoku.insert_number(row, col, num))

    def test_insert_number_valid(self):
        for _ in range(10):  # Test 10 random positions for each number
            for num in range(1, 10):
                row, col = random.randint(0, 8), random.randint(0, 8)
                is_valid = self.sudoku.is_number_valid(row, col, num)
                if is_valid:
                    prev_empty_squares = self.sudoku.empty_squares
                    prev_square_value = self.sudoku.get_number(row, col)
                    self.assertTrue(self.sudoku.insert_number(row, col, num))
                    self.assertEqual(self.sudoku.get_number(row, col), num)
                    square = self.sudoku._get_square(row, col)
                    self.assertTrue(square.valid)
                    # Check if the empty_squares count is decreased correctly
                    if prev_square_value == -1:
                        self.assertEqual(self.sudoku.empty_squares, prev_empty_squares - 1)
                    else:
                        self.assertEqual(self.sudoku.empty_squares, prev_empty_squares)
                # Clean up the inserted number for the next iteration
                self.sudoku.remove_number(row, col)

    def test_insert_number_invalid(self):
        for _ in range(10):  # Test 10 random positions for each number
            for num in range(1, 10):
                row, col = random.randint(0, 8), random.randint(0, 8)
                # Insert the number in the same row, column, and box to make it invalid
                self.sudoku.insert_number(row, (col + 1) % 9, num)
                self.sudoku.insert_number((row + 1) % 9, col, num)
                self.sudoku.insert_number((row + 1) % 9, (col + 1) % 9, num)
                is_valid = self.sudoku.is_number_valid(row, col, num)
                if not is_valid:
                    prev_empty_squares = self.sudoku.empty_squares
                    prev_square_value = self.sudoku.get_number(row, col)
                    self.assertTrue(self.sudoku.insert_number(row, col, num))
                    self.assertEqual(self.sudoku.get_number(row, col), num)
                    square = self.sudoku._get_square(row, col)
                    self.assertFalse(square.valid)
                    # Check if the empty_squares count is decreased correctly
                    if prev_square_value == -1:
                        self.assertEqual(self.sudoku.empty_squares, prev_empty_squares - 1)
                    else:
                        self.assertEqual(self.sudoku.empty_squares, prev_empty_squares)
                # Clean up the inserted numbers for the next iteration
                self.sudoku.remove_number(row, (col + 1) % 9)
                self.sudoku.remove_number((row + 1) % 9, col)
                self.sudoku.remove_number((row + 1) % 9, (col + 1) % 9)
                self.sudoku.remove_number(row, col)

    def test_remove_number(self):
        for row in range(9):
            for col in range(9):
                self.sudoku.insert_number(row, col, 1)
                self.sudoku.remove_number(row, col)
                self.assertEqual(self.sudoku.get_number(row, col), -1)

    def test_is_number_valid(self):
        self.sudoku.insert_number(0, 0, 1)
        self.assertFalse(self.sudoku.is_number_valid(0, 1, 1))  # Same row
        self.assertFalse(self.sudoku.is_number_valid(1, 0, 1))  # Same column
        self.assertFalse(self.sudoku.is_number_valid(1, 1, 1))  # Same box
        self.assertTrue(self.sudoku.is_number_valid(0, 1, 2))  # Valid placement

        self.sudoku.insert_number(3, 3, 1)
        self.assertFalse(self.sudoku.is_number_valid(3, 4, 1))  # Same row
        self.assertFalse(self.sudoku.is_number_valid(4, 3, 1))  # Same column
        self.assertFalse(self.sudoku.is_number_valid(4, 4, 1))  # Same box
        self.assertTrue(self.sudoku.is_number_valid(3, 4, 2))  # Valid placement

    def test_value_in_row_col(self):
        for num in range(1, 10):
            self.sudoku.insert_number(0, num - 1, num)
            self.assertTrue(self.sudoku._value_in_row(0, num))
            self.assertFalse(self.sudoku._value_in_row(1, num))
            self.assertTrue(self.sudoku._value_in_col(num - 1, num))
            self.assertFalse(self.sudoku._value_in_col(num - 1, num + 1 if num < 9 else 1))

    def test_reset(self):
        for row in range(9):
            for col in range(9):
                self.sudoku.insert_number(row, col, 1)
        self.sudoku.reset()
        for row in range(9):
            for col in range(9):
                self.assertEqual(self.sudoku.get_number(row, col), -1)

    def test_is_grid_valid(self):
        # Test for an empty grid
        self.assertFalse(self.sudoku.is_grid_valid())

        # Test for a grid with some random values
        self.sudoku.insert_number(0, 0, 1)
        self.sudoku.insert_number(0, 1, 2)
        self.sudoku.insert_number(1, 0, 3)
        self.sudoku.update_square_validities()
        self.assertFalse(self.sudoku.is_grid_valid())  # Some Squares are still empty

        # Test for an invalid grid
        self.sudoku.insert_number(0, 2, 1)  # Same row
        self.sudoku.update_square_validities()
        self.assertFalse(self.sudoku.is_grid_valid())

        # Test for a valid and filled grid
        # (you can use a pre-filled Sudoku grid that you know is valid)
        valid_filled_grid = [
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
        for row in range(9):
            for col in range(9):
                self.sudoku.insert_number(row, col, valid_filled_grid[row][col])
        self.sudoku.update_square_validities()
        self.assertTrue(self.sudoku.is_grid_valid())

    def test_update_square_validities(self):
        # Test for an empty grid
        self.sudoku.update_square_validities()
        for row in range(9):
            for col in range(9):
                square = self.sudoku._get_square(row, col)
                self.assertIsNone(square.valid)

        # Test for a grid with some random values
        self.sudoku.insert_number(0, 0, 1)
        self.sudoku.insert_number(0, 1, 2)
        self.sudoku.insert_number(1, 0, 3)
        self.sudoku.update_square_validities()
        for row in range(9):
            for col in range(9):
                square = self.sudoku._get_square(row, col)
                if square.value != -1:
                    is_valid = self.sudoku.is_number_valid(row, col, square.value)
                    self.assertEqual(square.valid, is_valid)
                else:
                    self.assertIsNone(square.valid)

        # Test for an invalid grid
        self.sudoku.insert_number(0, 2, 1)  # Same row
        self.sudoku.update_square_validities()
        for row in range(9):
            for col in range(9):
                square = self.sudoku._get_square(row, col)
                if square.value != -1:
                    is_valid = self.sudoku.is_number_valid(row, col, square.value)
                    self.assertEqual(square.valid, is_valid)
                else:
                    self.assertIsNone(square.valid)

    def test_update_square_validities_with_invalid_insertions(self):
        # Fill the grid with values that will become invalid after subsequent insertions
        self.sudoku.insert_number(0, 0, 1)
        self.sudoku.insert_number(0, 1, 1)  # Same row
        self.sudoku.insert_number(1, 0, 1)  # Same column
        self.sudoku.insert_number(1, 1, 1)  # Same box

        self.sudoku.update_square_validities()
        self.assertFalse(self.sudoku.is_grid_valid())

        # Continue inserting invalid values
        self.sudoku.insert_number(0, 2, 1)  # Same row
        self.sudoku.insert_number(2, 0, 1)  # Same column
        self.sudoku.insert_number(1, 2, 1)  # Same box
        self.sudoku.insert_number(2, 1, 1)  # Same box

        self.sudoku.update_square_validities()
        self.assertFalse(self.sudoku.is_grid_valid())

        # Add even more invalid values
        for i in range(3, 9):
            self.sudoku.insert_number(0, i, 1)
            self.sudoku.insert_number(i, 0, 1)

        self.sudoku.update_square_validities()
        self.assertFalse(self.sudoku.is_grid_valid())

    def test_win_condition(self):
        # Load a solved Sudoku grid
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
        for row in range(9):
            for col in range(9):
                if (row, col) != (8, 8):
                    self.sudoku.insert_number(row, col, solved_grid[row][col])
        self.sudoku.update_square_validities()
        self.sudoku.insert_number(8, 8, solved_grid[8][8])

        # Ensure that the Sudoku puzzle is solved
        self.assertTrue(self.sudoku.solved)


if __name__ == "__main__":
    unittest.main()
