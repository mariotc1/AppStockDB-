from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel

# Clase para dar efecto de máquina de escribir al texto de la pantalla de bienvenida
class TypewriterLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.full_text = text
        self.current_text = ""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateText)
        self.timer.start(50)

    def updateText(self):
        if len(self.current_text) < len(self.full_text):
            self.current_text += self.full_text[len(self.current_text)]
            self.setText(self.current_text)
        else:
            self.timer.stop()