import requests

from io import BytesIO

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QScrollArea
from PyQt5.QtGui import QPixmap, QPainter, QBitmap

# Importación de los estilos 
from styles.styled_button import StyledButton
from styles.styled_line_edit import StyledLineEdit
from styles.password_field import PasswordField

# URL de la api para la conexión con la api rest
API_BASE_URL = "http://localhost:5000"


# Clase principal de la vista Mi Perfil
class MyProfileView(QWidget):
    profile_pic_updated = pyqtSignal(str)

    def __init__(self, user_id, parent=None):
        super().__init__(parent)
        self.user_id = user_id

        import json
        # Cargar tema desde settings.json
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except:
            self.current_theme = "light"

        self.initUI()

    # Creación de la interfaz
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
        if self.current_theme == "dark":
            border_color = "#FF5500"  # Naranja oscuro (modo dark)
        else:
            border_color = "#FFA500"  # Naranja claro (modo light)

        self.profile_pic.setStyleSheet(f"""
            border-radius: 100px;
            background: transparent;
            border: 3px solid {border_color};
        """)

        self.profile_pic.setScaledContents(True)
        layout.addWidget(self.profile_pic, alignment=Qt.AlignCenter)

        # Cambiar la foto de perfil
        self.btn_change_pic = StyledButton("Cambiar Foto", "images/galeria.png", theme=self.current_theme)
        self.btn_change_pic.clicked.connect(self.change_profile_picture)
        layout.addWidget(self.btn_change_pic, alignment=Qt.AlignCenter)

        # Nombre de usuario
        self.name_input = StyledLineEdit("Nombre", "images/nombre_usuario.png", theme=self.current_theme)
        layout.addWidget(self.name_input)

        # Correo de registro
        self.email_input = StyledLineEdit("Correo", "images/email.png", theme=self.current_theme)
        self.email_input.setReadOnly(True)
        layout.addWidget(self.email_input)

        # Botón de editar que habiliata la edición del Nombre de usuario
        self.btn_edit_name = StyledButton("Editar Nombre", "images/edit.png", theme=self.current_theme)
        self.btn_edit_name.clicked.connect(self.enable_name_edit)
        layout.addWidget(self.btn_edit_name)

        password_label = QLabel("Cambiar Contraseña")
        password_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; background: transparent;")
        layout.addWidget(password_label)

        # Campo de la contraseña actual
        self.old_password = PasswordField("Contraseña Actual", "images/password.png", theme=self.current_theme)
        layout.addLayout(self.old_password)

        # Campo de la nueva contraseña
        self.new_password = PasswordField("Nueva Contraseña", "images/password.png", theme=self.current_theme)
        layout.addLayout(self.new_password)

        # Campo de confirmar la contraseña
        self.confirm_password = PasswordField("Confirmar Contraseña", "images/confirmar_password.png", theme=self.current_theme)
        layout.addLayout(self.confirm_password)

        # Botón de guardar los cambios
        self.btn_save_changes = StyledButton("Guardar Cambios", "images/guardar.png", theme=self.current_theme)
        self.btn_save_changes.clicked.connect(self.save_changes)
        layout.addWidget(self.btn_save_changes)

        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        self.load_user_data()


    # Darle formato circular a la foto de perfil
    def set_profile_picture(self, pixmap):
        mask = QBitmap(pixmap.size())
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, pixmap.width(), pixmap.height())
        painter.end()
        pixmap.setMask(mask)
        self.profile_pic.setPixmap(pixmap)


    # Crgar los datos del usuario desde la api rest
    def load_user_data(self):
        response = requests.get(f"{API_BASE_URL}/get-user/{self.user_id}")
        
        if response.status_code == 200:
            
            user_data = response.json()
            self.name_input.setText(user_data.get("username", ""))
            self.email_input.setText(user_data.get("email", ""))

            profile_pic_url = user_data.get("profile_picture", "")
            pixmap = QPixmap()

            if profile_pic_url.startswith("http"):
                try:
                    img_data = requests.get(profile_pic_url).content
                    pixmap.loadFromData(BytesIO(img_data).read())
                except Exception as e:
                    print(f"Error al cargar la imagen de perfil desde la URL: {e}")
                    pixmap.load("images/b_usuario.png") # imagen por defecto

            else:
                pixmap.load("images/b_usuario.png") # iamgen por defecto

            self.set_profile_picture(pixmap)


    # Se habiliata la edición del nombre (correo no)
    def enable_name_edit(self):
        self.name_input.setReadOnly(False)
        self.name_input.setFocus()
    

    # Mostrar los mensajes en un cuadro de diálogo personalizado
    def show_message_box(self, title, message, icon_type="info"):
        msg_box = QMessageBox(self)
        
        # Estilo del cuadro de diálogo
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: black;
                border: 2px solid #FFA500;
                border-radius: 12px;
                font-size: 16px;
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


    # Guardar los cambios del cambio de contraseña y/o nombre conectando con la api
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


    # Permito al usuairo seleccionar una nueva foto de perdil y enviarla a la API
    def change_profile_picture(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")

        if file_path:
            try:
                # Verificar si el archivo se puede cargar
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    self.show_message_box("Error", "La imagen seleccionada no es válida (png, jpg o jpeg).", "error")
                    return

                # Envio la imagen al servidor
                with open(file_path, "rb") as file:
                    files = {"file": file}
                    data = {"user_id": self.user_id}
                    response = requests.post(f"{API_BASE_URL}/upload-profile-picture", files=files, data=data)

                if response.status_code == 200:
                    # Escalo la imagen y actse actualiza en tiempo real
                    pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.set_profile_picture(pixmap)

                    # Señal para actualizar el icono del menú lateral
                    self.profile_pic_updated.emit(file_path)

                    self.show_message_box("Éxito", "Foto de perfil actualizada correctamente.", "info")
                else:
                    self.show_message_box("Error", "No se pudo subir la foto de perfil.", "error")

            except requests.exceptions.ConnectionError:
                self.show_message_box("Error", "Error de conexión. Verifica tu conexión a internet.", "error")

            except Exception as e:
                self.show_message_box("Error", f"Ocurrió un error al subir la foto: {str(e)}", "error")