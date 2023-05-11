# Simple demo of the Sudoku class for manual testing.
# Partially generated with ChatGPT.

import pygame
from grid import Grid, Square
from sudoku import Sudoku

WIDTH = 1280
HEIGHT = 720
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    # Create a sprite group
    grid_sprites = pygame.sprite.Group()

    # Create a grid and Sudoku instance
    grid_pos = (int(WIDTH / 2), int(HEIGHT / 2))
    grid = Grid(grid_pos, 3, 3, 3, 3, grid_sprites)
    sudoku = Sudoku(grid, grid_pos)

    def update_screen(screen, sprites):
        sprites.update()
        sprites.draw(screen)
        pygame.display.flip()
        pygame.time.delay(100)

    def test_insert_remove_all():
        # Test inserting and removing a value for each Square
        for row in range(9):
            for col in range(9):
                num = (row * 3 + col) % 9 + 1
                if sudoku.insert_number(row, col, num):
                    print(f"Inserted number {num} at row {row}, column {col}.")
                else:
                    print(f"Skipped inserting invalid number {num} at row {row}, column {col}.")
                update_screen(screen, grid_sprites)
                sudoku.remove_number(row, col)
                print(f"Removed number {num} at row {row}, column {col}.")

    def test_validity():
        # Test the insert_number method for top-left Box
        for row in range(3):
            for col in range(3):
                num = (row * 3 + col) % 9 + 1
                sudoku.insert_number(row, col, num)
                print(f"Inserted number {num} at row {row}, column {col}.")
                update_screen(screen, grid_sprites)

        # Test the insert_number method for bottom-right Box
        for row in range(6, 9):
            for col in range(6, 9):
                num = ((row - 6) * 3 + (col - 6)) % 9 + 1
                sudoku.insert_number(row, col, num)
                print(f"Inserted number {num} at row {row}, column {col}.")
                update_screen(screen, grid_sprites)

        # Test some additional insertions and removals for top-left Box
        if sudoku.insert_number(0, 0, 2):
            print(f"Inserted number 2 at row 0, column 0.")
        else:
            print(f"Skipped inserting invalid number 2 at row 0, column 0.")
        update_screen(screen, grid_sprites)
        if sudoku.insert_number(3, 0, 1):
            print(f"Inserted number 1 at row 3, column 1.")
        else:
            print(f"Skipped inserting invalid number 1 at row 3, column 1.")
        update_screen(screen, grid_sprites)
        sudoku.remove_number(0, 0)
        print(f"Removed number 1 at row 0, column 0.")
        update_screen(screen, grid_sprites)
        if sudoku.insert_number(3, 0, 1):
            print(f"Inserted number 1 at row 3, column 0.")
        else:
            print(f"Skipped inserting invalid number 1 at row 3, column 1.")
        update_screen(screen, grid_sprites)

        # Test some additional insertions and removals for bottom-right Box
        if sudoku.insert_number(6, 6, 2):
            print(f"Inserted number 2 at row 6, column 6.")
        else:
            print(f"Skipped inserting invalid number 2 at row 6, column 6.")
        update_screen(screen, grid_sprites)
        if sudoku.insert_number(6, 5, 1):
            print(f"Inserted number 1 at row 6, column 5.")
        else:
            print(f"Skipped inserting invalid number 1 at row 6, column 5.")
        update_screen(screen, grid_sprites)
        sudoku.remove_number(6, 6)
        print(f"Removed number 1 at row 6, column 6.")
        update_screen(screen, grid_sprites)
        if sudoku.insert_number(6, 5, 1):
            print(f"Inserted number 1 at row 6, column 5.")
        else:
            print(f"Skipped inserting invalid number 1 at row 6, column 5.")
        update_screen(screen, grid_sprites)

    # Add a flag to ensure tests run only once
    tests_done = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        # Render the grid
        grid_sprites.update()
        grid_sprites.draw(screen)

        # Place the tests inside the game loop
        if not tests_done:
            test_insert_remove_all()
            test_validity()

            """sudoku.insert_number(8, 6, 1)
            update_screen(screen, grid_sprites)
            sudoku.insert_number(0, 1, 1)
            update_screen(screen, grid_sprites)
            sudoku.insert_number(5, 3, 1)
            update_screen(screen, grid_sprites)"""

            # Set tests_done flag to True after tests are complete
            tests_done = True

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
