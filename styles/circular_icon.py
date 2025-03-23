from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

# Clase para crear los círculos de los card de InfoView
class CircularIcon(QLabel):
    def __init__(self, icon_path, size=80):
        super().__init__()
        self.size = size
        self.setFixedSize(size, size)
        icon_size = int(size * 0.65)
        self.pixmap = QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.setPen(Qt.white)
        painter.drawEllipse(0, 0, self.size, self.size)
        x = (self.size - self.pixmap.width()) // 2
        y = (self.size - self.pixmap.height()) // 2
        painter.drawPixmap(x, y, self.pixmap)