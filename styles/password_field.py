from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLineEdit, QHBoxLayout

# Clase para darle estilo a los campos de la contraseña
class PasswordField(QHBoxLayout):
    def __init__(self, placeholder, icon):
        super().__init__()
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setEchoMode(QLineEdit.Password)
        self.line_edit.setStyleSheet("""
            QLineEdit {
                padding: 12px 12px 12px 40px;
                border: 2px solid #FFA500;
                border-radius: 15px;
                background: transparent;
                color: white;
                font-size: 16px;
            }
            QLineEdit:focus {
                border-color: #FF8C00;
            }
        """)
        self.addWidget(self.line_edit)

        self.eye_button = QPushButton()
        self.eye_button.setIcon(QIcon("images/icon_eye_off.png"))
        self.eye_button.setIconSize(QSize(24, 24))
        self.eye_button.setCheckable(True)
        self.eye_button.setStyleSheet("background: transparent; border: none;")
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        
        self.addWidget(self.eye_button)

    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.line_edit.setEchoMode(QLineEdit.Normal)
            self.eye_button.setIcon(QIcon("images/icon_eye.png"))
        else:
            self.line_edit.setEchoMode(QLineEdit.Password)
            self.eye_button.setIcon(QIcon("images/icon_eye_off.png"))

    def text(self):
        return self.line_edit.text()