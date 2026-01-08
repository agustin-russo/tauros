import numpy as np
import core.perlin_noise as pn
from core.advanced_mapping import temperature_map, humidity_map, biomes_map


colors = [
    0xFF000000,
    0xFF2D5C88,
    0xFF858044,
    0xFF457422,
    0xFF434D4B,
    0xFFD8D8D8
]

HCOLORS = np.array([
    (255, 125, 107, 67),
    (255, 224, 183, 90),
    (255, 93, 176, 88),
    (255, 59, 112, 56),
    (255, 86, 156, 179),
], dtype=np.float32)

COLORS = np.array([
    (255,   0,   0, 255),  
    (255,   0, 255,   0),  
    (255, 255, 255,   0),  
    (255, 255,   0,   0), 
], dtype=np.float32)


class MapGenerator:
    def __init__(self, width=512, height=512, seed=0):

        self.width = width
        self.height = height
        self.seed = int(seed)
        self.perm = pn.make_perm(seed)
        self.temperature = np.zeros((self.height, self.width), dtype=float)
        self.humidity = np.zeros_like(self.temperature)
        self.biome = np.zeros_like(self.temperature, dtype=np.int32)

    def _make_world(self, scale=100.0, octaves=4, persistence=0.5, lacunarity=2.0, sea_level=0.55, sand_level=0.60):
        w = pn.perlin_noise(self.perm, self.height, self.width, scale, octaves, persistence, lacunarity)
        self.world = (w - w.min()) / (w.max() - w.min())

        # Temperature and humidity
        t = temperature_map(pn.perlin_noise(pn.make_perm(self.seed+1), self.height, self.width), self.height, self.width, self.world, sea_level, sand_level)
        low, high = np.percentile(t, [5, 95])
        self.temperature = np.clip((t - low) / (high - low), 0, 1)

        h = humidity_map(self.seed+2, self.height, self.width, self.world, sea_level)
        low, high = np.percentile(h, [5, 95])
        self.humidity = np.clip((h - low) / (high - low), 0, 1)


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

        return color_world

    def _color_temperature(self):
        def heatmap_argb(t):
            t = np.clip(t, 0.0, 1.0)

            p = t * 3.0
            i = np.minimum(p.astype(np.int32), 2)
            f = p - i

            c1 = COLORS[i]
            c2 = COLORS[i + 1]

            rgba = (c1 + (c2 - c1) * f[..., None]).astype(np.uint32)

            return (
                (rgba[..., 0] << 24) |
                (rgba[..., 1] << 16) |
                (rgba[..., 2] << 8)  |
                rgba[..., 3]
            ).astype(np.uint32)
        
        return heatmap_argb(self.temperature)
    
    def _color_humidity(self):
        def heatmap_argb(t):
            t = np.clip(t, 0.0, 1.0)

            p = t * 4.0
            i = np.minimum(p.astype(np.int32), 3)
            f = p - i

            c1 = HCOLORS[i]
            c2 = HCOLORS[i + 1]

            rgba = (c1 + (c2 - c1) * f[..., None]).astype(np.uint32)

            return (
                (rgba[..., 0] << 24) |
                (rgba[..., 1] << 16) |
                (rgba[..., 2] << 8)  |
                rgba[..., 3]
            ).astype(np.uint32)
        
        return heatmap_argb(self.humidity)
    

    def _color_biomes(self, sea_level, coast_level, land_level, mountain_level):
        biome = biomes_map(self.height, self.width, self.world, self.temperature, self.humidity, sea_level, coast_level, land_level, mountain_level)

        self.biome = biome

        return biome

