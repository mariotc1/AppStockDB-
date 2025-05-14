"""
circular_icon.py

Define el widget `CircularIcon`, un componente gráfico que muestra un icono
centrado dentro de un círculo blanco, usado en tarjetas informativas o vistas decorativas.

Características:
- Escalado proporcional del icono.
- Alineación centrada.
- Renderizado antialiasing.
- Ideal para mostrar funcionalidades o categorías visualmente.

Requiere:
    - PyQt5
    - Ruta válida a un archivo de imagen para el icono
"""

from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

class CircularIcon(QLabel):

    """
    Inicializa el icono circular con la imagen proporcionada y un tamaño fijo.

    Args:
        icon_path (str): Ruta de la imagen del icono.
        size (int, opcional): Tamaño del contenedor circular en píxeles. Por defecto 80.
    """
    def __init__(self, icon_path, size=80):
        super().__init__()
        self.size = size
        self.setFixedSize(size, size)
        icon_size = int(size * 0.65)
        self.pixmap = QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    """
    Dibuja un círculo blanco y posiciona el icono centrado dentro del mismo.

    Usa antialiasing para suavizar los bordes.
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.setPen(Qt.white)
        painter.drawEllipse(0, 0, self.size, self.size)
        x = (self.size - self.pixmap.width()) // 2
        y = (self.size - self.pixmap.height()) // 2
        painter.drawPixmap(x, y, self.pixmap)