"""
rotating_logo_mw.py

Contiene la clase `RotatingLogo`, un widget decorativo que muestra el logo
girando suavemente en el eje horizontal. Usado como elemento visual en la cabecera
de la aplicación principal (`MainWindow`).

Características:
- Rotación continua mediante `QTimer`.
- Transformación de escala horizontal para simular giro en eje Y.
- Renderizado optimizado con antialiasing.

Requiere:
    - PyQt5
    - Imagen del logo en `images/`
"""

import math

from PyQt5.QtCore import Qt, QTimer, QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap, QTransform

class RotatingLogo(QWidget):

    """
    Inicializa el logo, lo escala y comienza la animación de rotación.

    Args:
        logo_path (str): Ruta de la imagen del logo.
        parent (QWidget, opcional): Widget padre.
    """
    def __init__(self, logo_path="images/logoDB_Blanco.png", parent=None):
        super().__init__(parent)
        self.logo = QPixmap(logo_path)
        self.logo = self.logo.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        self.angle = 0
        self.timer = QTimer(self)
        
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)
       
        self.setFixedSize(60, 60)


    """
    Actualiza el ángulo de rotación y redibuja el widget.
    """
    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()


    """
    Dibuja el logo con una transformación de rotación horizontal animada.

    Se utiliza una escala horizontal basada en `cos(angle)` para simular
    una rotación 3D (como si girara en su eje Y).
    """
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