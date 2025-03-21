import requests
from io import BytesIO
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QHBoxLayout, 
    QFileDialog, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QPixmap, QIcon, QFont, QPainter, QColor, QLinearGradient, QRegion, QBitmap
from PyQt5.QtCore import Qt, QSize, pyqtSignal

API_BASE_URL = "http://localhost:5000"

class GradientWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 200))
        gradient.setColorAt(1, QColor(255, 165, 0, 200))
        painter.fillRect(self.rect(), gradient)

class StyledButton(QPushButton):
    def __init__(self, text, icon=None):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                border: 2px solid white;
                color: white;
                padding: 12px 24px;
                text-align: center;
                font-size: 18px;
                margin: 4px 2px;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
                border: 2px solid #FF8C00;
            }
        """)
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(24, 24))

class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder, icon):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                padding: 12px 12px 12px 40px;
                border: 2px solid #FFA500;
                border-radius: 15px;
                background: transparent;
                color: white;
            }
            QLineEdit:focus {
                border-color: #FF8C00;
            }
        """)
        self.setTextMargins(40, 0, 0, 0)
        
        icon_label = QLabel(self)
        icon_label.setPixmap(QIcon(icon).pixmap(QSize(24, 24)))
        icon_label.setStyleSheet("background: transparent;")
        icon_label.move(10, 8)
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
            }
            QLineEdit:focus {
                border-color: #FF8C00;
            }
        """)
        self.addWidget(self.line_edit)

        self.eye_button = QPushButton()
        self.eye_button.setIcon(QIcon("images/ojo_cerrado.png"))
        self.eye_button.setIconSize(QSize(24, 24))
        self.eye_button.setCheckable(True)
        self.eye_button.setStyleSheet("background: transparent; border: none;")
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        self.addWidget(self.eye_button)

    def toggle_password_visibility(self):
        if self.eye_button.isChecked():
            self.line_edit.setEchoMode(QLineEdit.Normal)
            self.eye_button.setIcon(QIcon("images/ojo_abierto.png"))
        else:
            self.line_edit.setEchoMode(QLineEdit.Password)
            self.eye_button.setIcon(QIcon("images/ojo_cerrado.png"))

    def text(self):
        return self.line_edit.text()

class MiPerfilView(QWidget):
    profile_pic_updated = pyqtSignal(str)

    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        self.setStyleSheet("background: transparent;")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background: transparent; border: none;")

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        scroll_area.setWidget(content_widget)

        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title_label = QLabel("Mi Perfil")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; font-size: 36px; font-weight: bold; background: transparent;")
        layout.addWidget(title_label)

        self.profile_pic = QLabel(self)
        self.profile_pic.setFixedSize(200, 200)
        self.profile_pic.setStyleSheet("border-radius: 100px; background: transparent; border: 3px solid #FFA500;")
        self.profile_pic.setScaledContents(True)
        layout.addWidget(self.profile_pic, alignment=Qt.AlignCenter)

        self.btn_change_pic = StyledButton("Cambiar Foto", "images/galeria.png")
        self.btn_change_pic.clicked.connect(self.change_profile_picture)
        layout.addWidget(self.btn_change_pic, alignment=Qt.AlignCenter)

        self.name_input = StyledLineEdit("Nombre", "images/nombre_usuario.png")
        layout.addWidget(self.name_input)

        self.email_input = StyledLineEdit("Correo", "images/email.png")
        self.email_input.setReadOnly(True)
        layout.addWidget(self.email_input)

        self.btn_edit_name = StyledButton("Editar Nombre", "images/edit.png")
        self.btn_edit_name.clicked.connect(self.enable_name_edit)
        layout.addWidget(self.btn_edit_name)

        password_label = QLabel("Cambiar Contraseña")
        password_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: transparent;")
        layout.addWidget(password_label)

        self.old_password = PasswordField("Contraseña Actual", "images/password.png")
        layout.addLayout(self.old_password)

        self.new_password = PasswordField("Nueva Contraseña", "images/password.png")
        layout.addLayout(self.new_password)

        self.confirm_password = PasswordField("Confirmar Contraseña", "images/confirmar_password.png")
        layout.addLayout(self.confirm_password)

        self.btn_save_changes = StyledButton("Guardar Cambios", "images/guardar.png")
        self.btn_save_changes.clicked.connect(self.save_changes)
        layout.addWidget(self.btn_save_changes)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        self.load_user_data()

    def set_profile_picture(self, pixmap):
        mask = QBitmap(pixmap.size())
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, pixmap.width(), pixmap.height())
        painter.end()
        pixmap.setMask(mask)
        self.profile_pic.setPixmap(pixmap)

    def load_user_data(self):
        response = requests.get(f"{API_BASE_URL}/get-user/{self.user_id}")
        if response.status_code == 200:
            user_data = response.json()
            self.name_input.setText(user_data.get("username", ""))
            self.email_input.setText(user_data.get("email", ""))

            profile_pic_url = user_data.get("profile_picture", "")
            if profile_pic_url:
                try:
                    img_data = requests.get(profile_pic_url).content
                    pixmap = QPixmap()
                    pixmap.loadFromData(BytesIO(img_data).read())
                    self.set_profile_picture(pixmap)

                    # 🔥 Emitir la señal para que la imagen se actualice en el menú lateral
                    self.profile_pic_updated.emit(profile_pic_url)

                except Exception as e:
                    print(f"Error al cargar la imagen de perfil: {e}")
            else:
                self.set_profile_picture(QPixmap("images/usuario.png"))

    def enable_name_edit(self):
        """Habilita la edición del nombre"""
        self.name_input.setReadOnly(False)
        self.name_input.setFocus()
    
    def show_message_box(self, title, message, icon_type="info"):
        msg_box = QMessageBox(self)
        
        # Estilo del cuadro de diálogo
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: black;
                border: 2px solid #FFA500;
                border-radius: 12px;
                font-size: 14px;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #FFA500;
                border: none;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)

        # Icono del mensaje
        if icon_type == "info":
            msg_box.setIcon(QMessageBox.Information)
        elif icon_type == "error":
            msg_box.setIcon(QMessageBox.Critical)

        # Título e información
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # Agregar logo personalizado
        logo = QLabel()
        logo.setPixmap(QPixmap("images/logoDB_Negro.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        msg_box.setIconPixmap(logo.pixmap())

        msg_box.exec_()

    def save_changes(self):
        new_name = self.name_input.text()
        old_pass = self.old_password.text()
        new_pass = self.new_password.text()
        confirm_pass = self.confirm_password.text()
        
        data = {
            "user_id": self.user_id,
            "username": new_name,
            "current_password": old_pass,
            "new_password": new_pass,
            "confirm_password": confirm_pass
        }
        
        response = requests.post(f"{API_BASE_URL}/update-profile", json=data)
        if response.status_code == 200:
            self.show_message_box("Éxito", "Perfil actualizado correctamente.", "info")
        else:
            self.show_message_box("Error", "No se pudieron guardar los cambios.", "error")

    def change_profile_picture(self):
        """Permite al usuario seleccionar una nueva foto de perfil y enviarla a la API"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")

        if file_path:
            try:
                # Verificar si el archivo se puede cargar correctamente como imagen
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    self.show_message_box("Error", "La imagen seleccionada no es válida.", "error")
                    return  # 🚨 Sale del método si la imagen está dañada

                # Enviar la imagen al servidor
                with open(file_path, "rb") as file:
                    files = {"file": file}
                    data = {"user_id": self.user_id}
                    response = requests.post(f"{API_BASE_URL}/upload-profile-picture", files=files, data=data)

                if response.status_code == 200:
                    # Escalar la imagen y actualizar en tiempo real
                    pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.set_profile_picture(pixmap)

                    # 🔥 Emitir la señal para actualizar el icono del menú lateral
                    self.profile_pic_updated.emit(file_path)

                    self.show_message_box("Éxito", "Foto de perfil actualizada correctamente.", "info")
                else:
                    self.show_message_box("Error", "No se pudo subir la foto de perfil.", "error")

            except requests.exceptions.ConnectionError:
                self.show_message_box("Error", "Error de conexión. Verifica tu conexión a internet.", "error")

            except Exception as e:
                self.show_message_box("Error", f"Ocurrió un error al subir la foto: {str(e)}", "error")