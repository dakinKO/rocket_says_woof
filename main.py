import os
import pygame as pg
import sys
import time
import math
from collections import deque

from enemies import Enemy
from towers import Towers
from bullets import Bullets
from classes import UserInfo, Levels, Message, SquareGrid, Menus

# Set the window's position
os.environ['SDL_VIDEO_WINDOW_POS'] = "0, 30"

# Define global variables
# Screen specifications
SCREEN_HEIGHT = 830
SCREEN_WIDTH = 1440
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
HEADING = "Tower Defence"
FPS = 60

# Static
TILE_SIZE = int(SCREEN_WIDTH/54)
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
RED_COINS_TIME = 0
RETRY_COUNTER = 0

# User
RED_COINS = False

# Wave variables
WAVE_READY = False
START_WAVE = False
CREATE_WAVE = False
ENEMY_NUMBER = 0

# Menu
SELECTED = None
SELECTED_POS = False

# Game and pg Window status
ACTIVE = True
GG = False
CONGRATS = False

pg.init()
# Create a clock
clock = pg.time.Clock()

# Create a screen
pg.display.set_caption(HEADING)
my_screen = pg.display.set_mode(SCREEN_SIZE)

# Define groups
all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()
towers = pg.sprite.Group()
bullets = pg.sprite.Group()

# Create a UserInfo instance
user = UserInfo(5, 20, 500)

