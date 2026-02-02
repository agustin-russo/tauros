from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLineEdit, QPushButton, QScrollArea, QRadioButton, QButtonGroup, QDialog, QFileDialog
from PySide6.QtCore import Qt
import qdarktheme
from PySide6.QtGui import QFont, QFontDatabase, QIntValidator, QDoubleValidator
from ui.map_widget import MapWidget
from core.saving_module import save_config, load_config
from core.routes import SAVES_DIR
import re


app = QApplication()
app.setStyleSheet(qdarktheme.load_stylesheet("dark"))

font_path = "TAUROS/assets/fonts/InterVariable.ttf"
font_id = QFontDatabase.addApplicationFont(font_path)
families = QFontDatabase.applicationFontFamilies(font_id)
app.setFont(QFont(families[0], 11))

title_font = QFont(families[0], 32)
title_font.setBold(True)
subtitle_font = QFont(families[0], 20)


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
        

class SaveDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Save configuration")

        layout = QVBoxLayout(self)
        label = QLabel("Name of the save file:")
        layout.addWidget(label)

        self.line = QLineEdit()
        self.line.setFixedWidth(120)
        self.line.setText("save1.json")

        layout.addWidget(self.line)

        self.warning = QLabel("")
        self.warning.hide()
        
        layout.addWidget(self.warning)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.saving)

        layout.addWidget(self.save_btn)
    
    def saving(self):
        text = self.line.text()
        regex = re.compile(r'^[^<>:"/\\|?*\x00-\x1F]+\.json$')

        if bool(regex.match(text)):
            self.accept()

        else:
            self.warning.setText("Invalid format")
            self.warning.show()

    @property
    def filename(self):
        return self.line.text()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tauros Versión 0.0.1")

        container = QWidget()
        layout = QHBoxLayout(container)
        scroll_area = QScrollArea()
        scroll_area.verticalScrollBar()
        option_container = QWidget()
        self.opciones_layout = QVBoxLayout(option_container)

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

        label1 = QLabel("Options")
        label1.setFont(title_font)
        label1.setAlignment(Qt.AlignCenter)

        self.opciones_layout.addWidget(label1)
        self.load_save_controls()
        self.build_options()

        layout.addWidget(mapa_widget)
        scroll_area.setWidget(option_container)
        scroll_area.setMinimumWidth(230)
        layout.addWidget(scroll_area)

        self.setCentralWidget(container)


    def load_save_controls(self):

        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setFrameShadow(QFrame.Sunken)


        linea2 = QFrame()
        linea2.setFrameShape(QFrame.HLine)
        linea2.setFrameShadow(QFrame.Sunken)

        label1 = QLabel("Configs")
        label1.setFont(subtitle_font)
        label1.setAlignment(Qt.AlignCenter)

        widget = QWidget()
        layout = QHBoxLayout(widget)
        self.save_btn = QPushButton("Save Config")
        self.save_btn.clicked.connect(self.save_config_options)
        layout.addWidget(self.save_btn)

        self.load_btn = QPushButton("Load Config")
        self.load_btn.clicked.connect(self.load_config_options)
        layout.addWidget(self.load_btn)

        self.opciones_layout.addWidget(linea)
        self.opciones_layout.addWidget(label1)
        self.opciones_layout.addWidget(widget)
        self.opciones_layout.addWidget(linea2)

    def build_options(self):
        self.opciones = []
        # Seed
        self.seed = BasicOptions("Seed", "0", True)
        self.seed._connect(self.opciones_layout)
        self.opciones.append(self.seed)

        # Size
        self.size_op = DoubleLineOptions("Size", "512", True)
        self.size_op._connect(self.opciones_layout)
        self.opciones.append(self.size_op)

        # Scale
        self.scale = BasicOptions("Scale", "100", True)
        self.scale._connect(self.opciones_layout)
        self.opciones.append(self.scale)

        # Octaves
        self.octaves = BasicOptions("Octaves", "6", True)
        self.octaves._connect(self.opciones_layout)
        self.opciones.append(self.octaves)

        # Peristence
        self.persistence = BasicOptions("Persistence", "0.5", double_only=True)
        self.persistence._connect(self.opciones_layout)
        self.opciones.append(self.persistence)

        # Lacunarity
        self.lacunarity = BasicOptions("Lacunarity", "2.0", double_only=True)
        self.lacunarity._connect(self.opciones_layout)
        self.opciones.append(self.lacunarity)

        linea = QFrame()
        linea.setFrameShape(QFrame.HLine)
        linea.setFrameShadow(QFrame.Sunken)
        self.opciones_layout.addWidget(linea)

        self.load_terrain_options(self.opciones_layout)

        # Button
        self.generate = QPushButton("Generate")
        self.opciones_layout.addWidget(self.generate)

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

    
    def save_config_options(self):
        dialog = SaveDialog()
        result = dialog.exec()

        if result:
            values = self.get_values()
            save_config(values, dialog.filename)

    
    def load_config_options(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load file",
            str(SAVES_DIR),                       
            "JSON files (*.json);;All files (*)"
        )

        if filename:
            values = load_config(filename)
            for i in self.opciones:
                if i.label.text().lower() == "size":
                    i.line.setText(values["size"][0])
                    i.line2.setText(values["size"][1])
                    continue

                i.line.setText(values[i.label.text().lower()])

            self.generate.click()
