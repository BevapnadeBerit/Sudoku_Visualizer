import os

import pygame

GRID_OUTLINE = 30
BOX_OUTLINE = 2

SQUARE_SIZE = 60
BOX_SIZE = 3 * SQUARE_SIZE + 2 * BOX_OUTLINE
GRID_SIZE = 3 * BOX_SIZE + 2 * GRID_OUTLINE


# The grid class contains other smaller parts that all together make up the sudoku grid
class Grid(pygame.sprite.Sprite):
    def __init__(self, grid_pos: tuple[int, int], v_boxes: int, h_boxes: int, box_width: int, box_height: int,
                 group: pygame.sprite.Group):
        super().__init__(group)

        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill("gray")
        self.rect = self.image.get_rect()
        self.rect.center = grid_pos

        self.boxes: [[Box]] = []
        for h in range(h_boxes):
            current_array = []
            for v in range(v_boxes):
                box_pos = (grid_pos[0] + (h - 1) * BOX_SIZE, grid_pos[1] + (v - 1) * BOX_SIZE)
                current_array.append(Box(box_pos, box_width, box_height, group))
            self.boxes.append(current_array)


class Box(pygame.sprite.Sprite):
    def __init__(self, box_pos: tuple[int, int], width: int, height: int, group: pygame.sprite.Group):
        super().__init__(group)

        self.image = pygame.Surface((BOX_SIZE, BOX_SIZE))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.rect.center = box_pos

        self.squares: [[Square]] = []
        for x in range(width):
            current_array = []
            for y in range(height):
                square_pos = (box_pos[0] + (x - 1) * SQUARE_SIZE, box_pos[1] + (y - 1) * SQUARE_SIZE)
                current_array.append(Square(square_pos, group))
            self.squares.append(current_array)


class Square(pygame.sprite.Sprite):
    def __init__(self, square_pos: tuple[int, int], group: pygame.sprite.Group, value=0):
        super().__init__(group)

        file_path = os.path.join("images", "square.png")
        image = pygame.image.load(file_path)
        image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

        self.pos = square_pos
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
        self.number = Number(self.pos, value, group)


class Number(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], value: int, group: pygame.sprite.Group):
        super().__init__(group)
        if value not in range(1, 10):
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
