from level import Level
import random

forest = Level(100, 100)
forest.fill()
forest.make_grass()

for i in range(300):
    forest.tilemap[random.randint(1, 98)][random.randint(1, 98)] = 24

forest.save("levels/forest")
