from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QLineEdit, QPushButton
from PySide6.QtCore import Qt
import qdarktheme
from PySide6.QtGui import QFont, QFontDatabase, QIntValidator, QDoubleValidator, QPainter, QImage
import numpy as np


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

        # Button
        self.generate = QPushButton("Generate")
        opciones.addWidget(self.generate)

    def get_values(self):
        valores = {}
        for i in self.opciones:
            if i.label.text().lower() == "size":
                valores[i.label.text().lower()] = (i.line.text(), i.line2.text())
                continue

            valores[i.label.text().lower()] = i.line.text()
        
        return valores


# Mapa para dibujar

class MapWidget(QWidget):
    def __init__(self, rows=512, cols=512, pixel_size=1):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.pixel_size = pixel_size

        self.map_data = np.zeros((self.cols, self.rows), dtype=np.uint32)
        self.cached_image = None

        self.update_widget_size()
        self.regenerate_image()

    def set_pixel_size(self, new_size):
        self.pixel_size = new_size
        self.update_widget_size()
        self.regenerate_image()
        self.update()

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
        arr = self.map_data.astype(np.uint32)
        buf = memoryview(arr)
        bytes_per_line = arr.strides[0]

        img = QImage(
            buf,
            self.cols,
            self.rows,
            bytes_per_line,
            QImage.Format_RGB32
        )

        if self.pixel_size > 1:
            img = img.scaled(
                self.cols * self.pixel_size,
                self.rows * self.pixel_size
            )

        self.cached_image = img

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.cached_image)

