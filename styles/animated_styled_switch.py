from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty

# Clase para crear un switch animado en la vista de configuración para cambiar entre modo claro y oscuro
class AnimatedStyledSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(60, 28)
        self._circle_position = 2

        self.animation = QPropertyAnimation(self, b"pos")
        self.stateChanged.connect(self.start_animation)

        self.setStyleSheet("""
            QCheckBox {
                background-color: none;
            }
            QCheckBox::indicator {
                width: 0;
                height: 0;
            }
        """)


    # Personalizar el aspecto del switch
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background
        bg_color = QColor("#FF5500") if self.isChecked() else QColor("#aaa")
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 14, 14)

        # Circle + icono dentro
        circle_color = QColor("white")
        painter.setBrush(circle_color)
        x_pos = self._circle_position
        painter.drawEllipse(x_pos, 2, 24, 24)

        # Dibujar icono encima del círculo
        icon_path = "images/oscuro.png" if self.isChecked() else "images/claro.png"
        icon = QPixmap(icon_path).scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        painter.drawPixmap(x_pos + 4, 6, icon)
        painter.end()


    # Animación al cambiar el estado del switch
    def start_animation(self):
        self.anim = QPropertyAnimation(self, b"circle_position")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        
        start = 2 if not self.isChecked() else self.width() - 26
        end = self.width() - 26 if not self.isChecked() else 2
       
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()


    # Propiedad para la posición del círculo
    def get_circle_position(self):
        return self._circle_position

    # Setter para la posición del círculo
    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    # Propiedad para la posición del círculo
    @pyqtProperty(int)
    def circle_position(self):
        return self._circle_position

    # Setter para la posición del círculo
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    # Método para manejar el evento de pulsar el switch
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked())
            super().mouseReleaseEvent(event)