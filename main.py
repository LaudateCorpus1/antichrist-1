import pygame
import sys
import random


from constants import *
from tileset import Tileset
from level import Level
from menu import Text, ConfirmationBox, TextBox
from actor import Player, Point, NPC


## Helpers

def load_levels():
    levels = dict()
    for level_name in LEVEL_NAMES:
        levels[level_name] = Level.load("levels/" + level_name)
    return levels

def initialize_player():
    return Player("Sahe", Point(51, 51), levels, START_LEVEL, 224, 10)

def generate_npc(n):
    npc = []
    random.shuffle(names)
    for i in range(n):
        npc.append(NPC(names[i], Point(random.randint(1, 99), random.randint(1, 99)), levels, 'village', ord(names[i][0]), 20 + random.randint(2, 15), 'farmer'))
        npc[-1].house = levels['village'].zones[i]
        npc[-1].work_zone = random.choice(levels['village'].zones[-4:])
        for j in range(n):
            npc[-1].relations[names[j]] = 10
        npc[-1].relations[names[i]] = 100

    for i in range(random.randint(2, 4)):
        guardian_id = random.randint(0, len(npc) - 1)
        npc[guardian_id].profession = 'guardian'
        npc[guardian_id].work_zone = levels['village'].zones[-4:]

    return npc

def generate_items(n):
    items = []
    return items

def load_names():
    with open("res/names.txt") as f:
        names = [i.strip() for i in f.readlines()]
    return names
    
## Initialize

pygame.init()
display_info = pygame.display.Info()
display_size = display_info.current_w, display_info.current_h
screen = pygame.display.set_mode(display_size)
pygame.display.set_caption('Antichrist')

surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

levels = load_levels()
player = initialize_player()
tileset = Tileset("res/Talryth_square_15x15.png", (TILE_SIZE, TILE_SIZE), 0, 0)
names = load_names()
ticks = 0
status_text = Text((0, MAP_HEIGHT), f"{player.level} - {ticks} ({['night','morning','day','day','evening','night'][ticks//1000]})")
game_state = GAME_RUNNING
clock = pygame.time.Clock()

npc = generate_npc(15)
items = generate_items(32)

menus = [TextBox("Antichrist", timer=13)]

## Main loop

vel_x = 0
vel_x_m = 0
vel_y = 0
vel_y_m = 0

is_dead_message_created = False

while game_state != GAME_FINISHED:
    # Fetch events
    for event in pygame.event.get():
        used = False
        for menu in menus:
            if menu.handle_event(event):
                used = True
                break
        if used: continue
        
        if event.type == pygame.QUIT:
            game_state = GAME_FINISHED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                vel_x_m = -1
            if event.key == pygame.K_RIGHT:
                vel_x = 1
            if event.key == pygame.K_UP:
                vel_y_m = -1
            if event.key == pygame.K_DOWN:
                vel_y = 1
                
            if event.key == pygame.K_q:
                game_state = GAME_FINISHED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and vel_x_m == -1:
                vel_x_m = 0
            if event.key == pygame.K_RIGHT and vel_x == 1:
                vel_x = 0
            if event.key == pygame.K_UP and vel_y_m == -1:
                vel_y_m = 0
            if event.key == pygame.K_DOWN and vel_y == 1:
                vel_y = 0
                    
    # Update game state
    if player.is_alive:
        player.pos.x += vel_x + vel_x_m
        player.pos.y += vel_y + vel_y_m
    if player.pos.x <= 0 or player.pos.y <= 0 or \
       player.pos.x >= levels[player.level].width - 1 or player.pos.y >= levels[player.level].height - 1:
        if player.level == 'village':
            next_level = 'forest'
        else:
            next_level = 'village'
        
        if player.pos.x <= 0:
            player.pos.x = levels[next_level].width - 2
        elif player.pos.x >= levels[player.level].width - 1:
            player.pos.x = 1
            
        if player.pos.y <= 0:
            player.pos.y = levels[next_level].height - 2
        elif player.pos.y >= levels[player.level].height - 1:
            player.pos.y = 1

        levels[player.level].actors.remove(player)
        levels[next_level].actors.append(player)
        player.level = next_level
    for actor in npc:
        actor.define_current_action(ticks)
    for actor in npc:
        actor.act()
    
    for menu in menus:
        menu.update(ticks)
    
    if not player.is_alive and not is_dead_message_created:
        def stop_game():
            global game_state
            game_state = GAME_FINISHED
        is_dead_message_created = True
        menus.append(ConfirmationBox("YOU ARE DEAD", stop_game))
    
    # Render
    surface.fill((0, 0, 0))
    position = (player.pos.x - MAP_WIDTH // 2,
                player.pos.y - MAP_HEIGHT // 2)
    
    levels[player.level].render(surface, tileset, position)
    for actor in levels[player.level].actors:
        levels[player.level].render_actor(surface, tileset, position, actor)
    levels[player.level].render_actor(surface, tileset, position, player)
    status_text.text = f"{player.level} - {ticks} ({['night','morning','day','day','evening','night'][ticks//1000]})"
    status_text.render(surface, tileset)

    for menu in menus:
        if menu.is_need_to_be_removed():
            menus.remove(menu)
            continue
        menu.render(surface, tileset)
    pygame.display.update()

    screen.blit(surface, (display_size[0] // 2 - SCREEN_WIDTH // 2, display_size[1] // 2 - SCREEN_HEIGHT // 2))

    clock.tick(FRAMERATE)
    ticks = (ticks + 1) % 6000

## Deinit

pygame.quit()
sys.exit()
