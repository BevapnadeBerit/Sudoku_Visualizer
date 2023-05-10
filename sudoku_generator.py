import random

class SudokuGenerator:

    def __init__(self):
        self.grid = [[-1 for _ in range(9)] for _ in range(9)]
        self.solution = None

    def generate_puzzle(self, hints: int) -> None:
        success = False
        while not success:
            self.__generate_random_diagonal()
            self.solution = [row.copy() for row in self.grid]
            success = self.__remove_numbers(hints)

    def __solve(self, grid: list[list[int]]) -> bool:
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
    
    def __is_valid_grid(self, grid: list[list[int]]) -> bool:
        for row in range(9):
            for col in range(9):
                num = grid[row][col]
                if num != -1:
                    grid[row][col] = -1
                    if not self.__is_valid(grid, row, col, num):
                        grid[row][col] = num
                        return False
                    grid[row][col] = num
        return True
    
    def __generate_random_diagonal(self) -> bool: #Completely new puzzle, with three boxes filled in on the diagonal
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

    def __fill_in_after_diagonal(self) -> bool:
        row, col = self.__find_empty(self.grid)
        if row == -1 or col == -1:
            return True

        for num in range(1, 10):
            if self.__is_valid(self.grid, row, col, num):
                self.grid[row][col] = num

                if self.__fill_in_after_diagonal():
                    return True

                self.grid[row][col] = -1

        return False
    
    def __remove_numbers(self, hints: int) -> bool:
        remaining_positions = {(row, col) for row in range(9) for col in range(9)}
        original_grid = [row.copy() for row in self.grid]

        restart_count = 0
        while len(remaining_positions) > hints:
            position = random.choice(list(remaining_positions))
            row, col = position
            temp_val = self.grid[row][col]
            self.grid[row][col] = -1

            grid_copy = [row.copy() for row in self.grid]
            solutions = self.__count_solutions(grid_copy)

            if solutions == 1:
                remaining_positions.remove(position)
            else:
                self.grid[row][col] = temp_val

            if len(remaining_positions) == hints:
                break

            if len(remaining_positions) == 0:
                remaining_positions = {(row, col) for row in range(9) for col in range(9)}
                self.grid = [row.copy() for row in original_grid]
                restart_count += 1

                if restart_count > 1:
                    return False

        return True

    def __count_solutions(self, grid: list[list[int]], count=0) -> int:
        row, col = self.__find_empty(grid)

        if row == -1 or col == -1:
            return count + 1

        for num in range(1, 10):
            if self.__is_valid(grid, row, col, num):
                grid[row][col] = num

                count = self.__count_solutions(grid, count)

                if count > 1:
                    break

                grid[row][col] = -1

        return count

    def __resetGrid(self) -> None:
        self.grid = [[-1 for _ in range(9)] for _ in range(9)]

    def __find_empty(self, grid: list[list[int]]) -> tuple[int, int]:
        for row in range(9):
            for col in range(9):
                if grid[row][col] == -1:
                    return row, col
        return -1, -1

    def __is_valid(self, grid: list[list[int]], row: int, col: int, num: int) -> bool:
        return all([
            not self.__in_row(grid, row, num),
            not self.__in_col(grid, col, num),
            not self.__in_box(grid, row - row % 3, col - col % 3, num)
        ])

    def __in_row(self, grid: list[list[int]], row: int, num: int) -> bool:
        return any(cell == num for cell in grid[row])

    def __in_col(self, grid: list[list[int]], col: int, num: int) -> bool:
        return any(grid[row][col] == num for row in range(9))

    def __in_box(self, grid: list[list[int]], start_row: int, start_col: int, num: int) -> bool:
        return any(
            grid[row + start_row][col + start_col] == num
            for row in range(3)
            for col in range(3)
        )

    def __format_cell(self, value: int) -> str:
        return str(value) if value != -1 else ' '
    
    def __grid_to_str(self, grid: list[list[int]]) -> str:
        grid_str = []
        for row in range(9):
            if row % 3 == 0 and row != 0:
                grid_str.append('-' * 19)
            row_str = []
            for col in range(9):
                if col % 3 == 0 and col != 0:
                    row_str.append('|')
                cell = self.__format_cell(grid[row][col])
                row_str.append(' ' + cell)
            grid_str.append(''.join(row_str))
        return '\n'.join(grid_str)

    def __print_grid(self, grid: list[list[int]]) -> None:
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

    def print_puzzle(self) -> None:
        print("Puzzle:")
        self.__print_grid(self.grid)
        
    def print_solution(self) -> None:
        print("Solution:")
        self.__print_grid(self.solution)

if __name__ == '__main__':
    generator = SudokuGenerator()
    generator.generate_puzzle(29)
    generator.print_puzzle()
    generator.print_solution()
