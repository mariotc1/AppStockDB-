"""
styled_line_edit.py

Define la clase `StyledLineEdit`, una entrada de texto personalizada con:
- Borde redondeado.
- Padding interior.
- Icono embebido a la izquierda.
- Colores adaptados dinámicamente al tema claro/oscuro.

Usado en:
- Formularios de login, registro y perfil.

Requiere:
    - PyQt5
    - Ruta a un icono PNG o SVG.
    - Archivo de configuración `config/settings.json` (opcional si se pasa el tema manualmente).
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QIcon
import json

class StyledLineEdit(QLineEdit):

    """
    Inicializa el campo de texto con estilos y un icono visual.

    Args:
        placeholder (str): Texto guía mostrado cuando el campo está vacío.
        icon (str): Ruta del icono que se muestra a la izquierda del campo.
        theme (str, opcional): Tema actual (light/dark). Si no se indica, se carga desde settings.json.
    """
    def __init__(self, placeholder, icon, theme=None):
        super().__init__()

        # Si no se pasa el tema como argumento, intenta detectarlo automáticamente
        if theme is None:
            try:
                with open("config/settings.json", "r") as f:
                    config = json.load(f)
                    theme = config.get("theme", "light")
            except:
                theme = "light"

        self.setPlaceholderText(placeholder)

        # Colores según tema
        if theme == "dark":
            border_color = "#FF5500"
            focus_color = "#FF7700"
            bg_color = "#222222"
            text_color = "white"
        else:
            border_color = "#FFA500"
            focus_color = "#FF8C00"
            bg_color = "#FFFFFF"
            text_color = "#000000"

        self.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px 12px 12px 40px;
                border: 2px solid {border_color};
                border-radius: 15px;
                background-color: {bg_color};
                color: {text_color};
                font-size: 16px;
            }}
            QLineEdit:focus {{
                border-color: {focus_color};
            }}
            QLineEdit::placeholder {{
                color: #888888;
            }}
        """)

        self.setTextMargins(40, 0, 0, 0)

        icon_label = QLabel(self)
        icon_label.setPixmap(QIcon(icon).pixmap(QSize(24, 24)))
        icon_label.setStyleSheet("background: transparent; border: none;")
        icon_label.move(10, 8)