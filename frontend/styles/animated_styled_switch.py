"""
animated_styled_switch.py

Contiene la clase `AnimatedStyledSwitch`, un interruptor personalizado con animación
utilizado para alternar entre el modo claro y oscuro de la interfaz.

Simula un switch moderno con animaciones suaves, círculo deslizante e iconos representativos.
Ideal para menús de configuración modernos.

Características:
- Basado en `QCheckBox`.
- Uso de `QPropertyAnimation`.
- Estilo completamente personalizado mediante `paintEvent`.

Requiere:
    - PyQt5
    - Iconos en `images/claro.png` y `images/oscuro.png`
"""

from PyQt5.QtWidgets import QCheckBox
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty

class AnimatedStyledSwitch(QCheckBox):

    """
    Inicializa el interruptor, establece estilo base y conecta la animación al cambio de estado.

    Args:
        parent (QWidget, opcional): Widget padre.
    """
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


    """
    Dibuja el interruptor: fondo redondeado, círculo animado e icono del modo actual.

    El color y el icono cambian según el estado (`checked` o no).
    """
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


    """
    Lanza la animación suave del círculo deslizante al cambiar el estado del switch.
    """
    def start_animation(self):
        self.anim = QPropertyAnimation(self, b"circle_position")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        
        start = 2 if not self.isChecked() else self.width() - 26
        end = self.width() - 26 if not self.isChecked() else 2
       
        self.anim.setStartValue(start)
        self.anim.setEndValue(end)
        self.anim.start()


    """
    Getter de la propiedad `circle_position`.

    Returns:
        int: Posición actual del círculo.
    """
    def get_circle_position(self):
        return self._circle_position


    """
    Setter de la propiedad `circle_position`.

    Actualiza la posición del círculo y repinta el widget.

    Args:
        pos (int): Nueva posición horizontal del círculo.
    """
    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()


    """
    Propiedad Qt que permite animar la posición del círculo mediante `QPropertyAnimation`.
    """
    @pyqtProperty(int)
    def circle_position(self):
        return self._circle_position


    # Setter para la posición del círculo
    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()


    """
    Alterna el estado del switch al hacer clic izquierdo, disparando la animación.
    """
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setChecked(not self.isChecked())
            super().mouseReleaseEvent(event)