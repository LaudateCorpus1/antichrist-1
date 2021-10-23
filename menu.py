import pygame


from constants import *


class Menu:
    def render(self, surface, tileset):
        pass

    def update(self, ticks):
        pass

    def handle_event(self, event):
        return False


class Text (Menu):
    def __init__(self, position, text):
        self.position = position
        self.text = text

    def render(self, surface, tileset):
        x = self.position[0]
        y = self.position[1]
        for letter in self.text:
            surface.blit(tileset.get_tile(ord(letter)), (x * TILE_SIZE, y * TILE_SIZE))
            x += 1


class TextBox(Menu):
    def __init__(self, text, timer=None):
        self.text = text
        self.size = (len(text) + 4, 3)
        self.timer = timer

    def is_need_to_be_removed(self):
        if self.timer is not None:
            return self.timer <= 0
        return False

    def update(self, ticks):
        self.timer -= 1

    def render(self, surface, tileset):
        message = pygame.Surface((self.size[0] * TILE_SIZE, self.size[1] * TILE_SIZE))
        pygame.draw.rect(message, (255, 255, 255), (0, 0, self.size[0] * TILE_SIZE, self.size[1] * TILE_SIZE))
        pygame.draw.rect(message, (0, 0, 0), (BORDER_WIDTH, BORDER_WIDTH, self.size[0] * TILE_SIZE - BORDER_WIDTH * 2, self.size[1] * TILE_SIZE - BORDER_WIDTH * 2))
        for ind, letter in enumerate(self.text):
            message.blit(tileset.get_tile(ord(letter)), ((2 + ind) * TILE_SIZE, 1 * TILE_SIZE))
        surface.blit(message, (SCREEN_WIDTH // 2 - self.size[0] * TILE_SIZE // 2 ,
                               SCREEN_HEIGHT // 2 - self.size[1] * TILE_SIZE // 2))

class ConfirmationBox(TextBox):
    def __init__(self, text, callback):
        self.text = text
        self.size = (len(text) + 4, 5)
        self.callback = callback
        self.clicked = False

    def is_need_to_be_removed(self):
        return self.clicked

    def update(self, ticks):
        pass

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.callback()
                self.clicked = True
                return True
        return False

    def render(self, surface, tileset):
        message = pygame.Surface((self.size[0] * TILE_SIZE, self.size[1] * TILE_SIZE))
        pygame.draw.rect(message, (255, 255, 255), (0, 0, self.size[0] * TILE_SIZE, self.size[1] * TILE_SIZE))
        pygame.draw.rect(message, (0, 0, 0), (BORDER_WIDTH, BORDER_WIDTH, self.size[0] * TILE_SIZE - BORDER_WIDTH * 2, self.size[1] * TILE_SIZE - BORDER_WIDTH * 2))
        for ind, letter in enumerate(self.text):
            message.blit(tileset.get_tile(ord(letter)), ((2 + ind) * TILE_SIZE, 1 * TILE_SIZE))
            
        for ind, letter in enumerate("[ok]"):
            message.blit(tileset.get_tile(ord(letter)), ((2 + len(self.text) // 2 - 2 + ind) * TILE_SIZE, 3 * TILE_SIZE))
        surface.blit(message, (SCREEN_WIDTH // 2 - self.size[0] * TILE_SIZE // 2 ,
                               SCREEN_HEIGHT // 2 - self.size[1] * TILE_SIZE // 2))

