from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit, QPushButton
from PySide6.QtCore import Qt
import qdarktheme
from PySide6.QtGui import QFont, QFontDatabase, QIntValidator, QDoubleValidator, QPainter, QColor, QImage
from core.basic_mapping import colors

app = QApplication()
app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

font_path = "TAUROS/fonts/InterVariable.ttf"
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tauros Versión 0.0.1")

        container = QWidget()
        layout = QHBoxLayout(container)
        option_container = QWidget()
        opciones = QVBoxLayout(option_container)

        self.mapa = MapWidget()

        label1 = QLabel("Opciones")
        label1.setFont(title_font)
        label1.setAlignment(Qt.AlignCenter)

        opciones.addWidget(label1)
        self.load_options(opciones)

        layout.addWidget(self.mapa)
        layout.addWidget(option_container)

        self.setCentralWidget(container)

    def load_options(self, opciones):
        self.opciones = []
        # Seed
        self.seed = BasicOptions("Seed", "0", True)
        self.seed._connect(opciones)
        self.opciones.append(self.seed)

        # Size
        self.size_op = BasicOptions("Size", "512", True)
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

        # Button
        self.generate = QPushButton("Generate")
        opciones.addWidget(self.generate)

    def get_values(self):
        valores = {}
        for i in self.opciones:
            valores[i.label.text().lower()] = i.line.text()
        
        return valores


# Mapa para dibujar

class MapWidget(QWidget):
    def __init__(self, rows=512, cols=512, pixel_size=1):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.pixel_size = pixel_size

        self.map_data = [[0 for _ in range(cols)] for _ in range(rows)]

        # Imagen cacheada
        self.cached_image = None

        self.update_widget_size()
        self.regenerate_image()

    # Cambiar el tamaño de cada píxel
    def set_pixel_size(self, new_size):
        self.pixel_size = new_size
        self.update_widget_size()
        self.regenerate_image()
        self.update()

    # Cambiar completamente el mapa
    def set_map(self, new_map):
        self.map_data = new_map
        self.rows = len(new_map)
        self.cols = len(new_map[0])
        self.update_widget_size()
        self.regenerate_image()
        self.update()

    def update_widget_size(self):
        self.setFixedSize(
            self.cols * self.pixel_size,
            self.rows * self.pixel_size
        )

    def regenerate_image(self):
        w = self.cols * self.pixel_size
        h = self.rows * self.pixel_size

        img = QImage(w, h, QImage.Format_RGB32)
        painter = QPainter(img)

        for row in range(self.rows):
            for col in range(self.cols):
                color = QColor(colors[self.map_data[row][col]])
                painter.fillRect(
                    col * self.pixel_size,
                    row * self.pixel_size,
                    self.pixel_size,
                    self.pixel_size,
                    color
                )

        painter.end()
        self.cached_image = img

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.cached_image)

