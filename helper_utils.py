import pygame


def value_of_number_key(key: int):
    """
    Returns the represented value of a Event.key that is a number.
    :param key: The Event.key to be translated
    :return: The translated value
    """
    return key - pygame.K_1 + 1