# Create an instance of a SquareGrid and set it's start, end, and walls
my_grid = SquareGrid(SCREEN_WIDTH/TILE_SIZE, SCREEN_HEIGHT/TILE_SIZE)
my_grid.start = (0, 11)
my_grid.end = (47, 24)
walls = [(5, 12), (6, 8), (6, 7), (6, 6), (6, 12), (7, 12), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (9, 6), (9, 5),
         (8, 12), (12, 1), (13, 1), (14, 1), (15, 1), (18, 1), (17, 1), (16, 1), (19, 1), (20, 1), (22, 1), (21, 1),
         (22, 4), (23, 4), (24, 4), (25, 4), (26, 5), (26, 6), (25, 7), (24, 7), (23, 7), (22, 7), (21, 7), (22, 10),
         (21, 10), (20, 10), (19, 10), (19, 21), (20, 21), (21, 21), (22, 17), (22, 16), (22, 15), (24, 13), (25, 13),
         (26, 13), (27, 13), (28, 13), (33, 2), (34, 2), (35, 2), (36, 2), (37, 2), (38, 2), (39, 2), (40, 2), (41, 2),
         (42, 2), (43, 11), (43, 12), (43, 13), (23, 21), (22, 21), (24, 21), (25, 17), (28, 16), (29, 16), (30, 16),
         (31, 16), (35, 15), (35, 14), (35, 13), (35, 12), (35, 11), (35, 10), (35, 9), (35, 8), (35, 7), (35, 6),
         (40, 6), (40, 7), (40, 8), (40, 9), (40, 11), (40, 10), (40, 17), (5, 26), (6, 26), (7, 26), (8, 26), (9, 26),
         (10, 26), (11, 26), (12, 26), (13, 26), (7, 19), (7, 20), (7, 21), (7, 22), (12, 23), (13, 23), (14, 23),
         (18, 25), (18, 24), (18, 23), (18, 22), (40, 18), (40, 19), (40, 20), (40, 21), (40, 22), (40, 23), (40, 24),
         (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (14, 14), (18, 10), (6, 10), (7, 5), (9, 3), (21, 3),
         (27, 9), (16, 12), (12, 24), (22, 19), (29, 14), (33, 8), (40, 4), (41, 12), (42, 21), (13, 15), (12, 15),
         (11, 15), (10, 15), (9, 15), (10, 18), (9, 18), (8, 18), (10, 17), (6, 5), (7, 24), (9, 4), (26, 4), (26, 7),
         (17, 10), (14, 15), (7, 23), (15, 23), (18, 21), (22, 18), (40, 5), (7, 18), (4, 12), (8, 11), (8, 10), (8, 9),
         (8, 8), (8, 7), (9, 7), (7, 4), (7, 3), (7, 2), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3), (16, 3),
         (18, 3), (17, 3), (19, 3), (20, 3), (22, 3), (23, 1), (24, 2), (24, 1), (25, 2), (26, 2), (27, 2), (28, 2),
         (28, 3), (28, 4), (28, 5), (28, 6), (28, 7), (28, 8), (28, 9), (26, 9), (25, 9), (24, 9), (23, 9), (22, 9),
         (20, 8), (19, 8), (20, 7), (18, 8), (17, 8), (16, 8), (15, 8), (16, 10), (16, 11), (16, 13), (16, 14),
         (16, 15), (16, 16), (16, 17), (15, 17), (14, 17), (13, 17), (12, 17), (11, 17), (8, 16), (7, 16), (6, 16),
         (5, 16), (8, 15), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23), (5, 24), (5, 25), (8, 24),
         (9, 24), (10, 24), (11, 24), (14, 25), (14, 26), (15, 25), (16, 25), (17, 25), (16, 23), (16, 22), (16, 21),
         (16, 20), (16, 19), (17, 19), (18, 19), (19, 19), (20, 19), (21, 19), (24, 20), (24, 19), (24, 18), (24, 17),
         (23, 15), (23, 14), (23, 13), (25, 16), (25, 15), (26, 15), (27, 15), (27, 16), (33, 13), (33, 12), (33, 11),
         (33, 10), (33, 9), (33, 7), (33, 6), (33, 5), (33, 4), (33, 3), (35, 4), (35, 5), (36, 4), (37, 4), (38, 4),
         (39, 4), (42, 3), (42, 4), (42, 5), (42, 6), (42, 7), (42, 8), (42, 9), (42, 10), (43, 10), (43, 14), (42, 18),
         (6, 9), (40, 12), (43, 15), (43, 16), (43, 17), (41, 13), (41, 14), (41, 15), (40, 16), (41, 16), (43, 18),
         (42, 19), (42, 20), (42, 22), (40, 25), (41, 25), (42, 25), (43, 25), (44, 25), (45, 25), (46, 25), (47, 25),
         (47, 23), (46, 23), (45, 23), (44, 23), (43, 23), (42, 23), (0, 10), (0, 12), (1, 10), (1, 12), (2, 10),
         (2, 12), (3, 12), (3, 10), (4, 10), (5, 10), (32, 16), (33, 16), (34, 16), (35, 16), (29, 13), (30, 14),
         (31, 14), (32, 14), (33, 14), (48, 23), (48, 24), (48, 25)]
for wall in walls:
    my_grid.walls.append(wall)

# Create a Levels instance
my_levels = Levels(my_grid)

# Create instances of inactive Towers for the menu
dart_monkey = Towers('dart', (49.25*TILE_SIZE, 4*TILE_SIZE), False)
sniper = Towers('sniper', (52.25*TILE_SIZE, 4*TILE_SIZE), False)
# Alter the Towers' rects to blow them up
dart_monkey.rect = pg.Rect(dart_monkey.pos, (2*TILE_SIZE, 2*TILE_SIZE))
sniper.rect = pg.Rect(sniper.pos, (2*TILE_SIZE, 2*TILE_SIZE))
menu_towers = [dart_monkey, sniper]
tower_menu = Menus(my_screen, pg.Rect(48*TILE_SIZE, 0, SCREEN_WIDTH - 48*TILE_SIZE, SCREEN_HEIGHT), BLUE, menu_towers)

# Create Message instances to display on the menu
t_m_title1 = Message(my_screen, (50*TILE_SIZE, TILE_SIZE/2), 'Tower', font=pg.font.SysFont('comicsansms', 28),
                     bg_color=BLUE)
t_m_title2 = Message(my_screen, (49.5*TILE_SIZE, 2*TILE_SIZE), 'Selection', font=pg.font.SysFont('comicsansms', 28),
                     bg_color=BLUE)
