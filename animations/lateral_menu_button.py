"""
lateral_menu_button.py

Contiene la clase `LateralMenuButton`, utilizada para los botones del menú lateral en la MainWindow.

Permite un comportamiento visual dinámico: muestra solo el icono en modo colapsado y el texto completo
en modo expandido, aplicando estilos diferenciados para vistas principales y botones de acción.

Características:
- Icono configurable.
- Estilo adaptado a tema claro/oscuro.
- Comportamiento responsive al expandir/colapsar el menú lateral.

Requiere:
    - PyQt5
    - Archivo de configuración (`config/settings.json`)
"""

import json

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QSizePolicy


class LateralMenuButton(QPushButton):

    """
    Inicializa el botón con su icono, tamaño y comportamiento temático.

    Args:
        text (str): Texto que se mostrará al expandirse.
        icon_path (str): Ruta del icono del botón.
        is_main_view (bool): Indica si el botón representa una vista principal.
        parent (QWidget, optional): Widget padre. Por defecto, None.
    """
    def __init__(self, text, icon_path, is_main_view=True, parent=None):
        super().__init__("", parent)

        self.full_text = text
        self.full_icon = QIcon(icon_path)
        
        self.setIcon(self.full_icon)
        self.setIconSize(QSize(32, 32))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(60)
        self.is_main_view = is_main_view

        # Detecto si la app está en modo claro/oscuro desde settings.json
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.theme = config.get("theme", "light")
        except:
            self.theme = "light"

        self.setExpanded(False)


    """
    Activa o desactiva el modo expandido del botón, actualizando su texto y estilo.

    Args:
        expanded (bool): True para mostrar el texto, False para ocultarlo.
    """
    def setExpanded(self, expanded: bool):
        # Hover color adaptado según el tema claro/oscuro
        if self.theme == "dark":
            hover_color = "rgba(255, 85, 0, 0.8)"   # naranja oscuro
        else:
            hover_color = "rgba(255, 165, 0, 0.8)"  # naranja claro

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
                    background-color: {hover_color};
                }}
            """)
        else:
            self.setText("")
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                    border-radius: 5px;
                    text-align: center;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: {hover_color};
                }}
            """)
        self.update()