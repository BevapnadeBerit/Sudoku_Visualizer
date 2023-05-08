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
    for sprite in room.sprite_groups[room_key]:
        if sprite.rect.collidepoint(pygame.mouse.get_pos()):
            center = sprite.rect.center
            break
    if center is not None:
        for button in room.objects.values():
            if button is not None:
                if button.rect.center == center:
                    target_button = button
                    break
        target_button.pressed()


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

menu = None
settings = None
grid = None

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
            menu = Menu(SCREENSIZE)
            settings = None
            grid = None
            STATE = "MENU"
            continue

        elif event.type == SETTINGS:
            menu = None
            settings = Settings(SCREENSIZE)
            grid = None
            STATE = "SETTINGS"
            continue

        elif event.type == GAME:
            menu = None
            settings = None
            grid = Grid(SCREENSIZE, 3, 3, 3, 3)
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
                            select.set_value(value_of_number_key(event.key))
                            select.set_background(select_color)
                            select = None
                            select_value = None

                        elif event.key is not pygame.K_f:
                            select.set_value(select_value)
                            select.set_background(select_color)
                            select = None
                            select_value = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if select is None:
                        pressed_square = square_collision(grid, pygame.mouse.get_pos())
                        if pressed_square is not None:
                            select = pressed_square
                            select_value = pressed_square.value
                            select_color = pressed_square.background.color
                            select.set_value(-1)
                            select.set_background(get_color("blue"))
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

    if STATE == "MENU":
        menu.draw(screen)
    elif STATE == "SETTINGS":
        settings.draw(screen)
    elif STATE == "GAME":
        grid.draw_grid(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()