t_m_msgs = [t_m_title1, t_m_title2]


def reset_game_vars():
    global DT, CURSOR_TIME, TINT, TINT_TIME, WAVE_TIME, ENEMY_SPACING, RED_COINS_TIME, RETRY_COUNTER, RED_COINS,\
        WAVE_READY, START_WAVE, CREATE_WAVE, ENEMY_NUMBER, SELECTED, SELECTED_POS, GG, ACTIVE, CONGRATS, all_sprites, \
        enemies, towers, bullets
    # Timers
    DT = 0
    CURSOR_TIME = 0
    TINT = False
    TINT_TIME = 0
    WAVE_TIME = 0
    ENEMY_SPACING = 5
    RED_COINS_TIME = 0
    RETRY_COUNTER = 0

    # User
    RED_COINS = False

    # Wave variables
    WAVE_READY = False
    START_WAVE = False
    CREATE_WAVE = False
    ENEMY_NUMBER = 0

    # Menu
    SELECTED = None
    SELECTED_POS = False

    # Game and pg Window status
    ACTIVE = True
    GG = False
    CONGRATS = False

    # Define groups
    all_sprites = pg.sprite.Group()
    enemies = pg.sprite.Group()
    towers = pg.sprite.Group()
    bullets = pg.sprite.Group()


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


def cursor():
    global CURSOR_TIME
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


def show_t_m_msgs(msgs):
    for msg in msgs:
        msg.blit()


def draw_selected(surface, grid, menu):
    if SELECTED is None:
        return
    else:
        # Draw tower
        pos = pg.mouse.get_pos()
        SELECTED.pos = (pos[0] - SELECTED.rect.w/2, pos[1] - SELECTED.rect.h/2)
        SELECTED.draw(surface)
        # Draw radius, color based on if the position is accepted
        check_legal(grid, menu, SELECTED.rect)
        if SELECTED_POS:
            color = GREEN
        else:
            color = RED
        pg.draw.circle(surface, color, pos, SELECTED.range*TILE_SIZE, 5)


def draw_group(surface, group):
    for sprite in group:
        sprite.draw(surface)


def create_bullets(tower_group, enemy_group, path):
    for tower in tower_group:
        if tower.active:
            tower.counter += DT
            tower.in_range = []
            if tower.counter >= tower.wait_time:
                # Check for enemies in bounding box
                r = pg.Rect(0, 0, tower.range*TILE_SIZE*2, tower.range*TILE_SIZE*2)
                r.center = tower.rect.center
                for enemy in enemy_group:
                    if r.collidepoint(enemy.rect.centerx, enemy.rect.centery):
                        # Check if enemy is inside range
                        p1 = tower.rect.center
                        p2 = enemy.rect.center
                        if math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) <= tower.range*TILE_SIZE:
                            # If enemy is in range, add it to the tower's in_range list
                            tower.in_range.append(enemy)

                if len(tower.in_range) > 0:
                    # If there are enemies in range, create a bullet with the furthest enemy as it's target
                    b = Bullets(tower.rect.center, tower.damage)
                    bullets.add(b)
                    b.target_sprite = furthest(tower.in_range, path)
                    tower.counter = 0


def furthest(enemy_list, path):
    for tile in path:
        for enemy in enemy_list:
            if enemy.next == tile:
                return enemy


def update_bullets(bullet_group):
    for bullet in bullet_group:
        bullet.update()


def check_wave(user_info, group):
    global WAVE_READY, WAVE_TIME, CONGRATS
    if len(group) == 0:
        WAVE_TIME += DT
        if WAVE_TIME >= 5:
            if user_info.next_wave():
                WAVE_TIME = 0
                WAVE_READY = True
            else:
                CONGRATS = True
    else:
        WAVE_READY = False


