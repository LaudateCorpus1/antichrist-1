from PIL import Image
import numpy as np
from constants import COLORS


for color in COLORS:
    texture = Image.open('res/Talryth_square_15x15.png')
    px = texture.load()
    x, y = texture.size
    for i in range(x):
        for j in range(y):
            cc = px[i, j]
            nc = []
            for k in range(3):
                nc.append(int((cc[k] / 255) * color[2][k]))
            nc.append(cc[3])
            px[i, j] = tuple(nc)
    texture.save('res/texture_' + color[1] + '.png')
    print(color[1], 'texture generated')

