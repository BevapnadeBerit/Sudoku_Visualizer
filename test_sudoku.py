#Generated with ChatGPT

import unittest
from grid import Grid, Square, Box
from sudoku import Sudoku

import pygame
pygame.init()
pygame.display.set_mode((1, 1))

class TestSudoku(unittest.TestCase):

    def setUp(self):
        grid_pos = (0, 0)
        self.grid = Grid(grid_pos, 3, 3, 3, 3)
        self.sudoku = Sudoku(self.grid, grid_pos)

    def test_insert_number(self):
        for row in range(9):
            for col in range(9):
                for num in range(1, 10):
                    self.sudoku.remove_number(row, col)  # Clear the square before each insertion attempt
                    if self.sudoku.is_number_valid(row, col, num):
                        self.assertTrue(self.sudoku.insert_number(row, col, num))
                        self.assertEqual(self.sudoku.get_number(row, col), num)
                    else:
                        self.assertFalse(self.sudoku.insert_number(row, col, num))

    def test_insert_only_valid_numbers(self):
        for row in range(9):
            for col in range(9):
                for num in range(-5, 15):  # Test numbers outside the valid range
                    if 1 <= num <= 9:
                        continue  # Skip valid numbers, since they are tested in test_insert_number
                    self.assertFalse(self.sudoku.insert_number(row, col, num))
                    self.assertNotEqual(self.sudoku.get_number(row, col), num)

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
        self.assertTrue(self.sudoku.is_number_valid(0, 1, 2))   # Valid placement

        self.sudoku.insert_number(3, 3, 1)
        self.assertFalse(self.sudoku.is_number_valid(3, 4, 1))  # Same row
        self.assertFalse(self.sudoku.is_number_valid(4, 3, 1))  # Same column
        self.assertFalse(self.sudoku.is_number_valid(4, 4, 1))  # Same box
        self.assertTrue(self.sudoku.is_number_valid(3, 4, 2))   # Valid placement

    def test_value_in_row_col(self):
        self.sudoku.insert_number(0, 0, 1)
        self.assertTrue(self.sudoku._value_in_row(0, 1))
        self.assertFalse(self.sudoku._value_in_row(0, 2))
        self.assertTrue(self.sudoku._value_in_col(0, 1))
        self.assertFalse(self.sudoku._value_in_col(1, 1))

        self.sudoku.insert_number(3, 3, 1)
        self.assertTrue(self.sudoku._value_in_row(3, 1))
        self.assertFalse(self.sudoku._value_in_row(3, 2))
        self.assertTrue(self.sudoku._value_in_col(3, 1))
        self.assertFalse(self.sudoku._value_in_col(4, 1))

if __name__ == "__main__":
    unittest.main()

