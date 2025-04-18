from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

# Clase para darle estilo a los botones
class StyledButton(QPushButton):
    def __init__(self, text, icon=None, theme="light"):
        super().__init__(text)

        if theme == "dark":
            bg_color = "#FF5500"
            hover_color = "#FF7700"
            border_color = "white"
        else:
            bg_color = "#FFA500"
            hover_color = "#FF8C00"
            border_color = "white"

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                color: white;
                padding: 12px 24px;
                text-align: center;
                font-size: 18px;
                margin: 4px 2px;
                border-radius: 20px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 2px solid {hover_color};
            }}
        """)

        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(24, 24))
