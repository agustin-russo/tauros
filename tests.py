import sys
import os
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QFontDatabase, QFont

app = QApplication(sys.argv)

# Cargar la fuente desde archivo (aunque esté instalada)
font_path = "TAUROS/fonts/InterVariable.ttf"

print("Existe el archivo:", os.path.exists(font_path))

font_id = QFontDatabase.addApplicationFont(font_path)
families = QFontDatabase.applicationFontFamilies(font_id)

print("Families cargadas:", families)

if families:
    app.setFont(QFont(families[0], 100))
else:
    print("o se pudo cargar Inter")

label = QLabel("Esta debería verse con Inter")
label.show()

sys.exit(app.exec())
