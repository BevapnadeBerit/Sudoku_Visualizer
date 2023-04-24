import pygame


class Grid:
    def __init__(self, grid_pos: tuple[int, int], v_boxes: int, h_boxes: int, box_width: int, box_height: int):
        self.pos: pygame.Vector2 = pygame.Vector2(grid_pos)
        self.boxes: dict[tuple[int, int], Box] = {}
        for h in range(h_boxes):
            for v in range(v_boxes):
                box_pos: tuple[int, int] = (h, v)
                self.boxes[box_pos] = Box(box_pos, box_width, box_height)


class Box:
    def __init__(self, box_pos: tuple[int, int], width: int, height: int):
        self.pos: pygame.Vector2 = pygame.Vector2(box_pos)
        self.squares: dict[tuple[int, int], Square] = {}
        for x in range(width):
            for y in range(height):
                square_pos = (x, y)
                self.squares[square_pos] = Square(square_pos)


class Square:
    def __init__(self, square_pos: tuple[int, int], value=-1):
        self.pos: pygame.Vector2 = pygame.Vector2(square_pos)
        self.value: int = value
