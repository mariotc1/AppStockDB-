import sys

from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QPoint, 
    QSequentialAnimationGroup, QParallelAnimationGroup
)

from PyQt5.QtGui import ( 
    QPainter, QLinearGradient, 
    QBrush, QColor, QFont, QIcon
)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
)

from animations.rotating_logo import RotatingLogoWidget
from animations.typewriter_label import TypewriterLabel


# Ruta de las imágenes: logo, cerrar y refrescar
LOGO_PATH = "images/logoDB_Blanco.png"

# Pantalla de Bienvenida 
class WelcomeWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.animations = []
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.showMaximized()
        self.initUI()
    

    # Creacion de la interfaz
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Logo con el efecto de giro 360º
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

        # Footer
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


    # Configuro las animaciones de los elementos de la ventana
    def setupAnimations(self):
        self.fadeInWidget(self.title_label, 1500, QEasingCurve.OutCubic)
        self.fadeInWidget(self.subtitle_label, 2000, QEasingCurve.OutCubic)

        # Animaciones para los botones
        login_anim = self.createButtonAnimation(self.btn_login)
        register_anim = self.createButtonAnimation(self.btn_register)

        # Agrupo las animaciones de los botones para que se ejecuten en paralelo
        button_group = QParallelAnimationGroup()
        button_group.addAnimation(login_anim)
        button_group.addAnimation(register_anim)

        # Crea una secuencia de animación principal
        main_sequence = QSequentialAnimationGroup()
        main_sequence.addPause(2000)  # pausa antes de iniciar las animaciones de los botones
        main_sequence.addAnimation(button_group)

        main_sequence.start()


    # Creo una animación de desplazamiento para el botón
    def createButtonAnimation(self, button):
        anim = QPropertyAnimation(button, b"pos")
        anim.setDuration(1000)
        start_pos = button.pos() + QPoint(0, 50)
        anim.setStartValue(start_pos)
        anim.setEndValue(button.pos())
        anim.setEasingCurve(QEasingCurve.OutElastic)
        return anim


    # Aplico el efecto de sombra al widget
    def applyShadow(self, widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)


    # Efecto de 'fundido' de entrada en el widget
    def fadeInWidget(self, widget, duration=2000, easing=QEasingCurve.InOutQuad):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(easing)
        animation.start()
        self.animations.append(animation)


    # Lleva a la pantalla de Inicio de Sesión
    def onLogin(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


    # Lleva a la pantalla de Registro
    def onRegister(self):
        from register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


    # 'Pinto' el fondo de la pantalla con un degradado de negro a naranja
    def paintEvent(self, event):
        """Pinta el fondo con un degradado."""
        painter = QPainter(self)
        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0.0, QColor(0, 0, 0))
        gradient.setColorAt(1.0, QColor(255, 140, 0))
        painter.fillRect(rect, QBrush(gradient))
        super().paintEvent(event)


    # Animación de fundido de entrada al mostrar la pantalla
    def showEvent(self, event):
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
    # Estilo de la aplicación
    app.setStyleSheet("""
        QWidget {
            background-color: #333;
            color: white;
            font-family: Arial, Helvetica, sans-serif;
        }
                      
        QPushButton {
            background-color: #555;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
        }
                      
        QPushButton:hover { background-color: #777; }
                      
        QLabel { color: #eee; }
    """)

    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())