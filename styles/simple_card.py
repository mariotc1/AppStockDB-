"""
simple_card.py

Define el widget `SimpleCard`, una tarjeta visual con:
- Fondo semitransparente.
- Borde suave.
- Radio redondeado.

Ideal para mostrar bloques de información con separación clara del fondo.

Usado comúnmente en:
- InfoView
- Vistas decorativas o informativas.

Requiere:
    - PyQt5
"""

from PyQt5.QtWidgets import QFrame

class SimpleCard(QFrame):

    """
    Inicializa la tarjeta con un estilo visual translúcido y bordes suaves.

    Args:
        parent (QWidget, opcional): Widget padre.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            SimpleCard {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
            }
        """)