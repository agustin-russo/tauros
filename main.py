from Model import basic_mapping as bm
from View import view

window = view.MainWindow()
window.show()

def generate_map():
    valores = window.get_values()

    mapa = bm.MapGenerator(int(valores["size"]), int(valores["seed"]))

    mapa._perlin_noise(int(valores["scale"]), int(valores["octaves"]), float(valores["persistence"]), float(valores["lacunarity"]))
    mapa._color_world()

    window.mapa.set_map(mapa.world)


generate_map()
window.generate.clicked.connect(generate_map)

view.app.exec()
