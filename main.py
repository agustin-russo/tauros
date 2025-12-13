from core import basic_mapping as bm
from ui import view
#import time

window = view.MainWindow()
window.show()

def generate_map():
    #counter = time.perf_counter()
    valores = window.get_values()

    mapa = bm.MapGenerator(int(valores["size"][0]), int(valores["size"][1]), int(valores["seed"]))

    mapa._make_world(int(valores["scale"]), int(valores["octaves"]), float(valores["persistence"]), float(valores["lacunarity"]), float(valores["sea level"]))
    height = mapa._color_world([float(valores["sea level"]), float(valores["coast level"]), float(valores["land level"]), float(valores["mountain level"])])
    heat = mapa._color_temperature()

    #end_time1 = time.perf_counter()
    #print("Core done in ", end_time1-counter)

    window.mapa.set_maps([height, heat])
    #end_time = time.perf_counter()
    #print("World done in ", end_time-counter)
    

generate_map()
window.generate.clicked.connect(generate_map)

view.app.exec()
