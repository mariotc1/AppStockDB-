import sys
import math
import requests
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QPainter, QPixmap, QTransform, QLinearGradient, QBrush, QColor, QFont, QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QToolButton,
    QGraphicsOpacityEffect, QLineEdit, QProgressBar, QGraphicsDropShadowEffect, QMessageBox
)

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Inicializo la lista de animaciones
        self.animations = []
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        # Cargo y escalo el logo
        self.logo = QPixmap("images/logoDB_Blanco.png")
        self.logo = self.logo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Rotación del logo 
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Botones de Refrescar y Cerrar (estilo mejorado)
        top_buttons_layout = QHBoxLayout()
        refresh_button = QPushButton(QIcon("images/refrescar.png"), "")
        close_button = QPushButton(QIcon("images/cerrar.png"), "")
        refresh_button.setFixedSize(40, 40)
        close_button.setFixedSize(40, 40)
        refresh_button.clicked.connect(self.refreshApp)
        close_button.clicked.connect(self.close)
        btn_top_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 50);
                border: none;
                border-radius: 20px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """
        refresh_button.setStyleSheet(btn_top_style)
        close_button.setStyleSheet(btn_top_style)
        top_buttons_layout.addStretch()
        top_buttons_layout.addWidget(refresh_button)
        top_buttons_layout.addWidget(close_button)
        self.applyShadow(refresh_button)
        self.applyShadow(close_button)
        main_layout.addLayout(top_buttons_layout)
        main_layout.addSpacing(50)

        # Contenedor para el logo giratorio
        logo_container = QWidget()
        logo_container.setFixedSize(300, 300)
        main_layout.addWidget(logo_container, alignment=Qt.AlignCenter)
        self.logo_container = logo_container  # para usar en paintEvent

        # Título
        title_label = QLabel("Regístrate")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Campos de entrada (se mantienen igual que en el código original)
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(15)

        self.name_field = self.createInputField("Nombre", "images/icon_name.png", is_password=False)
        fields_layout.addLayout(self.name_field)

        self.email_field = self.createInputField("Correo", "images/icon_email.png", is_password=False)
        fields_layout.addLayout(self.email_field)

        self.password_field = self.createInputField("Contraseña", "images/icon_password.png", is_password=True)
        fields_layout.addLayout(self.password_field)

        self.confirm_password_field = self.createInputField("Confirmar Contraseña", "images/icon_password.png", is_password=True)
        fields_layout.addLayout(self.confirm_password_field)

        # Barra de fuerza de contraseña
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(10)
        # Estilo inicial (se actualizará según la fuerza)
        self.strength_bar.setStyleSheet("""
            QProgressBar {
                background-color: #555;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #FF0000;
                border-radius: 5px;
            }
        """)
        fields_layout.addWidget(self.strength_bar)

        # Texto informativo sobre la fuerza de la contraseña
        self.strength_label = QLabel("")
        self.strength_label.setFont(QFont("Arial", 12))
        self.strength_label.setStyleSheet("color: white;")
        self.strength_label.setAlignment(Qt.AlignCenter)
        fields_layout.addWidget(self.strength_label)

        main_layout.addLayout(fields_layout)

        # Conecto el cambio de texto del campo contraseña para actualizar la barra y label de fuerza
        password_line_edit = self.password_field.itemAt(1).widget()
        password_line_edit.textChanged.connect(self.updateStrengthBar)

        # Botones de Registrar y Volver
        bottom_buttons_layout = QHBoxLayout()
        self.btn_register = QPushButton("REGISTRAR")
        self.btn_back = QPushButton("VOLVER")
        btn_style = """
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
        self.btn_register.setStyleSheet(btn_style)
        self.btn_back.setStyleSheet(btn_style)
        self.applyShadow(self.btn_register)
        self.applyShadow(self.btn_back)
        bottom_buttons_layout.addWidget(self.btn_register)
        bottom_buttons_layout.addWidget(self.btn_back)
        main_layout.addLayout(bottom_buttons_layout)

        # Enlace "Ya tengo cuenta. Iniciar Sesión" justo debajo de los botones de registrar y volver
        account_layout = QHBoxLayout()
        self.btn_already_account = QToolButton()
        self.btn_already_account.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_already_account.setText("Ya tengo cuenta. Iniciar Sesión")
        self.btn_already_account.setIcon(QIcon("images/login_icon.png"))
        self.btn_already_account.setIconSize(QSize(48, 48))
        self.btn_already_account.setAutoRaise(True)
        self.btn_already_account.clicked.connect(self.openLogin)
        account_layout.addStretch()
        account_layout.addWidget(self.btn_already_account)
        account_layout.addStretch()
        self.fadeInWidget(self.btn_already_account, 2500, QEasingCurve.OutCubic)
        main_layout.addLayout(account_layout)

        # Agrego un stretch para empujar el footer hacia abajo
        main_layout.addStretch()

        # Footer abajo
        footer_label = QLabel("© 2025 DB Inmuebles. Todos los derechos reservados.")
        footer_label.setStyleSheet("color: white; font-size: 18px;")
        footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer_label)

        # Animaciones de aparición
        self.fadeInWidget(title_label, 1500, QEasingCurve.OutCubic)
        self.fadeInWidget(self.btn_register, 2000, QEasingCurve.OutCubic)
        self.fadeInWidget(self.btn_back, 2000, QEasingCurve.OutCubic)

        # Conexión de botones
        self.btn_register.clicked.connect(self.register)
        self.btn_back.clicked.connect(self.goBack)

        self.setLayout(main_layout)

    def createInputField(self, placeholder, icon_path, is_password):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_path)
        icon_pixmap = icon_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        layout.addWidget(icon_label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #FFA500;
                border-radius: 10px;
                color: #333;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #FF8C00;
            }
        """)
        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
            eye_button = QPushButton()
            eye_button.setIcon(QIcon("images/icon_eye_off.png"))
            eye_button.setFixedSize(24, 24)
            eye_button.setStyleSheet("border: none;")
            eye_button.setCheckable(True)
            eye_button.toggled.connect(lambda checked, le=line_edit, btn=eye_button: self.togglePasswordVisibility(checked, le, btn))
            layout.addWidget(line_edit)
            layout.addWidget(eye_button)
        else:
            layout.addWidget(line_edit)
        return layout

    def togglePasswordVisibility(self, checked, line_edit, button):
        if checked:
            line_edit.setEchoMode(QLineEdit.Normal)
            button.setIcon(QIcon("images/icon_eye.png"))
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            button.setIcon(QIcon("images/icon_eye_off.png"))

    def updateStrengthBar(self, text):
        strength = self.calculatePasswordStrength(text)
        self.strength_bar.setValue(strength)
        # Actualiza color y texto según la fuerza
        if strength < 40:
            color = "#FF0000"  # rojo para débil
            mensaje = "Contraseña débil"
        elif strength < 70:
            color = "#FFA500"  # naranja para moderada
            mensaje = "Contraseña moderada"
        else:
            color = "#00FF00"  # verde para fuerte
            mensaje = "Contraseña fuerte"
        self.strength_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #555;
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
        """)
        self.strength_label.setText(mensaje)

    def calculatePasswordStrength(self, password):
        strength = 0
        if len(password) >= 8:
            strength += 40
        else:
            strength += len(password) * 5
        if any(c.isdigit() for c in password):
            strength += 20
        if any(c.isupper() for c in password):
            strength += 20
        if any(c in "!@#$%^&*()_+-=[]{};':\",.<>/?\\" for c in password):
            strength += 20
        return min(strength, 100)

    def is_valid_email(self, email):
        """Validar si el correo tiene un formato correcto."""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email)

    def send_welcome_email(self, recipient_email):
        """Envía un correo de bienvenida tras el registro con imagen y datos de contacto."""
        sender_email = "gestionstock@gmail.com"
        subject = "¡Bienvenido a Gestión de Stock!"
        body = """
        <html>
            <body>
                <h2>¡Hola!</h2>
                <p>Gracias por registrarte en el programa de Gestión de Stock.</p>
                <p>Estamos encantados de tenerte con nosotros.</p>
                <p>Si necesitas ayuda, no dudes en escribirnos a <a href='mailto:gestionstock@gmail.com'>gestionSçstock@gmail.com</a> o <a href='mailto:mariotomecore@gmail.com'>mariotomecore@gmail.com</a>.</p>
                <br>
                <img src='cid:thanks_image' width='400'/>
                <p>Saludos,<br>El equipo de Gestión de Stock.</p>
            </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with open("images/thanks.png", "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<thanks_image>')
                msg.attach(img)
        except Exception as e:
            print(f"No se pudo adjuntar la imagen: {e}")

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, "TU_CONTRASEÑA_AQUÍ")  # Configura tu contraseña correctamente
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print("Correo de bienvenida enviado con éxito.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

    def register(self):
        """Manejo del registro con validación de email y envío de correo."""
        name = self.name_field.itemAt(1).widget().text().strip()
        email = self.email_field.itemAt(1).widget().text().strip()
        password = self.password_field.itemAt(1).widget().text()
        confirm_password = self.confirm_password_field.itemAt(1).widget().text()

        if not (name and email and password and confirm_password):
            self.showDialog("Error en el Registro", "Todos los campos deben estar completos.", QMessageBox.Critical)
            return
        
        if not self.is_valid_email(email):
            self.showDialog("Error en el Registro", "El correo electrónico no es válido.", QMessageBox.Critical)
            return
        
        if password != confirm_password:
            self.showDialog("Error en el Registro", "Las contraseñas no coinciden.", QMessageBox.Critical)
            return
        
        url = "http://127.0.0.1:5000/register"
        data = {
            "username": name,
            "email": email,
            "password": password
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                response_data = response.json()
                user_id = response_data.get("user_id", "")  # ✅ Captura el 'user_id'
                
                if not user_id:
                    self.showDialog("Error", "No se recibió el ID del usuario en la respuesta.", QMessageBox.Critical)
                    return

                self.showDialog("Registro Exitoso", "Usuario registrado exitosamente.", QMessageBox.Information)
                self.send_welcome_email(email)  # Enviar correo de bienvenida
                
                from main_window import MainWindow
                self.main_window = MainWindow(user_id)  # ✅ Ahora se pasa el 'user_id' correctamente
                self.main_window.show()
                self.close()

            else:
                error_message = response.json().get("error", "Error desconocido.")
                self.showDialog("Error en el Registro", error_message, QMessageBox.Critical)
        except Exception as e:
            self.showDialog("Error de Conexión", str(e), QMessageBox.Critical)

    def showDialog(self, title, message, icon=QMessageBox.Information):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        logo = QPixmap("images/logoDB_Negro.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        msg_box.setIconPixmap(logo)
        msg_box.exec_()

    def goBack(self):
        print("Volviendo a la pantalla de bienvenida...")
        from welcome_window import WelcomeWindow
        self.close()
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()

    def openLogin(self):
        from login_window import LoginWindow
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()

    def refreshApp(self):
        print("Refrescando la aplicación...")
        self.logo = QPixmap("images/logoDB_Blanco.png")
        self.logo = self.logo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.update()

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

    def applyShadow(self, widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)

    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        # Fondo degradado: de negro a naranja
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0.0, QColor(0, 0, 0))
        gradient.setColorAt(1.0, QColor(255, 140, 0))
        painter.fillRect(rect, QBrush(gradient))
        # Logo giratorio dentro del área del logo_container
        if hasattr(self, 'logo_container'):
            geo = self.logo_container.geometry()
            center_x = geo.center().x()
            center_y = geo.center().y()
        else:
            center_x = rect.width() // 2
            center_y = rect.height() // 3
        angle_radians = math.radians(self.angle)
        scale_x = abs(math.cos(angle_radians))
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(scale_x, 1.0)
        transform.translate(-self.logo.width() // 2, -self.logo.height() // 2)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.logo)
        painter.resetTransform()

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
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())