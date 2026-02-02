from core import basic_mapping as bm
from ui import view


window = view.MainWindow()
window.show()

def generate_map():

    valores = window.get_values()

    mapa = bm.MapGenerator(int(valores["size"][0]), int(valores["size"][1]), int(valores["seed"]))

    mapa._make_world(int(valores["scale"]), int(valores["octaves"]), float(valores["persistence"]),
                     float(valores["lacunarity"]), float(valores["sea level"]), float(valores["coast level"]))
    
    height = mapa._color_world([float(valores["sea level"]), float(valores["coast level"]), float(valores["land level"]), float(valores["mountain level"])])
    heat = mapa._color_temperature()
    hum = mapa._color_humidity()
    biome = mapa._color_biomes(float(valores["sea level"]), float(valores["coast level"]), float(valores["land level"]), float(valores["mountain level"]))

    window.mapa.set_maps([biome, height, heat, hum])
    

generate_map()
window.generate.clicked.connect(generate_map)

view.app.exec()
