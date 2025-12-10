import numpy as np
from noise import pnoise2

# =========================
# CONFIGURACIÓN DE COLORES
# =========================
colors = [
    "#000000",
    "#2D5C88",
    "#858044",
    "#457422",
    "#434D4B",
    "#D8D8D8"]

class MapGenerator:
    def __init__(self, size=512, seed=0):
        """
        size: resolución (square). Ej: 256, 512, 1024
        seed: semilla entera reproducible
        """
        self.size = size
        self.seed = int(seed)
        self.rng = np.random.RandomState(self.seed)
        self.height = np.zeros((size, size), dtype=float)
        self.temperature = np.zeros_like(self.height)
        self.humidity = np.zeros_like(self.height)
        self.biome = np.zeros_like(self.height, dtype=np.int32)
        self.world = np.zeros((size, size), dtype=float)

    def _perlin_noise(self, scale=100.0, octaves=4, persistence=0.5, lacunarity=2.0):
        # Genera ruido Perlin usando noise
        S = self.size
        for i in range(S):
            for j in range(S):
                self.world[i][j] = pnoise2(i/scale,
                                           j/scale,
                                           octaves=octaves,
                                           persistence=persistence,
                                           lacunarity=lacunarity,
                                           repeatx=S,
                                           repeaty=S,
                                           base=self.seed)
        self.world = self.world / self.world.max()

    def _color_world(self):
        color_world = np.zeros_like(self.world, dtype=np.int32)
        S = self.size
        for i in range(S):
            for j in range(S):
                a = self.world[i][j]
                if  a < 0.25:
                    color_world[i][j] = 1
                elif  a < 0.35:
                    color_world[i][j] = 2
                elif  a < 0.65:
                    color_world[i][j] = 3
                elif  a < 0.85:
                    color_world[i][j] = 4
                else: 
                    color_world[i][j] = 5

        self.world = color_world
