"""
welcome_window.py

Módulo que define la ventana de bienvenida de la aplicación de gestión de stock.

Contiene la clase `WelcomeWindow`, una interfaz moderna con estilo profesional, efectos visuales
como degradados, sombras, animaciones y efectos de entrada. Esta pantalla permite al usuario
acceder a las opciones de inicio de sesión y registro, además de permitir el cambio de tema
(oscuro o claro) con persistencia entre sesiones.

Componentes destacados:
- Logo rotativo central.
- Mensaje de bienvenida y subtítulo.
- Botones estilizados para navegar a Login o Registro.
- Selector de tema (modo claro/oscuro) persistente.
- Animaciones suaves y efectos visuales (sombra, fundido, entrada elástica).
- Efecto de máquina de escribir en el tagline.

Este módulo se ejecuta también como script independiente para pruebas directas de la ventana.

Requiere:
    - PyQt5
    - Archivos de configuración en `config/settings.json`
    - Imagen del logo en `images/logoDB_Blanco.png`
    - Componentes de animación y estilo personalizados
"""

import sys, json

from PyQt5.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QPoint, 
    QSequentialAnimationGroup, QParallelAnimationGroup
)

from PyQt5.QtGui import ( 
    QPainter, QLinearGradient, 
    QBrush, QColor, QFont, QIcon
)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QPushButton, QGraphicsOpacityEffect, QGraphicsDropShadowEffect
)

from animations.rotating_logo import RotatingLogoWidget
from animations.typewriter_label import TypewriterLabel

from styles.styled_button import StyledButton

# Ruta de la imagen del logo
LOGO_PATH = "images/logoDB_Blanco.png"

# Pantalla de Bienvenida 
class WelcomeWindow(QWidget):

    """
    Inicializa la ventana de bienvenida y carga la configuración del tema actual.
    """
    def __init__(self):
        super().__init__()
        
        self.animations = []
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.setWindowTitle("AppStockDB")
        self.setWindowIcon(QIcon("images/logoDB_Blanco.png"))

        # Veo si la app está en modo claro/oscuro desde el archivo de configuración
        import json
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_theme = "light"

        self.showMaximized()
        self.initUI()

    """
    Construye toda la interfaz gráfica, aplica estilos, configura botones y animaciones.
    """
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Logo con el efecto de giro 360º
        self.rotating_logo = RotatingLogoWidget(LOGO_PATH)
        main_layout.addWidget(self.rotating_logo, alignment=Qt.AlignCenter)

        # Card contenedor
        card = QFrame()
        card.setMinimumWidth(800)
        card.setMaximumWidth(800)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setSpacing(30)

        # Logo giratorio 
        card_layout.addWidget(self.rotating_logo, alignment=Qt.AlignCenter)

        # Títulos 
        self.title_label = QLabel("¡Bienvenido a DB Inmuebles!")
        self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.title_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("Sistema de Gestión de Stock")
        self.subtitle_label.setFont(QFont("Arial", 18))
        self.subtitle_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.subtitle_label)

        # Botones 
        button_layout = QHBoxLayout()
        self.btn_login = StyledButton("Iniciar Sesión", theme=self.current_theme)
        self.btn_register = StyledButton("Registrarse", theme=self.current_theme)

        self.applyShadow(self.btn_login)
        self.applyShadow(self.btn_register)

        button_layout.addWidget(self.btn_login)
        button_layout.addWidget(self.btn_register)

        card_layout.addSpacing(20)
        card_layout.addLayout(button_layout)

        # Tagline con efecto de máquina de escribir
        self.tagline_label = TypewriterLabel("Tecnología y excelencia en cada detalle")
        self.tagline_label.setFont(QFont("Courier", 14, QFont.StyleItalic))
        self.tagline_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.tagline_label.setAlignment(Qt.AlignCenter)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.tagline_label)

        main_layout.addStretch()
        main_layout.addWidget(card, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        from themes.theme_manager import ThemeManager
        self.theme_button = QPushButton()
        self.theme_button.setFixedSize(40, 40)
        self.updateThemeIcon()  # Icono inicial correcto
        self.theme_button.setStyleSheet("border: none;")
        self.theme_button.clicked.connect(self.toggleTheme)

        # Layout flotante arriba a la derecha
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        top_layout.addWidget(self.theme_button)

        main_layout.insertLayout(0, top_layout)  # Insertarlo en la parte superior

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


    """
    Alterna entre modo claro y oscuro, guarda el estado y reinicia la ventana para aplicar cambios.
    """
    def toggleTheme(self):
        from themes.theme_manager import ThemeManager
        app = QApplication.instance()
        ThemeManager.toggle_theme(app)
        self.updateThemeIcon()

        # Actualizo el tema actual leído del archivo
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_theme = "light"

        self.updateThemeIcon()
        self.reopen()


    """
    Actualiza el icono del botón de cambio de tema según el modo actual (claro u oscuro).
    """
    def updateThemeIcon(self):
        try:
            with open("config/settings.json", "r") as f:
                theme = json.load(f).get("theme", "light")
        except FileNotFoundError:
            theme = "light"
        
        icon_path = "images/claro.png" if theme == "light" else "images/oscuro.png"
        self.theme_button.setIcon(QIcon(icon_path))
        self.theme_button.setIconSize(self.theme_button.size())


    """
    Cierra y vuelve a abrir la ventana de bienvenida para aplicar el nuevo tema visual.
    """
    def reopen(self):
        self.new_window = WelcomeWindow()
        self.new_window.show()
        self.close()

    """
    Configura las animaciones de entrada para títulos y botones de la interfaz.
    """
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


    """
    Crea una animación de entrada para un botón, haciéndolo deslizar desde abajo.

    Args:
        button (QPushButton): Botón al que se le aplicará la animación.

    Returns:
        QPropertyAnimation: Objeto de animación configurado.
    """
    def createButtonAnimation(self, button):
        anim = QPropertyAnimation(button, b"pos")
        anim.setDuration(1000)
        start_pos = button.pos() + QPoint(0, 50)
        anim.setStartValue(start_pos)
        anim.setEndValue(button.pos())
        anim.setEasingCurve(QEasingCurve.OutElastic)
        return anim


    """
    Aplica un efecto de sombra estilizado a un widget dado.

    Args:
        widget (QWidget): Elemento visual al que se aplicará la sombra.
    """
    def applyShadow(self, widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)


    """
    Aplica una animación de entrada en forma de fundido al widget indicado.

    Args:
        widget (QWidget): Widget al que se le aplicará el efecto.
        duration (int): Duración del efecto en milisegundos.
        easing (QEasingCurve): Curva de suavizado de la animación.
    """
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


    """
    Muestra la ventana de inicio de sesión y cierra la actual.
    """
    def onLogin(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


    """
    Muestra la ventana de registro de usuario y cierra la actual.
    """
    def onRegister(self):
        from register_window import RegisterWindow
        self.register_window = RegisterWindow()
        self.register_window.show()
        self.close()


    """
    Dibuja el fondo con un degradado vertical dependiendo del tema actual.
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())

        if self.current_theme == "dark":
            # Fondo oscuro
            gradient.setColorAt(0.0, QColor(10, 10, 10))
            gradient.setColorAt(1.0, QColor(30, 30, 30))
        else:
            # Fondo claro
            gradient.setColorAt(0.0, QColor(0, 0, 0))
            gradient.setColorAt(1.0, QColor(255, 140, 0))

        painter.fillRect(rect, QBrush(gradient))
        super().paintEvent(event)


    """
    Aplica una animación de entrada con fundido al mostrar la ventana.
    """
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