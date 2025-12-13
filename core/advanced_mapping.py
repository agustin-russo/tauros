import numpy as np


def temperature_map(height, width, height_map, sea_level, type="global"):
    base_temp = 35
    temp_map = np.zeros_like(height_map, dtype=np.float32)
    height_punishment = 6.5 # Lapse Rate, perdida cada mil metros
    max_world_height = 8000 # Ocho mil metros


    for y in range(height):
        if type == "global":
            # Formula piola para normalizar la distancia al ecuador
            latitude = (abs(y - height / 2) / height) * 0.9
        elif type == "map":
            latitude = (abs(y - height) / height) * 0.9
            
        initial_temp = base_temp - latitude * 60.0

        for x in range(width):
            elevation = max(height_map[y][x], sea_level) - sea_level
            perdida_potencial = max_world_height * height_punishment / 1000.0
            perdida_altura = (elevation / (1 - sea_level)) * perdida_potencial
            temp_map[y][x] = initial_temp - perdida_altura

    return temp_map

def humidity_map():
    pass

