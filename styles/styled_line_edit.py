from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QIcon

# Clase para dar estilo a los campos de edición
class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder, icon):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                padding: 12px 12px 12px 40px;
                border: 2px solid #FFA500;
                border-radius: 15px;
                background: transparent;
                color: white;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #FF8C00;
            }
        """)
        self.setTextMargins(40, 0, 0, 0)
        
        icon_label = QLabel(self)
        icon_label.setPixmap(QIcon(icon).pixmap(QSize(24, 24)))
        icon_label.setStyleSheet("background: transparent;")
        icon_label.move(10, 8)