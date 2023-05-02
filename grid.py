import os

import pygame
from  pygame import Vector2

GRID_OUTLINE = 30
BOX_OUTLINE = 2

# All sizes must be even
SQUARE_SIZE = 60
BOX_SIZE = 3 * SQUARE_SIZE + 2 * BOX_OUTLINE
GRID_SIZE = 3 * BOX_SIZE + 2 * GRID_OUTLINE


# The grid class contains other smaller parts that all together make up the sudoku grid
class Grid(pygame.sprite.Sprite):
    """
    A grid containing a 3x3 2d array of boxes.
    """
    def __init__(self, grid_pos: tuple[int, int], v_boxes: int, h_boxes: int, box_width: int, box_height: int,
                 group: pygame.sprite.Group):
        super().__init__(group)

        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill("gray")
        self.rect = self.image.get_rect()
        self.rect.center = grid_pos

        self.boxes = []
        for v in range(v_boxes):
            current_array = []
            for h in range(h_boxes):
                box_pos = (grid_pos[0] + (h - 1) * BOX_SIZE, grid_pos[1] + (v - 1) * BOX_SIZE)
                current_array.append(Box(box_pos, box_width, box_height, group, box_row=v, box_col=h))
            self.boxes.append(current_array)


class Box(pygame.sprite.Sprite):
    """
    A box containing a 3x3 2d array of squares.
    """
    def __init__(self, box_pos: tuple[int, int], width: int, height: int, group: pygame.sprite.Group,
                 box_row: int, box_col: int):
        super().__init__(group)

        self.image = pygame.Surface((BOX_SIZE, BOX_SIZE))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.rect.center = box_pos

        self.squares = []
        for y in range(height):
            current_array = []
            for x in range(width):
                square_pos = (box_pos[0] + (x - 1) * SQUARE_SIZE, box_pos[1] + (y - 1) * SQUARE_SIZE)
                row = box_row * height + y
                col = box_col * width + x
                current_array.append(Square(square_pos, group, row=row, col=col))
            self.squares.append(current_array)


class Square(pygame.sprite.Sprite):
    """
    A square with a value which is represented by an instance of the Number class if in the range of 0-9.
    """
    def __init__(self, square_pos: tuple[int, int], group: pygame.sprite.Group, value=-1, row=-1, col=-1):
        super().__init__(group)

        file_path = os.path.join("images", "square.png")
        image = pygame.image.load(file_path)
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

        self.pos = square_pos
        self.row = row
        self.col = col
        self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.blit(image, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = square_pos

        self.value = None
        self.number = None
        self.set_value(value, group)

    def set_value(self, value: int, group: pygame.sprite.Group):
        self.value = value
        if self.number is not None:
            self.number.kill()
        if self.value == -1:
            self.number = None
        else:
            self.number = Number(self.pos, value, group)


class Number(pygame.sprite.Sprite):
    """
    An image showing the content of related square.
    """
    def __init__(self, pos: tuple[int, int], value: int, group: pygame.sprite.Group):
        super().__init__(group)
        if value not in range(0, 10):
            self.kill()
        else:
            file = "number_" + str(value) + ".png"
            file_path = os.path.join("images", file)
            image = pygame.image.load(file_path).convert_alpha()
            image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

            self.image = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            self.image.blit(image, (0, 0))
            self.rect = self.image.get_rect()
            self.rect.center = pos


def square_collision(grid: Grid, pos: tuple[int, int]) -> Square | None:
    """
    Searches for collision with square in grid at pos.
    :param grid: The grid to search
    :param pos: The position to compare
    :return: The collision Square, or None if no collision.
    """

    v = Vector2(pos)
    half_box = int(BOX_SIZE / 2)
    box_x = None
    box_y = None

    # Search for box
    for row in grid.boxes:
        box = row[0]
        d = v - Vector2(box.rect.center)
        if d.y in range(-half_box, half_box):
            box_y = grid.boxes.index(row)
            break
    for box in grid.boxes[0]:
        d = v - Vector2(box.rect.center)
        if d.x in range(-half_box, half_box):
            box_x = grid.boxes[0].index(box)
            break

    if box_x is None or box_y is None:
        return None

    # Found box
    box = grid.boxes[box_y][box_x]

    # Search for square
    v = Vector2(pos)
    half_square = int(SQUARE_SIZE / 2)
    square_x = None
    square_y = None

    for row in box.squares:
        square = row[0]
        d = v - Vector2(square.rect.center)
        if d.y in range(-half_square, half_square):
            square_y = box.squares.index(row)
            break
    for square in box.squares[0]:
        d = v - Vector2(square.rect.center)
        if d.x in range(-half_square, half_square):
            square_x = box.squares[0].index(square)
            break

    print(square_x)
    print(square_y)
    if square_x is None or square_y is None:
        return None

    return box.squares[square_y][square_x]
