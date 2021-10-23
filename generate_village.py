from level import Level
from constants import *
from zone import Zone
import random

village = Level(100, 100)
village.fill()
village.make_grass()

public_zone = Zone((45, 55, 45, 55))
for i in range(10):
    for j in range(10):
        if random.randint(0, 10) < (5 - abs(5 - i)) + (5 - abs(5 - j)) + 1:
            village.tilemap[45 + i][45 + j] = ord('.')

houses = 15

for i in range(houses):
    while True:
        x, y = random.randint(20, 70), random.randint(20, 70)
        w, h = random.randint(1,2) * 5, random.randint(2, 4) * 2
        house_zone = Zone((x, y, x + w - 1, y + h - 1))

        ok = True
        for zone in village.zones + [public_zone]:
            if zone.collide(house_zone):
                ok = False
                break
        if ok:
            break
    
    village.zones.append(house_zone)
    for j in range(w):
        village.tilemap[y][x + j] = 205
        village.tilemap[y + h - 1][x + j] = 205
        village.colormap[y][x + j] = COLOR_GRAY
        village.colormap[y + h - 1][x + j] = COLOR_GRAY
    for j in range(h):
        village.tilemap[y + j][x] = 186
        village.tilemap[y + j][x + w - 1] = 186
        village.colormap[y + j][x] = COLOR_GRAY
        village.colormap[y + j][x + w - 1] = COLOR_GRAY
    
    village.tilemap[y][x] = 201
    village.tilemap[y][x + w - 1] = 187
    village.tilemap[y + h - 1][x] = 200
    village.tilemap[y + h - 1][x + w - 1] = 188


village.zones.append(public_zone)

work_zones_count = 4

for i in range(work_zones_count):
    while True:
        x, y = random.randint(1, 90), random.randint(1, 90)
                
        w, h = random.randint(1, 5) * 2, random.randint(1, 5) * 2
        work_zone = Zone((x, y, x + w - 1, y + h - 1))

        if x + w - 1 >= 100 or y + h - 1 >= 100:
            continue

        ok = True
        for zone in village.zones:
            if zone.collide(work_zone):
                ok = False
                break
        if ok:
            break
    
    village.zones.append(work_zone)
    for j in range(w):
        for k in range(h):
            village.tilemap[y + k][x + j] = ord('~')
            village.colormap[y + k][x + j] = COLOR_YELLOW



village.save("levels/village")
