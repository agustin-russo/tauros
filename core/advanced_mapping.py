import numpy as np
from core.perlin_noise import perlin_noise, make_perm
from scipy.ndimage import gaussian_filter
from numba import njit


@njit
def temperature_map(random, height, width, height_map, sea_level, sand_level):
    base_temp = 25 # Temperatura "promedio" en el ecuador
    variacion_termica = 5 # Cuanto varía del promedio
    temp_map = np.zeros_like(height_map, dtype=np.float32)
    height_punishment = 1.5 # Lapse Rate, perdida cada mil metros
    max_world_height = 8000 # Ocho mil metros
    #random = perlin_noise(make_perm(seed), height=height, width=width)

    for y in range(height):
        for x in range(width):
            # Formula piola para normalizar la distancia al ecuador
            latitude = (abs(y - height / 2) / height) * 0.9
            initial_temp = base_temp - latitude * 35.0 # Minima temperatura, -10 grados
            
            if height_map[y][x] > sea_level:
                initial_temp = initial_temp + (variacion_termica * 0.5)
            else:
                initial_temp = initial_temp - (variacion_termica * 0.5)
            
            if height_map[y][x] > sea_level and height_map[y][x] < sand_level:
                perdida_altura = variacion_termica * 0.5

            else:
                elevation = max(height_map[y][x], sea_level) - sea_level
                perdida_potencial = max_world_height * height_punishment / 1000.0
                perdida_altura = (elevation / (1 - sea_level)) * perdida_potencial
            temp_map[y][x] = initial_temp - perdida_altura + (random[y][x] * 2.0)

    return temp_map


def humidity_map(seed, height, width, heightmap, sea_level, blur=2):
    n = perlin_noise(make_perm(seed+2), height, width)
    humidity = (n - n.min()) / (n.max() - n.min())
    
    gx, gy = np.gradient(heightmap)
    slope = np.sqrt(gx**2 + gy**2)
    slope = (slope - slope.min()) / (slope.max() - slope.min() + 1e-8)
    humidity *= (1.0 - slope)
    
    humidity[heightmap <= sea_level] = 1.0
    humidity = gaussian_filter(humidity, sigma=blur)

    return humidity

@njit
def biomes_map(height, width, heightmap, temperature, humidity, water, coast, land, mountains):
    colors = [
        0xFF637796, # Tundra
        0xFF8F793F, # Pastizales templados
        0xFF367032, # Taiga
        0xFF3D4A1B, # Matorral
        0xFFB5A75E, # Desierto
        0xFF1D5217, # Bosque
        0xFFBA7907, # Sabana
        0xFF234A36, # Bosque humedo
        0xFF07451B, # Selva
        0xFF2D5C88, # Mar
        0xFF858044, # Costa
        0xFF434D4B, # Montañas
        0xFFD8D8D8  # Nieve
    ]

    biomes = np.zeros_like(heightmap, dtype=np.uint32)
    for i in range(height):
        for j in range(width):
            a = heightmap[i][j]
            if a < coast:
                if a < water:
                    biomes[i][j] = colors[9]
                else:
                    biomes[i][j] = colors[10]
            
            elif a > land:
                if a < mountains:
                    biomes[i][j] = colors[11]
                else:
                    biomes[i][j] = colors[12]

            else:
                t = temperature[i][j]
                h = humidity[i][j]
                if t < 0.20: # Frío
                    biomes[i][j] = colors[0] 

                elif t < 0.70: # Templado
                    if h < 0.30: # Seco
                        if h < 0.15:
                            biomes[i][j] = colors[1]
                        else:
                            biomes[i][j] = colors[3]

                    elif h < 0.70: # Templado
                        if t < 0.35:
                            biomes[i][j] = colors[2]
                        else:
                            biomes[i][j] = colors[5]

                    else: # Húmedo
                        biomes[i][j] = colors[7]

                else: # Cálido
                    if h < 0.25: # Seco
                        biomes[i][j] = colors[4]

                    elif h < 0.70: # Templado
                        biomes[i][j] = colors[6]

                    else: # Húmedo
                        biomes[i][j] = colors[8]


    return biomes
