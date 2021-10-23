from constants import *
from zone import Zone
import struct
import random


class Level:
    def __init__(self, width, height):
        self.tilemap = []
        self.colormap = []
        self.zones = []
        self.width = width
        self.height = height
        self.actors = []

    def fill(self):
        self.tilemap = []
        self.colormap = []
        for i in range(self.height):
            self.tilemap.append([])
            self.colormap.append([])
            for j in range(self.width):
                if i == 0:
                    self.tilemap[-1].append(30)
                elif i == self.height - 1:
                    self.tilemap[-1].append(31)
                elif j == 0:
                    self.tilemap[-1].append(17)
                elif j == self.width - 1:
                    self.tilemap[-1].append(16)
                else:
                    self.tilemap[-1].append(0)
                self.colormap[-1].append(COLOR_WHITE)

    def make_grass(self):
        for i in range(1, self.height - 1):
            for j in range(1, self.width - 1):
                self.tilemap[i][j] = random.choice([ord(','), ord('.'), ord('`')])
                self.colormap[i][j] = COLOR_BROWN

    @staticmethod
    def load(name):
        with open(name, "rb") as f:
            width, height = struct.unpack('<ii', f.read(8))
            level = Level(width, height)
            for i in range(height):
                level.tilemap.append([])
                for j in range(width):
                    level.tilemap[-1].append(struct.unpack('<B', f.read(1))[0])
                    
            for i in range(height):
                level.colormap.append([])
                for j in range(width):
                    level.colormap[-1].append(struct.unpack('<B', f.read(1))[0])
            
            zones = struct.unpack('<i', f.read(4))[0]
            for i in range(zones):
                level.zones.append(Zone.load(f.read(16)))
        return level

    def save(self, name):
        with open(name, "wb") as f:
            f.write(struct.pack("<ii", self.width, self.height))
            for i in range(self.height):
                for j in range(self.width):
                    f.write(struct.pack("<B", self.tilemap[i][j]))
            for i in range(self.height):
                for j in range(self.width):
                    f.write(struct.pack("<B", self.colormap[i][j]))
            f.write(struct.pack('<i', len(self.zones)))
            for zone in self.zones:
                f.write(zone.save())

    def render(self, surface, tileset, position, size=(33, 33)):
        for y in range(size[1]):
            for x in range(size[0]):
                nx = x + position[0]
                ny = y + position[1]
                if nx < 0 or ny < 0 or nx >= self.width or ny >= self.height: continue
                surface.blit(tileset.get_tile(self.tilemap[ny][nx], self.colormap[ny][nx]), ((x + INVENTORY_WIDTH) * TILE_SIZE, y * TILE_SIZE))
                
    def render_actor(self, surface, tileset, position, actor, size=(33, 33)):
        nx = actor.pos.x - position[0]
        ny = actor.pos.y - position[1]
        if nx < 0 or ny < 0 or nx >= size[0] or ny >= size[1]: return
        surface.blit(tileset.get_tile(actor.tile, actor.color), ((nx + INVENTORY_WIDTH) * TILE_SIZE, ny * TILE_SIZE))

    def render_item(self, surface, tileset, position, item, size=(33, 33)):
        nx = item.pos.x - position[0]
        ny = item.pos.y - position[1]
        if nx < 0 or ny < 0 or nx >= size[0] or ny >= size[1]: return
        surface.blit(tileset.get_tile(item.tile, item.color), ((nx + INVENTORY_WIDTH) * TILE_SIZE, ny * TILE_SIZE))

