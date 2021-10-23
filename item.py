from constants import *
import json


class Item:
    def __init__(self, name, tile, color=COLOR_WHITE, pos=None):
        self.name = name
        self.tile = tile
        self.pos = pos
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
                self.items.append(Item(piece['name'], piece['symbol'], piece['color']))

    def create_instance_of(self, item_index):
        return self.items[item_index].copy()
