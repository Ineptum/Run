import pygame
from classes.player import Player
from classes.tile import Tile
import sys

tile_render = {'|': 'v', '-': 'h', '/': 'lu',
               '\\': 'ru', '<': 'ld', '>': 'rd',
               'L': 'dlu', 'R': 'urd', 'T': 'lur',
               'B': 'ldr', 'i': 'invert'}


def load_level(filename):
    with open("levels/" + filename) as mapFile:
        level_map = [line.rstrip() for line in mapFile]

    max_width = max(map(len, level_map))
    max_height = len(level_map)

    return list(map(lambda x: x.ljust(max_width, '.'), level_map)), max_width, max_height


def generate_level(level, all_sprites, tile_group, player_group, tile_size):
    player1, player2, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] in " .":
                pass
            elif level[y][x] == 'p':
                player1 = Player("Player 1", x, y,
                                 all_sprites, player_group, pygame.transform.scale(
                                     load_image('Player1.png', -1),
                                     tuple(map(int, (tile_size * 0.8, tile_size * 0.8)))), tile_size)
            elif level[y][x] == 'q':
                player2 = Player("Player 2", x, y,
                                 all_sprites, player_group, pygame.transform.scale(
                                     load_image('Player2.png', -1),
                                     tuple(map(int, (tile_size * 0.8, tile_size * 0.8)))), tile_size)
            else:
                Tile(tile_render[level[y][x]],
                     x, y, all_sprites, tile_group,
                     pygame.transform.scale(load_image(tile_render[level[y][x]] + '.png'),
                                            (tile_size, tile_size)), tile_size)

    return player1, player2


def load_image(name, colorkey=None):
    try:
        image = pygame.image.load("data/" + name)
    except Exception as exception:
        print("Cannot load image: {}".format(name))
        raise SystemExit(exception)

    image = image.convert_alpha()
    if colorkey:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()
