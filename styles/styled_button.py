from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

# Clase para darle estilo a los botones
class StyledButton(QPushButton):
    def __init__(self, text, icon=None):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                border: 2px solid white;
                color: white;
                padding: 12px 24px;
                text-align: center;
                font-size: 18px;
                margin: 4px 2px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
                border: 2px solid #FF8C00;
            }
        """)
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(24, 24))