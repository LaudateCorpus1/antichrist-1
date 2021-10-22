import pygame
import sys


from constants import *
from tileset import Tileset


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Actor:
    def __init__(self, name, pos, level, tile):
        self.name = name
        self.pos = pos
        self.level = level
        self.tile = tile

    def move(dx, dy):
        self.pos.x += dx
        self.pos.y += dy


class Player(Actor):
    pass


class Level:
    def __init__(self, width, height):
        self.tilemap = []
        self.width = width
        self.height = height

    def fill(self):
        self.tilemap = []
        for i in range(self.height):
            self.tilemap.append([])
            for j in range(self.width):
                self.tilemap[-1].append((43 if (j in (0, self.width-1) or i in (0, self.height-1)) else 0))

    @staticmethod
    def load(name):
        pass

    def render(self, surface, tileset, position, size=(32, 32)):
        for y in range(size[1]):
            for x in range(size[0]):
                nx = x + position[0]
                ny = y + position[1]
                if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height: continue
                surface.blit(tileset.tiles[self.tilemap[ny][nx]], (x * TILE_SIZE, y * TILE_SIZE))
                
    def render_actor(self, surface, tileset, position, actor, size=(32, 32)):
        nx = actor.pos.x - position[0]
        ny = actor.pos.y - position[1]
        if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height: return
        surface.blit(tileset.tiles[actor.tile], (nx * TILE_SIZE, ny * TILE_SIZE))


## Helpers

def load_levels():
    levels = dict()
    for level_name in LEVEL_NAMES:
        levels[level_name] = Level(50, 50) #Level.load(level_name)
        levels[level_name].fill()
    return levels

def initialize_player():
    return Player("Luka", Point(1, 1), START_LEVEL, 14)

## Initialize

levels = load_levels()
player = initialize_player()
tileset = Tileset("res/Talryth_square_15x15.png", (TILE_SIZE, TILE_SIZE), 0, 0)
game_state = GAME_RUNNING

pygame.init()
surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Antichrist')

## Main loop

while game_state != GAME_FINISHED:
    # Fetch events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GAME_FINISHED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.pos.x -= 1
            elif event.key == pygame.K_RIGHT:
                player.pos.x += 1
            if event.key == pygame.K_UP:
                player.pos.y -= 1
            elif event.key == pygame.K_DOWN:
                player.pos.y += 1

    # Render
    surface.fill((0, 0, 0))
    position = (player.pos.x - SCREEN_WIDTH_TILES // 2,
                player.pos.y - SCREEN_HEIGHT_TILES // 2)
    
    levels[player.level].render(surface, tileset, position)
    levels[player.level].render_actor(surface, tileset, position, player)
    pygame.display.update()

## Deinit

pygame.quit()
sys.exit()
