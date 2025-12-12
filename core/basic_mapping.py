import numpy as np
import core.perlin_noise as pn


colors = [
    0xFF000000,
    0xFF2D5C88,
    0xFF858044,
    0xFF457422,
    0xFF434D4B,
    0xFFD8D8D8
]

class MapGenerator:
    def __init__(self, width=512, height=512, seed=0):

        self.width = width
        self.height = height
        self.seed = int(seed)
        self.perm = pn.make_perm(seed)
        self.temperature = np.zeros((self.height, self.width), dtype=float)
        self.humidity = np.zeros_like(self.temperature)
        self.biome = np.zeros_like(self.temperature, dtype=np.int32)

    def _make_world(self, scale=100.0, octaves=4, persistence=0.5, lacunarity=2.0):
        w = pn.perlin_noise(self.perm, self.height, self.width, scale, octaves, persistence, lacunarity)
        self.world = (w - w.min()) / (w.max() - w.min())

        # Temperature and humidity


    def _color_world(self, levels=[0.55, 0.60, 0.80, 0.90]):
        color_world = np.zeros_like(self.world, dtype=np.uint32)
        for i in range(self.height):
            for j in range(self.width):
                a = self.world[i][j]
                if  a < levels[0]:
                    color_world[i][j] = colors[1]
                elif  a < levels[1]:
                    color_world[i][j] = colors[2]
                elif  a < levels[2]:
                    color_world[i][j] = colors[3]
                elif  a < levels[3]:
                    color_world[i][j] = colors[4]
                else: 
                    color_world[i][j] = colors[5]

        self.world = color_world
