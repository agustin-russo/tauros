from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit, QPushButton, QScrollArea, QRadioButton, QButtonGroup
from PySide6.QtCore import Qt
import qdarktheme
from PySide6.QtGui import QFont, QFontDatabase, QIntValidator, QDoubleValidator
from ui.map_widget import MapWidget


app = QApplication()
app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

font_path = "TAUROS/assets/fonts/InterVariable.ttf"
font_id = QFontDatabase.addApplicationFont(font_path)
families = QFontDatabase.applicationFontFamilies(font_id)
app.setFont(QFont(families[0], 11))

title_font = QFont(families[0], 32)
title_font.setBold(True)
subtitle_font = QFont(families[0], 26)


class BasicOptions:
    def __init__(self, text="", default="", int_only=False, double_only=False):
        self.widget = QWidget()
        self.layout = QHBoxLayout(self.widget)
        self.label = QLabel(text)
        #self.label.setFont(subtitle_font)
        self.line = QLineEdit()
        self.line.setFixedWidth(60)

        if int_only:
            self.line.setValidator(QIntValidator())

        if double_only:
            self.line.setValidator(QDoubleValidator())

        self.line.setText(default)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line)

    def _connect(self, layout):
        layout.addWidget(self.widget)

class DoubleLineOptions(BasicOptions):
    def __init__(self, text="", default="", int_only=False, double_only=False):
        super().__init__(text, default, int_only, double_only)
        self.line2 = QLineEdit()
        self.line2.setFixedWidth(60)

        if int_only:
            self.line2.setValidator(QIntValidator())

        if double_only:
            self.line2.setValidator(QDoubleValidator())

        self.line2.setText(default)
        self.layout.addWidget(self.line2)
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tauros Versión 0.0.1")

        container = QWidget()
        layout = QHBoxLayout(container)
        scroll_area = QScrollArea()
        scroll_area.verticalScrollBar()
        option_container = QWidget()
        opciones = QVBoxLayout(option_container)

        self.mapa = MapWidget()
        mapa_widget = QWidget()
        mapa_layout = QVBoxLayout(mapa_widget)
        mapa_layout.addWidget(self.mapa)

        # Nuevo, para cambiar entre mapas
        selection_widget = QWidget()
        selection_layout = QHBoxLayout(selection_widget)
        self.selection = QButtonGroup()

        button0 = QRadioButton("Biomes")
        button1 = QRadioButton("Height")
        button2 = QRadioButton("Temperature")
        button3 = QRadioButton("Humidity")

        button0.setChecked(True)

        button0.toggled.connect(self.change_map)
        button1.toggled.connect(self.change_map)
        button2.toggled.connect(self.change_map)
        button3.toggled.connect(self.change_map)

        selection_layout.addWidget(button0)
        selection_layout.addWidget(button1)
        selection_layout.addWidget(button2)
        selection_layout.addWidget(button3)

        self.selection.addButton(button0, id=0)
        self.selection.addButton(button1, id=1)
        self.selection.addButton(button2, id=2)  
        self.selection.addButton(button3, id=3)

        mapa_layout.addWidget(selection_widget)

        label1 = QLabel("Opciones")
        label1.setFont(title_font)
        label1.setAlignment(Qt.AlignCenter)

        opciones.addWidget(label1)
        self.load_options(opciones)

        layout.addWidget(mapa_widget)
        scroll_area.setWidget(option_container)
        scroll_area.setMinimumWidth(230)
        layout.addWidget(scroll_area)

        self.setCentralWidget(container)

    def load_options(self, opciones):
        self.opciones = []
        # Seed
        self.seed = BasicOptions("Seed", "0", True)
        self.seed._connect(opciones)
        self.opciones.append(self.seed)

        # Size
        self.size_op = DoubleLineOptions("Size", "512", True)
        self.size_op._connect(opciones)
        self.opciones.append(self.size_op)

        # Scale
        self.scale = BasicOptions("Scale", "100", True)
        self.scale._connect(opciones)
        self.opciones.append(self.scale)

        # Octaves
        self.octaves = BasicOptions("Octaves", "6", True)
        self.octaves._connect(opciones)
        self.opciones.append(self.octaves)

        # Peristence
        self.persistence = BasicOptions("Persistence", "0.5", double_only=True)
        self.persistence._connect(opciones)
        self.opciones.append(self.persistence)

        # Lacunarity
        self.lacunarity = BasicOptions("Lacunarity", "2.0", double_only=True)
        self.lacunarity._connect(opciones)
        self.opciones.append(self.lacunarity)

        label1 = QLabel("---------------------------")
        label1.setAlignment(Qt.AlignCenter)
        opciones.addWidget(label1)

        self.load_terrain_options(opciones)

        # Button
        self.generate = QPushButton("Generate")
        opciones.addWidget(self.generate)

    def load_terrain_options(self, opciones):
        # Sea Level
        self.sea = BasicOptions("Sea level", "0.55", double_only=True)
        self.sea._connect(opciones)
        self.opciones.append(self.sea)

        # Coast Level
        self.coast = BasicOptions("Coast level", "0.60", double_only=True)
        self.coast._connect(opciones)
        self.opciones.append(self.coast)

        # Land Level
        self.land = BasicOptions("Land level", "0.80", double_only=True)
        self.land._connect(opciones)
        self.opciones.append(self.land)

        # Mountain Level
        self.mountain = BasicOptions("Mountain level", "0.90", double_only=True)
        self.mountain._connect(opciones)
        self.opciones.append(self.mountain)


    def get_values(self):
        valores = {}
        for i in self.opciones:
            if i.label.text().lower() == "size":
                valores[i.label.text().lower()] = (i.line.text(), i.line2.text())
                continue

            valores[i.label.text().lower()] = i.line.text()
        
        return valores

    def change_map(self, checked):
        if checked:
            self.mapa.change_map(self.selection.id(self.selection.checkedButton()))
