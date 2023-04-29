# Simple demo of the Sudoku class for manual testing.

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
    grid_pos = (int(WIDTH/2), int(HEIGHT/2))
    grid = Grid(grid_pos, 3, 3, 3, 3, grid_sprites)
    sudoku = Sudoku(grid, grid_pos)

    # Test the insert_number method
    row = 1
    col = 1
    num = 5

    box = grid.boxes[row // 3][col // 3]
    square = box.squares[row % 3][col % 3]
    sudoku.insert_number(square, num)
    print(f"Inserted number {num} at row {row}, column {col}.")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        # Render the grid
        grid_sprites.update()
        grid_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
