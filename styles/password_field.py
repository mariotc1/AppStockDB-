import json
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLineEdit, QHBoxLayout

# Clase para darle estilo a los campos de la contraseña de mi Perfil
class PasswordField(QHBoxLayout):
    def __init__(self, placeholder, icon=None, theme=None):
        super().__init__()

        # Cargar tema si no se pasa
        if theme is None:
            try:
                with open("config/settings.json", "r") as f:
                    config = json.load(f)
                    theme = config.get("theme", "light")
            except:
                theme = "light"

        # Colores según el tema
        if theme == "dark":
            border_color = "#FF5500"
            focus_color = "#FF7700"
            bg_color = "#222222"
            text_color = "white"
        else:
            border_color = "#FFA500"
            focus_color = "#FF8C00"
            bg_color = "#FFFFFF"
            text_color = "#000000"

        # Campo de texto
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setEchoMode(QLineEdit.Password)
        self.line_edit.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px 12px 12px 40px;
                border: 2px solid {border_color};
                border-radius: 15px;
                background-color: {bg_color};
                color: {text_color};
                font-size: 16px;
            }}
            QLineEdit:focus {{
                border-color: {focus_color};
            }}
            QLineEdit::placeholder {{
                color: #888888;
            }}
        """)
        self.addWidget(self.line_edit)

        # Botón del ojo
        self.eye_button = QPushButton()
        
        self.eye_button.setIcon(QIcon("images/b_icon_eye_off.png"))
        self.eye_button.setIconSize(QSize(24, 24))
        self.eye_button.setCheckable(True)
        self.eye_button.setStyleSheet("border: none;")
        
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        self.addWidget(self.eye_button)


    # Método para alternar la visibilidad de la contraseña
    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.line_edit.setEchoMode(QLineEdit.Normal)
            self.eye_button.setIcon(QIcon("images/b_icon_eye.png"))
        else:
            self.line_edit.setEchoMode(QLineEdit.Password)
            self.eye_button.setIcon(QIcon("images/b_icon_eye_off.png"))

    # Método para obtener el texto del campo
    def text(self):
        return self.line_edit.text()