import numpy as np
from numba import njit
import math

"""
Implementación de Perlin Noise basada en el artículo de Adrian Biagioli (2021):
"Understanding Perlin Noise" https://adrianb.io/2014/08/09/perlinnoise.html

Adaptada, optimizada con Numba y extendida para Tauros World Engine.
"""

def make_perm(seed):
    rng = np.random.RandomState(seed)
    p = np.arange(256, dtype=np.int32)
    rng.shuffle(p)
    return np.concatenate([p, p])

@njit
def gradient(hash, dx, dy):
    h = hash & 7
    if h == 0:  return  dx
    if h == 1:  return -dx
    if h == 2:  return  dy
    if h == 3:  return -dy
    if h == 4:  return  dx + dy
    if h == 5:  return -dx + dy
    if h == 6:  return  dx - dy
    if h == 7:  return -dx - dy

@njit
def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

@njit
def lerp(a, b, t):
    return a + t * (b - a)

@njit
def perlin(perm, x, y):
    X = math.floor(x) & 255
    Y = math.floor(y) & 255

    xf = x - math.floor(x)
    yf = y - math.floor(y)

    h00 = perm[perm[X] + Y]
    h10 = perm[perm[X+1] + Y]
    h01 = perm[perm[X] + Y+1]
    h11 = perm[perm[X+1] + Y+1]

    d00 = gradient(h00, xf,     yf)
    d10 = gradient(h10, xf-1.0, yf)
    d01 = gradient(h01, xf,     yf-1.0)
    d11 = gradient(h11, xf-1.0, yf-1.0)

    u = fade(xf)
    v = fade(yf)

    return lerp(
        lerp(d00, d10, u),
        lerp(d01, d11, u),
        v
    )

@njit
def perlin_octaves(perm, x, y, octaves=1, persistence=0.5, lacunarity=2.0):
    total = 0.0
    amplitude = 1.0
    frequency = 1.0
    max_value = 0.0

    for _ in range(octaves):
        total += perlin(perm, x * frequency, y * frequency) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= lacunarity
    
    return total / max_value


@njit
def perlin_noise(perm, height=512, width=512,scale=100.0, octaves=4, persistence=0.5, lacunarity=2.0):
    output = np.zeros((height, width), dtype=float)

    for i in range(height):
        for j in range(width):
            x = i / scale
            y = j / scale
            output[i][j] = perlin_octaves(
                perm, x, y, 
                octaves=octaves, 
                persistence=persistence, 
                lacunarity=lacunarity
            )
    
    return output