def show_start_wave(user_info, surface):
    global WAVE_TIME, START_WAVE, CREATE_WAVE
    start_wave = Message(surface, (0, 10), ('Start Wave ' + str(user_info.wave + 1) + '/' + str(user_info.waves)),
                         font=pg.font.SysFont('comicsansms', 24, True), bg_color=BROWN)
    start_wave.rect.right = 48*TILE_SIZE - 10
    start_wave.blit()
    user_info.start_wave = start_wave


def create_wave(user_info, group, level_name):
    global ENEMY_SPACING, ENEMY_NUMBER, CREATE_WAVE
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


def update_enemies(enemy_group, grid):
    multiplier = DT*TILE_SIZE
    for enemy in enemy_group:
        if enemy.health <= 0:
            user.coins += enemy.coins
            enemy.kill()
        enemy.update(multiplier)
    check_enemies_path(enemy_group, grid)


def check_enemies_path(group, grid):
    for sprite in group:
        sprite.check_path(grid)


def show_user_info(surface, user_info):
    global RED_COINS, RED_COINS_TIME
    # Create Message instances to display user info
    wave = Message(surface, (5, 5), ('WAVE ' + str(user_info.wave) + '/' + str(user_info.waves)),
                   font=pg.font.SysFont('comicsansms', 24, True), bg_color=LIGHT_BLUE)
    lives = Message(surface, (5, 35), ('Lives: ' + str(user_info.lives)), bg_color=LIGHT_BLUE)
    if RED_COINS:
        RED_COINS_TIME += DT
        if RED_COINS_TIME <= 1:
            color = RED
        else:
            color = LIGHT_BLUE
            RED_COINS = False
            RED_COINS_TIME = 0
    else:
        color = LIGHT_BLUE

    coins = Message(surface, (5, 60), ('Coins: ' + str(user_info.coins)), bg_color=color)
    # Blit the info
    wave.blit()
    lives.blit()
    coins.blit()


def successful_enemies(group, grid, user_info, surface):
    global GG, TINT, TINT_TIME
    for sprite in group:
        if sprite.successful(grid.end):
            print(sprite.health)
            user_info.lives -= int(sprite.health/10)
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


def set_selected(tower_name):
    global SELECTED
    try:
        name = SELECTED.name
        SELECTED.kill()
    except AttributeError:
        name = None
    if name != tower_name or name is None:
        SELECTED = Towers(tower_name, (0, 0), False)
        all_sprites.add(SELECTED)
        towers.add(SELECTED)
    else:
        SELECTED = None


