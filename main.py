import os
import pygame as pg
import sys
import time
from math import ceil
from collections import deque

from sprites import Enemy, Tower
from squaregrid import SquareGrid
from message import Message
from user_info import UserInfo
from levels import Levels

# Set the window's position
os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 30"

# Define global variables
# Screen specifications
SCREEN_HEIGHT = 830
SCREEN_WIDTH = 1440
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
HEADING = "Tower Defence"
FPS = 60
# Colors
BLUE = pg.Color('blue1')
LIGHT_BLUE = pg.Color('skyblue2')
RED = pg.Color('red1')
GREEN = pg.Color('green3')
LIGHT_GRAY = pg.Color('gray32')
BROWN = pg.Color('saddlebrown')
LIGHT_BROWN = pg.Color('sandybrown')
# Timers
DT = 0
CURSOR_TIME = 0
TINT = False
TINT_TIME = 0
WAVE_TIME = 0
ENEMY_SPACING = 5
# Other
TILE_SIZE = 30
START_WAVE = False
CREATE_WAVE = False
ENEMY_NUMBER = 0
GG = False
ACTIVE = True


def simple_pathfinder(grid):
    frontier = deque()
    frontier.append(grid.end)
    path = {grid.end: None}
    while len(frontier) > 0:
        current = frontier.popleft()
        new_tiles = grid.find_neighbors(current)
        for tile in new_tiles:
            if tile not in path:
                frontier.append(tile)
                path[tile] = (current[0] - tile[0], current[1] - tile[1])
    return path


def setup_arrows_dictionary():
    # Define a library for the arrows and their rotations
    arrow_dictionary = {}
    arrow_img = pg.image.load('up_arrow.png')
    arrow_img = pg.transform.scale(arrow_img, (TILE_SIZE, TILE_SIZE))
    arrow_dictionary[(0, -1)] = arrow_img
    arrow_dictionary[(0, 1)] = pg.transform.flip(arrow_img, 0, 1)
    arrow_dictionary[(1, 0)] = pg.transform.rotate(arrow_img, 270)
    arrow_dictionary[(-1, 0)] = pg.transform.rotate(arrow_img, 90)
    return arrow_dictionary


pg.init()
# Create a clock
clock = pg.time.Clock()

# Create a screen
pg.display.set_caption(HEADING)
my_screen = pg.display.set_mode(SCREEN_SIZE)

# Define groups
all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()

# Create a UserInfo instance
user = UserInfo(5, 10, 500)

# Define the arrows dictionary
arrows = setup_arrows_dictionary()

