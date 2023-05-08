import copy
import random

class SudokuGenerator:

    def __init__(self):
        self.grid = [[-1 for _ in range(9)] for _ in range(9)]

    def generate_puzzle(self):
        self.__generate_random_diagonal()

    def __solve(self, grid):
        row, col = self.__find_empty(grid)

        if row == -1 or col == -1:
            return True

        for num in range(1, 10):
            random_num = random.randint(1, 9)
            if self.__is_valid(grid, row, col, random_num):
                grid[row][col] = random_num

                if self.__solve(grid):
                    return True

                grid[row][col] = -1

        return False
    
    def __generate_random_diagonal(self): #Completely new puzzle, with three boxes filled in on the diagonal
        self.__resetGrid()

        num_range = list(range(1, 10))
        for row in range(3):
            for col in range(3):
                num = random.choice(num_range)
                self.grid[row][col] = num
                num_range.remove(num)

        num_range = list(range(1, 10))
        for row in range(3, 6):
            for col in range(3, 6):
                num = random.choice(num_range)
                self.grid[row][col] = num
                num_range.remove(num)

        num_range = list(range(1, 10))
        for row in range(6, 9):
            for col in range(6, 9):
                num = random.choice(num_range)
                self.grid[row][col] = num
                num_range.remove(num)

        return self.__fill_in_after_diagonal()

    def __fill_in_after_diagonal(self): # Finish generating board after the diagonal boxes.
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == -1:
                    num = random.randint(1, 9)

                    if self.__is_valid(self.grid, row, col, num):
                        self.grid[row][col] = num

                        if self.__solve(self.grid):
                            self.__fill_in_after_diagonal()
                            return True

                        self.grid[row][col] = -1

        return False

    def __resetGrid(self):
        self.grid = [[-1 for _ in range(9)] for _ in range(9)]

    def __find_empty(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == -1:
                    return row, col
        return -1, -1

    def __is_valid(self, grid, row, col, num):
        return not self.__in_row(grid, row, num) and \
               not self.__in_col(grid, col, num) and \
               not self.__in_box(grid, row - row % 3, col - col % 3, num)

    def __in_row(self, grid, row, num):
        return num in grid[row]

    def __in_col(self, grid, col, num):
        return num in [grid[row][col] for row in range(9)]

    def __in_box(self, grid, start_row, start_col, num):
        for row in range(3):
            for col in range(3):
                if grid[row + start_row][col + start_col] == num:
                    return True
        return False

    def __format_cell(self, value):
        return str(value) if value != -1 else ' '

    def print_grid(self, grid):
        for row in range(9):
            if row % 3 == 0 and row != 0:
                print('-' * 19)
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    print('|', end='')
                cell = self.__format_cell(grid[row][col])
                if col == 8:
                    print(' ' + cell)
                elif col % 3 == 0 and col != 0:
                    print(cell, end='')
                else:
                    print(' ' + cell, end='')

if __name__ == '__main__':
    generator = SudokuGenerator()
    generator.generate_puzzle()
    generator.print_grid(generator.grid)
