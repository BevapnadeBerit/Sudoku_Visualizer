import pygame
from grid import *
from helper_utils import *
from menu import *
from settings import *
from game import *


def button_collision(room: Menu | Settings | Game, group_key: str):
    """
    Checks if a button is pressed and activates the pressed method on it if true.
    :param room: Room to search in
    :param group_key: sprite group to search in
    """
    center = None
    target_button = None
    for sprite in room.sprite_groups[group_key]:
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
DIFFICULTY = "EASY"
AUTOMODE = False

# settings
SCREENSIZE = (WIDTH, HEIGHT)

# key-binds
KEY_QUIT = pygame.K_q
KEY_MENU = pygame.K_ESCAPE

# pygame setup
pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
clock = pygame.time.Clock()
running = True

menu = None
settings = None
game = None

select = None
select_value = None
select_color = None

post(MENU)

while running:
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == KEY_QUIT:
                post(pygame.QUIT)
            if event.key == KEY_MENU:
                if STATE != "MENU":
                    post(MENU)

        elif event.type == MENU:
            menu = Menu(SCREENSIZE)
            settings = None
            game = None
            STATE = "MENU"
            continue

        elif event.type == SETTINGS:
            menu = None
            settings = Settings(SCREENSIZE)
            game = None
            STATE = "SETTINGS"
            continue

        elif event.type == GAME:
            menu = None
            settings = None
            game = Game(SCREENSIZE, screen)
            STATE = "GAME"
            continue
        elif event.type == DEMO:
            menu = None
            settings = None
            # game = Demo(SCREENSIZE)
            STATE = "GAME"

        elif event.type == MANUAL:
            AUTOMODE = False
        elif event.type == AUTO:
            AUTOMODE = True

        elif event.type == GENERATE:
            print("GENERATE")
            game.sudoku.generate_puzzle(DIFFICULTY)
        elif event.type == SOLVE:
            print("SOLVE")
            game.sudoku.solve()
        elif event.type == CLEAR:
            print("CLEAR")
            game.sudoku.clear()
        elif event.type == RESET:
            print("RESET")
            game.sudoku.reset()

        elif event.type == EASY:
            DIFFICULTY = "EASY"
        elif event.type == MEDIUM:
            DIFFICULTY = "MEDIUM"
        elif event.type == HARD:
            DIFFICULTY = "HARD"

        if STATE == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_collision(menu, "menu_ui")
        elif STATE == "SETTINGS":
            if event.type == pygame.MOUSEBUTTONDOWN:
                button_collision(settings, "settings_ui")
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

                        else:
                            select.set_value(select_value)
                            select.set_background(select_color)
                            select = None
                            select_value = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if select:
                        select.set_value(select_value)
                        select.set_background(select_color)
                        select = None
                        select_value = None

                    pressed_square = square_collision(game.objects["grid"], pygame.mouse.get_pos())
                    if pressed_square is not None:
                        select = pressed_square
                        select_value = pressed_square.value
                        select_color = pressed_square.background.color
                        select.set_value(-1)
                        select.set_background(get_color("blue"))
                    else:
                        button_collision(game, "game_ui")
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
        game.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()



