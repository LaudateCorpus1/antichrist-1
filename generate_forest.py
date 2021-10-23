from level import Level
from constants import *
import random

forest = Level(100, 100)
forest.fill()
forest.make_grass()

for i in range(300):
    x, y = random.randint(1, 98), random.randint(1, 98)
    forest.tilemap[x][y] = 24
    forest.colormap[x][y] = COLOR_GREEN

forest.save("levels/forest")
