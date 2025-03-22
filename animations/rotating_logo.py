import math, os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPixmap, QTransform
from PyQt5.QtWidgets import QWidget

# Ruta del logo
LOGO_PATH = "images/logoDB_Blanco.png"

# Clase para rotar el logo 360º
class RotatingLogoWidget(QWidget):
    def __init__(self, logo_path, parent=None):
        super().__init__(parent)
        self.logo_path = logo_path
        self.loadLogo()
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)
        self.setFixedSize(300, 300)

    # Cargo el logo y lo escalo
    def loadLogo(self):
        if os.path.exists(self.logo_path):
            self.logo = QPixmap(self.logo_path)
            self.logo = self.logo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            print(f"Error: No se encontró el logo en '{self.logo_path}'")
            self.logo = QPixmap()

    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        angle_radians = math.radians(self.angle)
        scale_x = abs(math.cos(angle_radians))
        
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(scale_x, 1.0)
        transform.translate(-self.logo.width() // 2, -self.logo.height() // 2)
        
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.logo)
        painter.resetTransform()