# Create an instance of a SquareGrid and set it's start, end, and walls
my_grid = SquareGrid(SCREEN_WIDTH/TILE_SIZE, SCREEN_HEIGHT/TILE_SIZE)
my_grid.start = (0, 11)
my_grid.end = (47, 24)
walls = [(5, 12), (6, 8), (6, 7), (6, 6), (6, 12), (7, 12), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (9, 6), (9, 5), (8, 12), (12, 1), (13, 1), (14, 1), (15, 1), (18, 1), (17, 1), (16, 1), (19, 1), (20, 1), (22, 1), (21, 1), (22, 4), (23, 4), (24, 4), (25, 4), (26, 5), (26, 6), (25, 7), (24, 7), (23, 7), (22, 7), (21, 7), (22, 10), (21, 10), (20, 10), (19, 10), (19, 21), (20, 21), (21, 21), (22, 17), (22, 16), (22, 15), (24, 13), (25, 13), (26, 13), (27, 13), (28, 13), (33, 2), (34, 2), (35, 2), (36, 2), (37, 2), (38, 2), (39, 2), (40, 2), (41, 2), (42, 2), (43, 11), (43, 12), (43, 13), (23, 21), (22, 21), (24, 21), (25, 17), (28, 16), (29, 16), (30, 16), (31, 16), (35, 15), (35, 14), (35, 13), (35, 12), (35, 11), (35, 10), (35, 9), (35, 8), (35, 7), (35, 6), (40, 6), (40, 7), (40, 8), (40, 9), (40, 11), (40, 10), (40, 17), (5, 26), (6, 26), (7, 26), (8, 26), (9, 26), (10, 26), (11, 26), (12, 26), (13, 26), (7, 19), (7, 20), (7, 21), (7, 22), (12, 23), (13, 23), (14, 23), (18, 25), (18, 24), (18, 23), (18, 22), (40, 18), (40, 19), (40, 20), (40, 21), (40, 22), (40, 23), (40, 24), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (18, 10), (6, 10), (7, 5), (9, 3), (21, 3), (27, 9), (16, 12), (12, 24), (22, 19), (29, 14), (33, 8), (40, 4), (41, 12), (42, 21), (13, 15), (12, 15), (11, 15), (10, 15), (9, 15), (10, 18), (9, 18), (8, 18), (10, 17), (6, 5), (7, 24), (9, 4), (26, 4), (26, 7), (17, 10), (14, 15), (7, 23), (15, 23), (18, 21), (22, 18), (40, 5), (7, 18), (4, 12), (8, 11), (8, 10), (8, 9), (8, 8), (8, 7), (9, 7), (7, 4), (7, 3), (7, 2), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3), (16, 3), (18, 3), (17, 3), (19, 3), (20, 3), (22, 3), (23, 1), (24, 2), (24, 1), (25, 2), (26, 2), (27, 2), (28, 2), (28, 3), (28, 4), (28, 5), (28, 6), (28, 7), (28, 8), (28, 9), (26, 9), (25, 9), (24, 9), (23, 9), (22, 9), (20, 8), (19, 8), (20, 7), (18, 8), (17, 8), (16, 8), (15, 8), (16, 10), (16, 11), (16, 13), (16, 14), (16, 15), (16, 16), (16, 17), (15, 17), (14, 17), (13, 17), (12, 17), (11, 17), (8, 16), (7, 16), (6, 16), (5, 16), (8, 15), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (5, 25), (8, 24), (9, 24), (10, 24), (11, 24), (14, 25), (14, 26), (15, 25), (16, 25), (17, 25), (16, 23), (16, 22), (16, 21), (16, 20), (16, 19), (17, 19), (18, 19), (19, 19), (20, 19), (21, 19), (24, 20), (24, 19), (24, 18), (24, 17), (23, 15), (23, 14), (23, 13), (25, 16), (25, 15), (26, 15), (27, 15), (27, 16), (33, 13), (33, 12), (33, 11), (33, 10), (33, 9), (33, 7), (33, 6), (33, 5), (33, 4), (33, 3), (35, 4), (35, 5), (36, 4), (37, 4), (38, 4), (39, 4), (42, 3), (42, 4), (42, 5), (42, 6), (42, 7), (42, 8), (42, 9), (42, 10), (43, 10), (43, 14), (42, 18), (6, 9), (40, 12), (43, 15), (43, 16), (43, 17), (41, 13), (41, 14), (41, 15), (40, 16), (41, 16), (43, 18), (42, 19), (42, 20), (42, 22), (40, 25), (41, 25), (42, 25), (43, 25), (44, 25), (45, 25), (46, 25), (47, 25), (47, 23), (46, 23), (45, 23), (44, 23), (43, 23), (42, 23), (0, 10), (0, 12), (1, 10), (1, 12), (2, 10), (2, 12), (3, 12), (3, 10), (4, 10), (5, 10), (32, 16), (33, 16), (34, 16), (35, 16), (29, 13), (30, 14), (31, 14), (32, 14), (33, 14)]
for wall in walls:
    my_grid.walls.append(wall)
my_grid.path = simple_pathfinder(my_grid)

# Create a Levels instance
my_levels = Levels(my_grid)

# Create an Enemy instance at the start of the grid, not on the map
# my_enemy = Enemy(4, 100, (my_grid.start[0] - 1, my_grid.start[1]), my_grid.start)
# all_sprites.add(my_enemy)
# enemies.add(my_enemy)


def cursor():
    global DT, CURSOR_TIME
    CURSOR_TIME += DT
    """Hide cursor if it is not in motion"""
    if pg.mouse.get_rel()[0] != 0 or pg.mouse.get_rel()[1] != 0:
        pg.mouse.set_visible(True)
        CURSOR_TIME = 0
    else:
        if CURSOR_TIME >= 1:
            pg.mouse.set_visible(False)
            CURSOR_TIME = 0


