from constants import *


class Menu:
    pass


class Text (Menu):
    def __init__(self, position, text):
        self.position = position
        self.text = text

    def render(self, surface, tileset):
        x = self.position[0]
        y = self.position[1]
        for letter in self.text:
            surface.blit(tileset.tiles[ord(letter)], (x * TILE_SIZE, y * TILE_SIZE))
            x += 1


class TextBox(Menu):
    def __init__(self, position, size, text):
        self.position = position
        self.size = size
        self.text = text

    def render(self, surface, tileset):
        pass
