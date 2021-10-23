import pygame


from constants import *


class Tileset:
    def __init__(self, file, size=(32, 32), margin=1, spacing=1):
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect()
        self.tiles = []
        self.load()


    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for y in range(y0, h, dy):
            for x in range(x0, w, dx):
                tile = pygame.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def get_tile(self, value):
        return self.tiles[value]


class ColoredTileset:
    def __init__(self, prefix, size=(32, 32), margin=1, spacing=1):
        self.prefix = prefix
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.tilesets = dict()
        self.load()

    def load(self):
        for color in COLORS:
            self.tilesets[color[0]] = Tileset(self.prefix + color[1] + '.png', self.size, self.margin, self.spacing)

    def get_tile(self, value, color=COLOR_WHITE):
        return self.tilesets[color].tiles[value]
