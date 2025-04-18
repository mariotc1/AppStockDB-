import math

from PyQt5.QtCore import Qt, QTimer, QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap, QTransform

# Clase para el giro del logo en la cabecera de la pantalla principal
class RotatingLogo(QWidget):
    def __init__(self, logo_path="images/logoDB_Blanco.png", parent=None):
        super().__init__(parent)
        self.logo = QPixmap(logo_path)
        self.logo = self.logo.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.angle = 0
        self.timer = QTimer(self)
        
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)
       
        self.setFixedSize(60, 60)


    # Método para actualizar el ángulo de rotación
    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()


    # Método para pintar el logo en la pantalla
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = self.rect()
        
        center_x = rect.width() // 2
        center_y = rect.height() // 2
       
        angle_radians = math.radians(self.angle)
        scale_x = abs(math.cos(angle_radians))
        
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(scale_x, 1.0)
        transform.translate(-self.logo.width() // 2, -self.logo.height() // 2)
        
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.logo)
        painter.resetTransform()