def draw_grid():
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pg.draw.line(my_screen, LIGHT_GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pg.draw.line(my_screen, LIGHT_GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_walls(grid, surface, color):
    grid.walls = list(filter(grid.in_bounds, grid.walls))
    for w in grid.walls:
        x, y = w[0]*TILE_SIZE, w[1]*TILE_SIZE
        w_rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pg.draw.rect(surface, color, w_rect)


def draw_path(grid, surface, color):
    for tile in grid.path:
        x, y = tile[0]*TILE_SIZE, tile[1]*TILE_SIZE
        r = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pg.draw.rect(surface, color, r)
    # Draw the start and end tiles
    draw_tile(my_screen, my_grid.start, LIGHT_BROWN)
    draw_tile(my_screen, my_grid.end, LIGHT_BROWN)


def draw_tile(surface, tile, color):
    x, y = tile[0]*TILE_SIZE, tile[1]*TILE_SIZE
    r = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
    pg.draw.rect(surface, color, r)


def show_user_info(surface, user_info):
    # Create Message instances to display user info
    wave = Message(surface, (5, 5), ('WAVE ' + str(user_info.wave) + '/' + str(user_info.waves)),
                   font=pg.font.SysFont('comicsansms', 24, True), bg_color=LIGHT_BLUE)
    lives = Message(surface, (5, 35), ('(Ex)Lives: ' + str(user_info.lives)), bg_color=LIGHT_BLUE)
    coins = Message(surface, (5, 60), ('(Test)Coins: ' + str(user_info.coins)), bg_color=LIGHT_BLUE)
    # Blit the info
    wave.blit()
    lives.blit()
    coins.blit()


def check_wave(user_info, group):
    global WAVE_TIME, DT, START_WAVE
    if len(group) == 0:
        WAVE_TIME += DT
        if WAVE_TIME >= 10:
            if user_info.next_wave():
                WAVE_TIME = 0
                START_WAVE = True


def start_wave(user_info, surface):
    global DT, WAVE_TIME, START_WAVE, CREATE_WAVE
    wave = Message(surface, (520, 340), ('WAVE ' + str(user_info.wave) + '/' + str(user_info.waves)),
                   font=pg.font.SysFont('comicsansms', 68, True), bg_color=BROWN)
    rect = wave.rect
    print(rect)
    WAVE_TIME += DT
    if WAVE_TIME <= 3:
        wave.blit()
    else:
        WAVE_TIME = 0
        START_WAVE = False
        CREATE_WAVE = True


def create_wave(user_info, group, level_name):
    global ENEMY_SPACING, DT, ENEMY_NUMBER, CREATE_WAVE
    # Store wave variables
    try:
        wave = eval(level_name + str(user_info.wave))
    except AttributeError:
        return
    spacing = wave[0]
    wave_pause = wave[1]
    pos = wave[2]
    next_tile = wave[3]
    # Create enemy every .2 seconds, with a .5 break every spacing
    pause = 0.2
    if ENEMY_NUMBER % spacing == 0:
        pause += wave_pause
    ENEMY_SPACING += DT
    if ENEMY_SPACING >= pause:
        if ENEMY_NUMBER + 4 < len(wave):
            specs = wave[ENEMY_NUMBER + 4]
            enemy = Enemy(specs[0], specs[1], pos, next_tile)
            all_sprites.add(enemy)
            group.add(enemy)
            ENEMY_NUMBER += 1
            ENEMY_SPACING = 0
        else:
            CREATE_WAVE = False
            ENEMY_NUMBER = 0


def move_enemies(group, grid):
    global DT
    multiplier = DT*TILE_SIZE
    for sprite in group:
        sprite.move(multiplier)
    check_enemies_path(enemies, grid)


def successful_enemies(group, grid, user_info, surface):
    global GG, DT, TINT, TINT_TIME, RED
    for sprite in group:
        if sprite.successful(grid.end):
            user_info.lives -= ceil(sprite.health / 100)
            if user_info.lives <= 0:
                GG = True
            sprite.kill()
            TINT, TINT_TIME = True, 0
    if TINT:
        TINT_TIME += DT
        if TINT_TIME < 0.25:
            draw_tint(RED, surface)


def draw_tint(color, surface):
    # Draw screen with tint
    tint = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    tint.set_alpha(64)
    tint.fill(color)
    surface.blit(tint, (0, 0))


def check_enemies_path(group, grid):
    for sprite in group:
        sprite.check_path(grid)


def draw_group(surface, group):
    global DT
    for sprite in group:
        sprite.draw(surface)


def gg(surface):
    draw_tint(RED, surface)
    gg1 = Message(surface, (520, 280), ' You Lost All   ', font=pg.font.SysFont('comicsansms', 68, True), bg_color=BROWN)
    gg2 = Message(surface, (520, 375), '   Your Lives...', font=pg.font.SysFont('comicsansms', 68, True), bg_color=BROWN)
    gg1.blit()
    gg2.blit()


# Define functions for the main loop
def handle_input():
    """Process and appropriately react to user input"""
    # Regulate frame rate and store frame time in seconds
    global DT
    DT = clock.tick(FPS)/1000
    # Test for a quit command
    for event in pg.event.get():
        if event.type == pg.QUIT:
            global ACTIVE
            ACTIVE = False
        elif not GG:
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos[0]//TILE_SIZE, event.pos[1]//TILE_SIZE
                print(pos)
                if event.button == 1:
                    pass

    pg.event.clear()


def update_screen():
    global START_WAVE
    """Draw an updated version of the screen"""
    cursor()
    my_screen.fill(LIGHT_BLUE)
    # draw_grid()
    draw_walls(my_grid, my_screen, BROWN)
    draw_path(my_grid, my_screen, LIGHT_BROWN)
    check_wave(user, enemies)
    if START_WAVE:
        start_wave(user, my_screen)
    if CREATE_WAVE:
        create_wave(user, enemies, 'my_levels.wave')
    move_enemies(enemies, my_grid)
    draw_group(my_screen, enemies)
    show_user_info(my_screen, user)
    successful_enemies(enemies, my_grid, user, my_screen)
    if GG:
        gg(my_screen)
    pg.display.flip()


def run_game():
    """Main game loop"""
    global ACTIVE
    while ACTIVE:
        handle_input()
        update_screen()
    pg.quit()
    sys.exit()


run_game()
