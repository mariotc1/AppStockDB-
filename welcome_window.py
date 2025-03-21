import sys
import math
import os
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QSequentialAnimationGroup, QParallelAnimationGroup
from PyQt5.QtGui import QPainter, QPixmap, QTransform, QLinearGradient, QBrush, QColor, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QGraphicsOpacityEffect, QGraphicsDropShadowEffect
)

# Ruta de las imágenes
LOGO_PATH = "images/logoDB_Blanco.png"
REFRESH_ICON_PATH = "images/refrescar.png"
CLOSE_ICON_PATH = "images/cerrar.png"

class RotatingLogoWidget(QWidget):
    def __init__(self, logo_path, parent=None):
        super().__init__(parent)
        self.logo_path = logo_path
        self.loadLogo()
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)
        self.setFixedSize(300, 300)

    def loadLogo(self):
        """Carga el logo y lo escala."""
        if os.path.exists(self.logo_path):
            self.logo = QPixmap(self.logo_path)
            self.logo = self.logo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            print(f"Error: No se encontró el logo en '{self.logo_path}'")
            self.logo = QPixmap()

    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        center_x = self.width() // 2
        center_y = self.height() // 2
        angle_radians = math.radians(self.angle)
        scale_x = abs(math.cos(angle_radians))
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(scale_x, 1.0)
        transform.translate(-self.logo.width() // 2, -self.logo.height() // 2)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.logo)
        painter.resetTransform()

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

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.animations = []
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen() 
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Layout para los botones de la parte superior
        top_buttons_layout = QHBoxLayout()
        self.refresh_button = QPushButton(QIcon(REFRESH_ICON_PATH), "")
        self.close_button = QPushButton(QIcon(CLOSE_ICON_PATH), "")
        self.refresh_button.setFixedSize(40, 40)
        self.close_button.setFixedSize(40, 40)
        self.refresh_button.clicked.connect(self.refreshApp)
        self.close_button.clicked.connect(self.close)
        btn_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 50);
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """
        self.refresh_button.setStyleSheet(btn_style)
        self.close_button.setStyleSheet(btn_style)
        self.applyShadow(self.refresh_button)
        self.applyShadow(self.close_button)
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(self.refresh_button)
        top_buttons_layout.addWidget(self.close_button)
        main_layout.addLayout(top_buttons_layout)

        # Logo rotatorio
        self.rotating_logo = RotatingLogoWidget(LOGO_PATH)
        main_layout.addWidget(self.rotating_logo, alignment=Qt.AlignCenter)

        # Layout para el contenido principal (títulos y botones)
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("¡Bienvenido a DB Inmuebles!")
        self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.subtitle_label = QLabel("Sistema de Gestión de Stock")
        self.subtitle_label.setFont(QFont("Arial", 18))
        self.subtitle_label.setStyleSheet("color: white;")
        self.subtitle_label.setAlignment(Qt.AlignCenter)

        # Layout para los botones de inicio de sesión y registro
        button_layout = QHBoxLayout()
        self.btn_login = QPushButton("INICIAR SESIÓN")
        self.btn_register = QPushButton("REGISTRARSE")
        btn_gradient_style = """
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #FFA500, stop:1 #FF8C00);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #FFB52E, stop:1 #FFA500);
            }
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #FF8C00, stop:1 #FFA500);
            }
        """
        self.btn_login.setStyleSheet(btn_gradient_style)
        self.btn_register.setStyleSheet(btn_gradient_style)
        self.applyShadow(self.btn_login)
        self.applyShadow(self.btn_register)
        button_layout.addWidget(self.btn_login)
        button_layout.addWidget(self.btn_register)

        content_layout.addWidget(self.title_label)
        content_layout.addWidget(self.subtitle_label)
        content_layout.addSpacing(40)
        content_layout.addLayout(button_layout)

        # Etiqueta de la línea de etiqueta con efecto de máquina de escribir
        self.tagline_label = TypewriterLabel("Tecnología y excelencia en cada detalle")
        self.tagline_label.setFont(QFont("Courier", 14, QFont.StyleItalic))
        self.tagline_label.setStyleSheet("color: white;")
        self.tagline_label.setAlignment(Qt.AlignCenter)
        content_layout.addSpacing(20)
        content_layout.addWidget(self.tagline_label)

        main_layout.addLayout(content_layout)
        main_layout.addStretch()

        # Etiqueta del pie de página
        footer_label = QLabel("© 2025 DB Inmuebles. Todos los derechos reservados.")
        footer_label.setStyleSheet("color: white; font-size: 18px;")
        footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer_label)

        self.setLayout(main_layout)

        # Conexión de los botones a sus respectivas funciones
        self.btn_login.clicked.connect(self.onLogin)
        self.btn_register.clicked.connect(self.onRegister)

        # Configuración de las animaciones
        self.setupAnimations()

    def setupAnimations(self):
        """Configura las animaciones de los elementos de la ventana."""
        self.fadeInWidget(self.title_label, 1500, QEasingCurve.OutCubic)
        self.fadeInWidget(self.subtitle_label, 2000, QEasingCurve.OutCubic)

        # Animaciones para los botones
        login_anim = self.createButtonAnimation(self.btn_login)
        register_anim = self.createButtonAnimation(self.btn_register)

        # Agrupa las animaciones de los botones para que se ejecuten en paralelo
        button_group = QParallelAnimationGroup()
        button_group.addAnimation(login_anim)
        button_group.addAnimation(register_anim)

        # Crea una secuencia de animación principal
        main_sequence = QSequentialAnimationGroup()
        main_sequence.addPause(2000)  # Pausa antes de iniciar las animaciones de los botones
        main_sequence.addAnimation(button_group)

        main_sequence.start()

    def createButtonAnimation(self, button):
        """Crea una animación de desplazamiento para el botón."""
        anim = QPropertyAnimation(button, b"pos")
        anim.setDuration(1000)
        start_pos = button.pos() + QPoint(0, 50)
        anim.setStartValue(start_pos)
        anim.setEndValue(button.pos())
        anim.setEasingCurve(QEasingCurve.OutElastic)
        return anim

    def applyShadow(self, widget):
        """Aplica un efecto de sombra al widget."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)

    def fadeInWidget(self, widget, duration=2000, easing=QEasingCurve.InOutQuad):
        """Realiza un efecto de fundido de entrada en el widget."""
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(easing)
        animation.start()
        self.animations.append(animation)

    def onLogin(self):
        """Muestra la ventana de inicio de sesión."""
        # Importa la ventana de inicio de sesión aquí para evitar dependencias circulares
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def onRegister(self):
        """Muestra la ventana de registro."""
        # Importa la ventana de registro aquí para evitar dependencias circulares
        from register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()

    def refreshApp(self):
        """Refresca la aplicación."""
        print("Refrescando la aplicación...")
        self.update()

    def paintEvent(self, event):
        """Pinta el fondo con un degradado."""
        painter = QPainter(self)
        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0.0, QColor(0, 0, 0))
        gradient.setColorAt(1.0, QColor(255, 140, 0))
        painter.fillRect(rect, QBrush(gradient))
        super().paintEvent(event)

    def showEvent(self, event):
        """Realiza una animación de fundido de entrada al mostrar la ventana."""
        self.setWindowOpacity(0)
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(1000)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        self.animations.append(anim)
        super().showEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Define el estilo de la aplicación
    app.setStyleSheet("""
        QWidget {
            background-color: #333; /* Fondo oscuro */
            color: white; /* Texto blanco */
            font-family: Arial, Helvetica, sans-serif;
        }
        QPushButton {
            background-color: #555; /* Botones grises */
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #777; /* Botones grises más claros al pasar el ratón */
        }
        QLabel {
            color: #eee;
        }
    """)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())