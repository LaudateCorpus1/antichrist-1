from constants import *
import json


class Item:
    def __init__(self, name, tile, color, item_type, pos=None, level=None):
        self.name = name
        self.tile = tile
        self.pos = pos
        self.level = level
        self.color = color
        self.item_type = item_type
        self.equipped = False

    def copy(self):
        return Item(self.name, self.tile, self.color, self.item_type)


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
                self.items.append(Item(piece['name'], ord(piece['symbol']), color, piece['type']))

    def create_instance_of(self, item_index):
        return self.items[item_index].copy()
