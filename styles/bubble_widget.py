from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

# Clase para darle estilo de burbuja al chatbot
class BubbleWidget(QWidget):
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.is_user = is_user
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Icono circular del usuario o bot
        icon_label = QLabel()
        pixmap = QPixmap("images/usuaria.png" if self.is_user else "images/chatbot_icon.png")
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Convertir imagen a circular
        mask = QPixmap(40, 40)
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(0, 0, 40, 40)
        painter.end()

        pixmap.setMask(mask.mask())
        icon_label.setPixmap(pixmap)

        # Burbuja de texto
        bubble = QLabel(self.text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(280)
        bubble.setStyleSheet(f"""
            background-color: {'#0078D7' if self.is_user else '#2C3E50'};
            border-radius: 12px;
            padding: 12px;
            color: white;
            font-size: 16px;
        """)

        if self.is_user:
            layout.addStretch()
            layout.addWidget(bubble)
            layout.addWidget(icon_label)
        else:
            layout.addWidget(icon_label)
            layout.addWidget(bubble)
            layout.addStretch()