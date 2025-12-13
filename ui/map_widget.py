import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QImage


class MapWidget(QWidget):
    def __init__(self, rows=512, cols=512, pixel_size=1):
        super().__init__()

        self.rows = rows
        self.cols = cols
        self.pixel_size = pixel_size

        self.maps = [np.zeros((self.cols, self.rows), dtype=np.uint32), ]
        self.selection = 0
        self.cached_images = []

        self.update_widget_size()
        self.cached_images.append(self.regenerate_image(self.maps[0]))

    def set_pixel_size(self, new_size):
        self.pixel_size = new_size
        self.update_widget_size()
        self.regenerate_image()
        self.update()

    def set_maps(self, new_maps):
        self.maps = new_maps
        self.rows = len(new_maps[0])
        self.cols = len(new_maps[0][0])
        self.update_widget_size()

        self.cached_images = [
            self.regenerate_image(m) for m in new_maps
        ]
        
        self.update()

    def update_widget_size(self):
        self.setFixedSize(
            self.cols * self.pixel_size,
            self.rows * self.pixel_size
        )
    
    def regenerate_image(self, mapa):
        arr = mapa.astype(np.uint32)
        buf = memoryview(arr)
        bytes_per_line = arr.strides[0]

        img = QImage(
            buf,
            self.cols,
            self.rows,
            bytes_per_line,
            QImage.Format_ARGB32
        )

        if self.pixel_size > 1:
            img = img.scaled(
                self.cols * self.pixel_size,
                self.rows * self.pixel_size
            )

        return img

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.cached_images[self.selection])

    
    def change_map(self, selection):
        self.selection = selection
        self.update()

