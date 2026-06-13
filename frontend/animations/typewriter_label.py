"""
typewriter_label.py

Contiene la clase `TypewriterLabel`, una etiqueta (`QLabel`) animada que muestra texto
como si se estuviera escribiendo carácter por carácter, al estilo de una máquina de escribir.

Características:
- Uso de `QTimer` para animar la aparición progresiva del texto.
- Ideal para mensajes dinámicos en interfaces de bienvenida.
- Integración sencilla con layouts de PyQt5.

Requiere:
    - PyQt5
"""

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QLabel

class TypewriterLabel(QLabel):

    """
    Inicializa la etiqueta y configura el temporizador para animar el texto.

    Args:
        text (str): Texto completo que se mostrará con el efecto máquina de escribir.
        parent (QWidget, opcional): Widget padre. Por defecto es None.
    """
    def __init__(self, text, parent=None):
        super().__init__(parent)
        
        self.full_text = text
        self.current_text = ""
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateText)
        self.timer.start(50)


    """
    Añade el siguiente carácter del texto original a la etiqueta actual.

    Se llama automáticamente cada 50 ms mediante un `QTimer`.
    Cuando el texto está completo, detiene la animación.
    """
    def updateText(self):
        if len(self.current_text) < len(self.full_text):
            self.current_text += self.full_text[len(self.current_text)]
            self.setText(self.current_text)
        else:
            self.timer.stop()