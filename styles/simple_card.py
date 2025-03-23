from PyQt5.QtWidgets import QFrame

# Clase para dar formato sencillo al card de InfoView
class SimpleCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            SimpleCard {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
            }
        """)