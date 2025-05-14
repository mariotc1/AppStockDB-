"""
Vista de configuración general de la aplicación.

Permite al usuario cambiar entre tema claro y oscuro, contactar con soporte técnico
(vía WhatsApp o correo), y cerrar sesión. Incluye controles estilizados y una interfaz
moderna y centrada, con un diseño responsive y coherente con el tema activo.

:param parent: Widget padre opcional.
"""

import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QMessageBox

# Estilos de los botones y del switch
from styles.styled_button import StyledButton
from styles.animated_styled_switch import AnimatedStyledSwitch

class SettingsView(QWidget):

    """
    Inicializa la vista de ajustes cargando el tema actual y construyendo la interfaz visual.

    :param parent: Widget padre opcional.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # Compruebo si está en modo ligth/dark desde settings.json
        import json
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_theme = "light"

        # Inicializo la vista
        self.initUI()

    
    """
    Construye la interfaz gráfica de la vista, incluyendo:
    - Título principal
    - Cambio de tema (claro/oscuro)
    - Opciones de contacto con soporte
    - Botón para cerrar sesión
    - Footer informativo
    """
    def initUI(self):
        self.setStyleSheet("background-color: transparent;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 20, 40, 20)
        main_layout.setSpacing(20)

        # Contenedor principal
        container = QFrame()
        container.setMaximumWidth(1000)
        container.setMinimumHeight(500)
        container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(50, 50, 50, 50)
        container_layout.setSpacing(35)

        # Título centrarl de la vista
        title = QLabel("Ajustes y Soporte Técnico")
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold; background: transparent; border: none;")
        title.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(title)

        # Texto de modo oscuro + switch para cambiar tema
        theme_block = QHBoxLayout()
        theme_block.setAlignment(Qt.AlignCenter)
        theme_block.setSpacing(15)

        label = QLabel("Modo Oscuro")
        label.setFont(QFont("Segoe UI", 18))
        label.setStyleSheet("color: white; background: transparent; border: none;")
        theme_block.addWidget(label)


        self.theme_toggle = AnimatedStyledSwitch()
        self.theme_toggle.setChecked(self.is_dark_theme())
        self.theme_toggle.stateChanged.connect(self.update_toggle_ui)
        theme_block.addWidget(self.theme_toggle)

        container_layout.addLayout(theme_block)

        # Pregunta de soporte técnico + botones de contacto
        support_text = QLabel("¿Tienes dudas o problemas? Contáctanos por nuestras vías oficiales")
        support_text.setFont(QFont("Segoe UI", 15))
        support_text.setStyleSheet("color: white; background: transparent; border: none;")
        support_text.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(support_text)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(25)
        buttons_layout.setAlignment(Qt.AlignCenter)

        btn_whatsapp = StyledButton("WhatsApp", "images/b_whatsapp.png", theme=self.current_theme)
        btn_whatsapp.clicked.connect(self.open_whatsapp)
        buttons_layout.addWidget(btn_whatsapp)

        btn_email = StyledButton("Gmail", "images/b_gmail.png", theme=self.current_theme)
        btn_email.clicked.connect(self.open_email)
        buttons_layout.addWidget(btn_email)

        container_layout.addLayout(buttons_layout)

        # Botón de cerrar sesión  (más adelante le pondré la funcionalidad)
        logout_label = QLabel("¿Deseas cerrar sesión?")
        logout_label.setFont(QFont("Segoe UI", 14))
        logout_label.setStyleSheet("color: white; background: transparent; border: none;")
        logout_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(logout_label)

        logout_button = StyledButton("Cerrar Sesión", "images/b_cerrarSesion.png", theme=self.current_theme)
        logout_button.clicked.connect(self.logout_action)
        container_layout.addWidget(logout_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(container, alignment=Qt.AlignCenter)
        main_layout.addStretch()

        # Footer abajo
        footer = QLabel("© 2025 App Gestión Stock DB Inmuebles | Todos los derechos reservados | Versión 1.0")
        footer.setFont(QFont("Segoe UI", 12))
        footer.setStyleSheet("color: white; background: transparent; border: none;")
        footer.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer)


    """
    Llama a la función encargada de aplicar el cambio de tema según el estado del switch.

    :param state: Estado del switch (Qt.Checked o Qt.Unchecked).
    """
    def update_toggle_ui(self, state):
        self.toggle_theme(state)

    
    """
    Comprueba si el tema actual guardado en configuración es 'dark'.

    :return: True si el tema actual es oscuro, False en caso contrario.
    """
    def is_dark_theme(self):
        import json
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
            return config.get("theme", "light") == "dark"
        except:
            return False


    """
    Cambia entre el tema claro y oscuro, guarda la preferencia en el archivo de configuración
    y reinicia la aplicación para aplicar los cambios visuales.

    :param state: Estado del switch que indica el nuevo tema a aplicar.
    """
    def toggle_theme(self, state):
        import json, os, sys
        new_theme = "dark" if state == Qt.Checked else "light"
        try:
            with open("config/settings.json", "w") as f:
                json.dump({"theme": new_theme}, f)
            self.showDialog("Tema Cambiado", "Se ha cambiado el tema. La aplicación se reiniciará.", QMessageBox.Information)
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            self.showDialog("Error", f"No se pudo cambiar el tema: {e}", QMessageBox.Critical)


    """
    Abre el navegador predeterminado y redirige al enlace de contacto por WhatsApp.
    """
    def open_whatsapp(self):
        import webbrowser
        webbrowser.open('https://wa.me/34644071074')


    """
    Abre el cliente de correo predeterminado con un nuevo mensaje a la dirección de soporte.
    """
    def open_email(self):
        import webbrowser
        webbrowser.open('mailto:gestionstockdb@gmail.com')


    """
    Elimina el archivo de sesión local, muestra un mensaje de confirmación y redirige al usuario
    a la pantalla de bienvenida.
    """
    def logout_action(self):
        session_path = os.path.join("config", "session.json")
        if os.path.exists(session_path):
            os.remove(session_path)

        QMessageBox.information(self, "Cerrar Sesión", "Sesión cerrada correctamente.")
        
        # Volver a pantalla de bienvenida
        from welcome_window import WelcomeWindow
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()
        self.window().close()  # Cierra la ventana actual

    
    """
    Muestra un cuadro de diálogo personalizado con ícono dinámico dependiendo del tema actual.

    :param title: Título de la ventana del mensaje.
    :param message: Mensaje a mostrar al usuario.
    :param icon: Tipo de icono de mensaje (por defecto: QMessageBox.Information).
    """
    def showDialog(self, title, message, icon=QMessageBox.Information):
        import json
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                current_theme = config.get("theme", "light")
        except (FileNotFoundError, json.JSONDecodeError):
            current_theme = "light"

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)

        # Logo dinámico según tema
        if current_theme == "dark":
            logo = QPixmap("images/logoDB_Blanco.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            logo = QPixmap("images/logoDB_Negro.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        msg_box.setIconPixmap(logo)
        msg_box.exec_()