import pygame
from grid import *
from helper_utils import *
from menu import *
from settings import *


def button_collision(room: Menu | Settings, room_key: str):
    center = None
    target_button = None
    for sprite in sprite_dict.get(room_key):
        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
            center = sprite.rect.center
            break
    if center is not None:
        for button in room.buttons.values():
            if button is not None:
                if button.rect.center == center:
                    target_button = button
                    break
        target_button.pressed()


# base settings
WIDTH = 1280
HEIGHT = 720
FPS = 60
AUTOMODE = False
STATE = "MENU"

# keybinds
KEY_QUIT = pygame.K_q
KEY_FULLSCREEN = pygame.K_f

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# sprite groups
sprite_dict = {
    "grid": pygame.sprite.Group(),
    "box": pygame.sprite.Group(),
    "square": pygame.sprite.Group(),
    "number": pygame.sprite.Group(),
    "square_background": pygame.sprite.Group(),
    "menu": pygame.sprite.Group(),
    "settings": pygame.sprite.Group(),
}

# room objects
menu = None
settings = None
grid = None
grid_pos = (int(WIDTH/2), int(HEIGHT/2))

# selected square
selected = None
selected_value = None
selected_color = None

post(MENU)

while running:
    for event in pygame.event.get():

        # Always
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_QUIT:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            if event.key == KEY_FULLSCREEN:
                pygame.event.post(pygame.event.Event(FULLSCREEN))

        elif event.type == MENU:
            menu = Menu((WIDTH, HEIGHT), sprite_dict)
            settings = None
            grid = None
            STATE = "MENU"
            continue

        elif event.type == SETTINGS:
            menu = None
            settings = Settings((WIDTH, HEIGHT), sprite_dict)
            grid = None
            STATE = "SETTINGS"
            continue

        elif event.type == GAME:
            menu = None
            settings = None
            grid = Grid(grid_pos, 3, 3, 3, 3, sprite_dict)
            STATE = "GAME"
            continue

        elif event.type == MANUAL:
            AUTOMODE = False
        elif event.type == AUTO:
            AUTOMODE = True

        if STATE == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_collision(menu, "menu")
        elif STATE == "SETTINGS":
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_collision(settings, "settings")
        elif STATE == "GAME":
            if not AUTOMODE:
                if event.type == pygame.KEYDOWN:
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
                            selected.set_value(value_of_number_key(event.key), sprite_dict)
                            selected.set_background(selected_color, sprite_dict)
                            selected = None
                            selected_value = None
                    elif selected is not None and event.key is not pygame.K_f:
                        selected.set_value(selected_value, sprite_dict)
                        selected.set_background(selected_color, sprite_dict)
                        selected = None
                        selected_value = None

                if event.type == pygame.MOUSEBUTTONDOWN and selected is None:
                    pressed_square = square_collision(grid, pygame.mouse.get_pos())
                    if pressed_square is not None:
                        selected = pressed_square
                        selected_value = pressed_square.value
                        selected_color = pressed_square.background.color
                        selected.set_value(-1, sprite_dict)
                        selected.set_background(get_color("blue"), sprite_dict)
            else:  # AUTO
                pass

        if event.type == pygame.QUIT:
            running = False
        elif event.type == FULLSCREEN:
            if screen.get_flags() & pygame.FULLSCREEN:
                pygame.display.set_mode((WIDTH, HEIGHT))
            else:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Render
    if STATE == "MENU":
        screen.fill(get_color("gray"))
        sprite_dict.get("menu").draw(screen)
    elif STATE == "SETTINGS":
        screen.fill(get_color("white"))
        sprite_dict.get("settings").draw(screen)
    elif STATE == "GAME":
        screen.fill(get_color("white"))
        for group in [
            "grid",
            "box",
            "square_background",
            "square",
            "number",
        ]:
            sprite_dict.get(group).draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()



