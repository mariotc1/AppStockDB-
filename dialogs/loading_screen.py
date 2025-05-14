"""
loading_screen.py

Este módulo define la clase `LoadingScreen`, que representa una pantalla modal de
carga utilizada durante operaciones importantes como el inicio de sesión, el registro
o la redirección entre vistas críticas.

Elementos:
- Imagen central de tipo "en proceso".
- Texto claro y visible centrado.
- Fondo con degradado radial y esquinas redondeadas.

Requiere:
    - PyQt5
    - Imagen: images/enProceso.png
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPainter, QRadialGradient, QBrush, QColor

class LoadingScreen(QDialog):

    """
    Inicializa el cuadro de carga, ocultando bordes de ventana y aplicando fondo transparente.
    Configura la imagen del spinner y un mensaje de espera centrado.

    Notas:
    - El cuadro se presenta de forma modal (`setModal(True)`).
    - El fondo utiliza `WA_TranslucentBackground` y bordes redondeados.
    """
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
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.spinner.setPixmap(pixmap)

        # Texto de carga
        self.label = QLabel("Cargando datos...\nPor favor, espere", self)
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


    """
    Sobrescribe el evento de pintura para dibujar un fondo con un degradado radial
    oscuro y bordes redondeados que mejoran la estética del cuadro de carga.

    Args:
        event (QPaintEvent): Evento de dibujo recibido por el sistema.
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        # Degradado radial para el fondo
        gradient = QRadialGradient(rect.center(), rect.width() / 2)
        gradient.setColorAt(0.0, QColor(50, 50, 50, 240))
        gradient.setColorAt(1.0, QColor(20, 20, 20, 240))

        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fondo con bordes redondeados
        painter.setBrush(QBrush(gradient))
        painter.setPen(QColor(255, 255, 255, 50))
        painter.drawRoundedRect(rect.adjusted(5, 5, -5, -5), 15, 15) 
