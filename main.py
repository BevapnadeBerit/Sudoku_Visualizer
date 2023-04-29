import pygame
from grid import *
from helper_utils import *
from random import choice, randint

# base settings
WIDTH = 1280
HEIGHT = 720
FPS = 60
MANUAL = False

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# sprite groups
grid_sprites = pygame.sprite.Group()

# grid
grid_pos = (int(WIDTH/2), int(HEIGHT/2))
grid = Grid(grid_pos, 3, 3, 3, 3, grid_sprites)

# selected square
selected = None
selected_value = None

# custom events
FULLSCREEN = pygame.USEREVENT + 1

while running:
    for event in pygame.event.get():
        if MANUAL:
            # Checks for Input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                if event.key == pygame.K_f:
                    pygame.event.post(pygame.event.Event(FULLSCREEN))

                if event.key in [
                    pygame.K_1,
                    pygame.K_2,
                    pygame.K_3,
                    pygame.K_4,
                    pygame.K_5,
                    pygame.K_6,
                    pygame.K_7,
                    pygame.K_8,
                    pygame.K_9,
                ]:
                    if selected is not None:
                        selected.set_value(value_of_number_key(event.key), grid_sprites)
                        selected = None
                        selected_value = None
                elif selected is not None and event.key is not pygame.K_f:
                    selected.set_value(selected_value, grid_sprites)
                    selected = None
                    selected_value = None

            if event.type == pygame.MOUSEBUTTONDOWN and selected is None:
                pressed_square = square_collision(grid, pygame.mouse.get_pos())
                if pressed_square is not None:
                    selected = pressed_square
                    selected_value = pressed_square.value
                    selected.set_value(0, grid_sprites)
        else:  # AUTO
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                if event.key == pygame.K_f:
                    pygame.event.post(pygame.event.Event(FULLSCREEN))

                if event.key == pygame.K_r:
                    for box_x in grid.boxes:
                        for box in box_x:
                            for square_x in box.squares:
                                for square in square_x:
                                    square.set_value(randint(1, 9), grid_sprites)

        if event.type == pygame.QUIT:
            running = False

        # Checks for fullscreen event
        elif event.type == FULLSCREEN:
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode((WIDTH, HEIGHT))
            else:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # CGPT

    screen.fill("white")

    # RENDER YOUR GAME HERE
    grid_sprites.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)  # limits FPS to 60

pygame.quit()
