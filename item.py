from constants import *
import json


class Item:
    def __init__(self, name, tile, color=COLOR_WHITE, pos=None, level=None):
        self.name = name
        self.tile = tile
        self.pos = pos
        self.level = level
        self.color = color

    def copy(self):
        return Item(self.name, self.tile, self.color)


class ItemDB:
    def __init__(self, filename):
        self.filename = filename
        self.items = []

    def load(self):
        with open(self.filename) as f:
            data = json.load(f)
            for piece in data:
                for color in COLORS:
                    if color[1] == piece['color']:
                        color = color[0]
                        break
                self.items.append(Item(piece['name'], ord(piece['symbol']), color))

    def create_instance_of(self, item_index):
        return self.items[item_index].copy()
