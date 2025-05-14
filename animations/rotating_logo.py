"""
rotating_logo.py

Módulo que define el widget `RotatingLogoWidget`, encargado de mostrar un logo
girando suavemente sobre su eje horizontal, como un elemento decorativo principal
en la pantalla de bienvenida.

Características:
- Transformaciones gráficas con `QTransform`.
- Efecto visual de rotación 3D usando `cos(angle)`.
- Comprobación del archivo del logo en disco.
- Temporizador (`QTimer`) para actualizar la animación cada 50 ms.

Requiere:
    - PyQt5
    - Archivo de imagen accesible en `images/`
"""

import math, os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPixmap, QTransform

# Ruta del logo
LOGO_PATH = "images/logoDB_Blanco.png"

# Clase para rotar el logo 360º
class RotatingLogoWidget(QWidget):

    """
    Inicializa el widget, carga el logo y comienza la rotación animada.

    Args:
        logo_path (str): Ruta a la imagen del logo.
        parent (QWidget, opcional): Widget padre.
    """
    def __init__(self, logo_path, parent=None):
        super().__init__(parent)
        
        self.logo_path = logo_path
        self.loadLogo()
        
        self.angle = 0
       
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)
        
        self.setFixedSize(300, 300)


    """
    Carga el logo desde el sistema de archivos y lo escala proporcionalmente.

    Si el archivo no se encuentra, carga un `QPixmap` vacío.
    """
    def loadLogo(self):
        if os.path.exists(self.logo_path):
            self.logo = QPixmap(self.logo_path)
            self.logo = self.logo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            print(f"Error: No se encontró el logo en '{self.logo_path}'")
            self.logo = QPixmap()


    """
    Aumenta el ángulo de rotación y solicita el repintado del widget.
    """
    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()


    """
    Dibuja el logo rotado aplicando una transformación de escala horizontal animada.

    Simula un giro 3D en el eje Y, con efecto visual continuo.
    """
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