from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton,QSizePolicy
from PyQt5.QtGui import QIcon

# Clase para ele fecto de que se uestre el menu lateral de la pantalla principal al pasar el ratón
class LateralMenuButton(QPushButton):
    def __init__(self, text, icon_path, is_main_view=True, parent=None):
        super().__init__("", parent)
        self.full_text = text
        self.full_icon = QIcon(icon_path)
        self.setIcon(self.full_icon)
        self.setIconSize(QSize(32, 32))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(60)
        self.is_main_view = is_main_view
        self.setExpanded(False)

    def setExpanded(self, expanded: bool):
        if expanded:
            text_color = "white" if self.is_main_view else "black"
            font_weight = "bold"
            font_size = "16px" if self.is_main_view else "14px"
            self.setText("  " + self.full_text)
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 255, 255, 0.1);
                    color: {text_color};
                    border: none;
                    border-radius: 5px;
                    font-size: {font_size};
                    font-weight: {font_weight};
                    text-align: left;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 165, 0, 0.8);
                }}
            """)
            
        else:
            self.setText("")
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 5px;
                    text-align: center;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 165, 0, 0.8);
                }
            """)
        self.update()