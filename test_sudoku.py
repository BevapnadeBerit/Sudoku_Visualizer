#Generated with ChatGPT

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

    def test_insert_invalid_numbers(self):
        for num in range(-10, 20):
            if num not in range(1, 10):
                for row in range(9):
                    for col in range(9):
                        self.assertFalse(self.sudoku.insert_number(row, col, num))

    def test_insert_valid_numbers(self):
        for num in range(1, 10):
            for _ in range(10):  # Test 10 random positions for each number
                row, col = random.randint(0, 8), random.randint(0, 8)
                is_valid = self.sudoku.is_number_valid(row, col, num)
                is_inserted = self.sudoku.insert_number(row, col, num)
                self.assertEqual(is_inserted, is_valid)
                # Clean up the inserted number for the next iteration
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
        self.assertTrue(self.sudoku.is_number_valid(0, 1, 2))   # Valid placement

        self.sudoku.insert_number(3, 3, 1)
        self.assertFalse(self.sudoku.is_number_valid(3, 4, 1))  # Same row
        self.assertFalse(self.sudoku.is_number_valid(4, 3, 1))  # Same column
        self.assertFalse(self.sudoku.is_number_valid(4, 4, 1))  # Same box
        self.assertTrue(self.sudoku.is_number_valid(3, 4, 2))   # Valid placement

    def test_value_in_row_col(self):
        for num in range(1, 10):
            self.sudoku.insert_number(0, num - 1, num)
            self.assertTrue(self.sudoku._value_in_row(0, num))
            self.assertFalse(self.sudoku._value_in_row(1, num))
            self.assertTrue(self.sudoku._value_in_col(num - 1, num))
            self.assertFalse(self.sudoku._value_in_col(num - 1, num + 1 if num < 9 else 1))

if __name__ == "__main__":
    unittest.main()

