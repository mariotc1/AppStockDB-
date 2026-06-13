"""
styled_button.py

Contiene la clase `StyledButton`, un botón estilizado que adapta su apariencia
a los temas claro u oscuro.

Aplicaciones típicas:
- Formularios.
- Navegación.
- Confirmaciones o acciones destacadas.

Características:
- Colores planos (naranja, blanco).
- Bordes redondeados.
- Hover animado.
- Icono opcional.

Requiere:
    - PyQt5
    - (Opcional) Ruta a un archivo de icono válido.
"""

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

class StyledButton(QPushButton):

    """
    Inicializa un botón estilizado con texto, tema y un posible icono.

    Args:
        text (str): Texto que se mostrará en el botón.
        icon (str, opcional): Ruta del icono a mostrar junto al texto.
        theme (str): Tema de la aplicación ("light" o "dark"). Define colores de fondo y hover.
    """
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