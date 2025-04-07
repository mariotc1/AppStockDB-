from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QRadialGradient, QBrush, QColor

class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setModal(True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(30, 30, 30, 30)

        # Imagen estática
        self.spinner = QLabel(self)
        self.spinner.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("images/enProceso.png")
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Escala la imagen manteniendo la proporción
        self.spinner.setPixmap(pixmap)

        # Texto de carga
        self.label = QLabel("Cargando datos...\nPor favor espere", self)
        self.label.setFont(QFont("Arial", 16, QFont.Bold))
        self.label.setStyleSheet("""
            color: white;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
        """)
        self.label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.spinner)
        layout.addSpacing(20)
        layout.addWidget(self.label)

    # Pintar fondo con degradado radial y borde redondeado
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # Degradado radial para el fondo
        gradient = QRadialGradient(rect.center(), rect.width() / 2)
        gradient.setColorAt(0.0, QColor(50, 50, 50, 240))  # Gris oscuro semitransparente
        gradient.setColorAt(1.0, QColor(20, 20, 20, 240))  # Gris más oscuro

        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo con bordes redondeados
        painter.setBrush(QBrush(gradient))
        painter.setPen(QColor(255, 255, 255, 50))  # Borde blanco semitransparente
        painter.drawRoundedRect(rect.adjusted(5, 5, -5, -5), 15, 15) 
