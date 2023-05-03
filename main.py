import pygame
from grid import *
from helper_utils import *
from menu import *
from settings import *


def button_collision(room: Menu | Settings, room_key: str):
    """
    Checks if a button is pressed and activates the pressed method on it if true.
    :param room: Room to search in
    :param room_key: sprite group to search in
    """
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


def draw(surface: pygame.Surface, color: str, sprite_groups: dict[str, pygame.sprite.Group], *group_keys: str):
    """
    Draws a number of sprite groups onto a Surface with a background of given color.
    :param surface: Surface to draw onto
    :param color: color of the background
    :param sprite_groups: sprite group dict
    :param group_keys: keys to the sprite groups to draw
    :return:
    """
    surface.fill(get_color(color))
    for key in group_keys:
        sprite_groups.get(key).draw(surface)


# States
STATE = "MENU"
AUTOMODE = False

# settings
SCREENSIZE = (WIDTH, HEIGHT)

# key-binds
KEY_QUIT = pygame.K_q

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
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

# selected square
select = None
select_value = None
select_color = None

post(MENU)

while running:
    for event in pygame.event.get():

        # Always
        if event.type == pygame.KEYDOWN:
            if event.key == KEY_QUIT:
                post(pygame.QUIT)

        elif event.type == MENU:
            menu = Menu(SCREENSIZE, sprite_dict)
            settings = None
            grid = None
            STATE = "MENU"
            continue

        elif event.type == SETTINGS:
            menu = None
            settings = Settings(SCREENSIZE, sprite_dict)
            grid = None
            STATE = "SETTINGS"
            continue

        elif event.type == GAME:
            menu = None
            settings = None
            grid = Grid(SCREENSIZE, 3, 3, 3, 3, sprite_dict)
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
                    if select:
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
                            select.set_value(value_of_number_key(event.key), sprite_dict)
                            select.set_background(select_color, sprite_dict)
                            select = None
                            select_value = None

                        elif event.key is not pygame.K_f:
                            select.set_value(select_value, sprite_dict)
                            select.set_background(select_color, sprite_dict)
                            select = None
                            select_value = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if select is None:
                        pressed_square = square_collision(grid, pygame.mouse.get_pos())
                        if pressed_square is not None:
                            select = pressed_square
                            select_value = pressed_square.value
                            select_color = pressed_square.background.color
                            select.set_value(-1, sprite_dict)
                            select.set_background(get_color("blue"), sprite_dict)
            else:  # AUTO
                pass

        if event.type == pygame.QUIT:
            running = False
        elif event.type == FULLSCREEN:
            if screen.get_flags() & pygame.FULLSCREEN:
                SCREENSIZE = (WIDTH, HEIGHT)
                pygame.display.set_mode(SCREENSIZE)
            else:
                pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                SCREENSIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            print("CHANGE")
            print(SCREENSIZE)

    # Render
    if STATE == "MENU":
        draw(screen, "gray", sprite_dict, "menu")
    elif STATE == "SETTINGS":
        draw(screen, "gray", sprite_dict, "settings")
    elif STATE == "GAME":
        draw(screen, "white", sprite_dict,
             "grid",
             "box",
             "square_background",
             "square",
             "number",
             )

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()