def check_legal(grid, menu, tower_rect):
    global SELECTED_POS
    illegal_rects = []
    for w in grid.walls:
        rect = pg.Rect(w[0]*TILE_SIZE, w[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        illegal_rects.append(rect)
    for p in grid.path:
        rect = pg.Rect(p[0]*TILE_SIZE, p[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        illegal_rects.append(rect)
    illegal_rects.append(menu.rect)
    if tower_rect.collidelistall(illegal_rects):
        SELECTED_POS = False
    else:
        SELECTED_POS = True


def gg(surface):
    global RETRY_COUNTER
    draw_tint(RED, surface)
    gg1 = Message(surface, (480, 223), ' You Lost All      ', font=pg.font.SysFont('comicsansms', 56, True),
                  bg_color=BROWN)
    gg2 = Message(surface, (480, 300), '      Your Lives...', font=pg.font.SysFont('comicsansms', 56, True),
                  bg_color=BROWN)
    gg1.blit()
    gg2.blit()
    RETRY_COUNTER += DT
    if RETRY_COUNTER >= 2:
        user.try_again = Message(surface, (565, 420), 'Try Again?', font=pg.font.SysFont('comicsansms', 58, True),
                                 bg_color=GREEN)
        user.try_again.blit()


def congrats(surface):
    global RETRY_COUNTER
    draw_tint(GREEN, surface)
    c1 = Message(surface, (480, 220), 'You Completed ', font=pg.font.SysFont('comicsansms', 60, True),
                 bg_color=BROWN)
    c2 = Message(surface, (480, 300), 'All the Waves! ', font=pg.font.SysFont('comicsansms', 60, True),
                 bg_color=BROWN)
    c1.blit()
    c2.blit()
    RETRY_COUNTER += DT
    if RETRY_COUNTER >= 2:
        user.try_again = Message(surface, (560, 420), 'Play Again?', font=pg.font.SysFont('comicsansms', 58, True),
                                 bg_color=GREEN)
        user.try_again.blit()


# Define functions for the main loop
def handle_input():
    """Process and appropriately react to user input"""
    # Regulate frame rate and store frame time in seconds
    global DT, SELECTED, SELECTED_POS, RED_COINS, RED_COINS_TIME
    DT = clock.tick(FPS)/1000
    # Test for a quit command
    for event in pg.event.get():
        if event.type == pg.QUIT:
            global ACTIVE
            ACTIVE = False
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = event.pos[0], event.pos[1]
                if event.button == 1 or event.button == 3:
                    global GG, CONGRATS, user
                    if GG:
                        if user.try_again.rect.collidepoint(pos):
                            user = UserInfo(5, 20, 500)
                            reset_game_vars()
                    elif CONGRATS:
                        if user.try_again.rect.collidepoint(pos):
                            CONGRATS = False
                            user = UserInfo(5, 20, 500)
                            reset_game_vars()
                    else:
                        global WAVE_READY, CREATE_WAVE
                        # Check for updates on the selected tower from the menu
                        if SELECTED is not None and SELECTED_POS:
                            # Pay coins and create tower
                            user.coins -= SELECTED.cost
                            t = Towers(SELECTED.name, SELECTED.pos, True)
                            all_sprites.add(t)
                            towers.add(t)
                            SELECTED.kill()
                            SELECTED, SELECTED_POS = None, False
                        for tower in menu_towers:
                            if tower.rect.collidepoint(pos):
                                if user.coins >= tower.cost:
                                    set_selected(tower.name)
                                else:
                                    RED_COINS = True
                                    RED_COINS_TIME = 0
                        # Check for the start_wave button
                        if WAVE_READY and user.start_wave is not None:
                            if user.start_wave.rect.collidepoint(pos):
                                user.start_wave = None
                                user.wave += 1
                                WAVE_READY = False
                                CREATE_WAVE = True

    pg.event.clear()


def update_screen():
    global START_WAVE
    """Draw an updated version of the screen"""
    # Draw bg
    my_screen.fill(LIGHT_BLUE)
    # draw_grid()
    draw_walls(my_grid, my_screen, BROWN)
    draw_path(my_grid, my_screen, LIGHT_BROWN)
    # Draw towers
    draw_selected(my_screen, my_grid, tower_menu)
    draw_group(my_screen, towers)
    # Draw the tower menu
    tower_menu.draw()
    show_t_m_msgs(t_m_msgs)
    # Create bullets
    create_bullets(towers, enemies, my_grid.path)
    # Update bullets
    update_bullets(bullets)
    # Draw bullets
    draw_group(my_screen, bullets)
    # Handle waves
    check_wave(user, enemies)
    if WAVE_READY:
        show_start_wave(user, my_screen)
    if CREATE_WAVE:
        create_wave(user, enemies, 'my_levels.wave')
    # Update enemies
    update_enemies(enemies, my_grid)
    # Draw enemies
    draw_group(my_screen, enemies)
    # Draw User Info
    show_user_info(my_screen, user)
    successful_enemies(enemies, my_grid, user, my_screen)
    # Draw the end screen if the player lost
    if GG:
        gg(my_screen)
    # Draw the congrats screen if the player won
    elif CONGRATS:
        congrats(my_screen)

    pg.display.flip()


def run_game():
    """Main game loop"""
    global ACTIVE
    my_grid.path = simple_pathfinder(my_grid)
    while ACTIVE:
        handle_input()
        update_screen()
    pg.quit()
    sys.exit()


run_game()
