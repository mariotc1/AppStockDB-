import sys, math, requests, re, smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from PyQt5.QtCore import (
     Qt, QTimer, QPropertyAnimation, 
     QEasingCurve, QSize
)

from PyQt5.QtGui import (
    QPainter, QPixmap, QTransform, QLinearGradient, 
    QBrush, QColor, QFont, QIcon
)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QLabel, QPushButton, QToolButton, QGraphicsOpacityEffect, 
    QLineEdit, QProgressBar, QGraphicsDropShadowEffect, QMessageBox
)

# Estilos para los botones
from styles.styled_button import StyledButton

# Clase de Registro
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Inicializo la lista de animaciones
        self.animations = []

        # Cargo y escalo el logo
        self.logo = QPixmap("images/logoDB_Blanco.png")
        self.logo = self.logo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Rotación del logo 
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)

        import json

        # Leer el tema actual
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_theme = "light"


        self.initUI()
        self.setWindowTitle("AppStockDB")
        self.setWindowIcon(QIcon("images/logoDB_Blanco.png"))
        self.showMaximized()


    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Card contenedor
        card = QFrame()
        card.setMinimumWidth(1000)
        card.setMaximumWidth(1000)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(15)

        # Contenedor para el logo giratorio dentro del card
        self.logo_container = QWidget()
        self.logo_container.setFixedSize(300, 300)
        card_layout.insertWidget(0, self.logo_container, alignment=Qt.AlignCenter)

        # Título
        title_label = QLabel("Regístrate")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setStyleSheet("color: white; background: transparent; border: none;")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # Campos
        self.name_field = self.createInputField("Nombre", "images/b_iconName.png", is_password=False)
        self.email_field = self.createInputField("Correo", "images/b_iconMail.png", is_password=False)
        self.password_field = self.createInputField("Contraseña", "images/b_iconPass.png", is_password=True)
        self.confirm_password_field = self.createInputField("Confirmar Contraseña", "images/b_iconPass.png", is_password=True)

        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(15)
        fields_layout.addLayout(self.name_field)
        fields_layout.addLayout(self.email_field)
        fields_layout.addLayout(self.password_field)
        fields_layout.addLayout(self.confirm_password_field)

        card_layout.addLayout(fields_layout)

        # Barra de fuerza de contraseña
        self.strength_bar = QProgressBar()
        self.strength_bar.setRange(0, 100)
        self.strength_bar.setValue(0)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setFixedHeight(10)
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
        card_layout.addWidget(self.strength_bar)

        # Label de fuerza de contraseña
        self.strength_label = QLabel("")
        self.strength_label.setFont(QFont("Arial", 12))
        self.strength_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.strength_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.strength_label)

        # Actualización de la barra de fuerza al cambiar el texto
        password_line_edit = self.password_field.itemAt(1).widget()
        password_line_edit.textChanged.connect(self.updateStrengthBar)

        # Botones de registro y volver
        self.btn_register = StyledButton("Registrar", theme=self.current_theme)
        self.btn_back = StyledButton("Volver", theme=self.current_theme)

        self.applyShadow(self.btn_register)
        self.applyShadow(self.btn_back)

        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.addWidget(self.btn_register)
        bottom_buttons_layout.addWidget(self.btn_back)
        card_layout.addLayout(bottom_buttons_layout)

        # Enlace "ya tengo cuenta"
        self.btn_already_account = QToolButton()
        self.btn_already_account.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_already_account.setText("Ya tengo cuenta. Iniciar Sesión")
        self.btn_already_account.setStyleSheet("color: white; font-weight: bold;")
        self.btn_already_account.setIcon(QIcon("images/b_loginIcon.png"))
        self.btn_already_account.setIconSize(QSize(48, 48))
        self.btn_already_account.setAutoRaise(True)
        self.btn_already_account.clicked.connect(self.openLogin)

        account_layout = QHBoxLayout()
        account_layout.addStretch()
        account_layout.addWidget(self.btn_already_account)
        account_layout.addStretch()

        self.fadeInWidget(self.btn_already_account, 2500, QEasingCurve.OutCubic)
        card_layout.addLayout(account_layout)

        main_layout.addStretch()
        # Añadir el card al layout principal
        main_layout.addWidget(card, alignment=Qt.AlignCenter)

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


    # Creo un campo de entrada con icono y placeholder
    def createInputField(self, placeholder, icon_path, is_password):
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        icon_label = QLabel()
        icon_pixmap = QPixmap(icon_path)
        icon_pixmap = icon_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setStyleSheet("background: transparent; border: none;")
        icon_label.setPixmap(icon_pixmap)
        
        layout.addWidget(icon_label)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
              
        if is_password:
            line_edit.setEchoMode(QLineEdit.Password)
            eye_button = QPushButton()
            eye_button.setIcon(QIcon("images/b_icon_eye_off.png"))
            eye_button.setFixedSize(24, 24)
            eye_button.setStyleSheet("border: none;")
            eye_button.setCheckable(True)
            eye_button.toggled.connect(lambda checked, le=line_edit, btn=eye_button: self.togglePasswordVisibility(checked, le, btn))
            layout.addWidget(line_edit)
            layout.addWidget(eye_button)
        else:
            layout.addWidget(line_edit)
        return layout


    # Cambia la visibilidad de la contraseña al hacer clic en el botón
    def togglePasswordVisibility(self, checked, line_edit, button):
        if checked:
            line_edit.setEchoMode(QLineEdit.Normal)
            button.setIcon(QIcon("images/b_icon_eye.png"))
        else:
            line_edit.setEchoMode(QLineEdit.Password)
            button.setIcon(QIcon("images/b_icon_eye_off.png"))


    # Actualiza la barra de fuerza de contraseña y el texto informativo
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


    # Calculo la fuerza de la contraseña
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


    # Validar si el correo tiene formato correto con una regex
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email)


    # Enviar un correo de bienvenida al usuario tras el registro
    def send_welcome_email(self, recipient_email):
        sender_email = "gestionstockdb@gmail.com"
        subject = "¡Bienvenido a Gestión de Stock!"
        body = """
        <html>
            <body>
                <h2>¡Hola!</h2>
                <p>Gracias por registrarte en el programa de Gestión de Stock.</p>
                <p>Estamos encantados de tenerte con nosotros.</p>
                <p>Si necesitas ayuda, no dudes en escribirnos a <a href='mailto:gestionstockdb@gmail.com'>gestionstockdb@gmail.com</a> o <a href='mailto:mariotomecore@gmail.com'>mariotomecore@gmail.com</a>.</p>
                <br>
                <img src='cid:gracias' width='400'/>
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
            with open("images/gracias.png", "rb") as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-ID', '<thanks_image>')
                msg.attach(img)

        except Exception as e:
            print(f"No se pudo adjuntar la imagen: {e}")

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, "tjjw gvdp tlot rege")  # Contraseña generada para este proeycto
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print("Correo de bienvenida enviado con éxito.")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")


    # Manejo del registro con validación del correo y envío de correo de bienvenida
    def register(self):
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
                user_id = response_data.get("user_id", "")
                
                if not user_id:
                    self.showDialog("Error", "No se recibió el ID del usuario en la respuesta.", QMessageBox.Critical)
                    return

                self.showDialog("Registro Exitoso", "Usuario registrado exitosamente.", QMessageBox.Information)
                self.send_welcome_email(email)  # Enviar correo de bienvenida
                
                # Muestra Loading Screen
                from dialogs.loading_screen import LoadingScreen
                self.loading_screen = LoadingScreen()
                self.loading_screen.show()

                # Carga MainWindow con un pequeño delay para permitir la animación
                QTimer.singleShot(100, lambda: self.openMainWindow(user_id))

            else:
                error_message = response.json().get("error", "Error desconocido.")
                self.showDialog("Error en el Registro", error_message, QMessageBox.Critical)
        except Exception as e:
            self.showDialog("Error de Conexión", str(e), QMessageBox.Critical)


    def openMainWindow(self, user_id):
        from main_window import MainWindow
        self.main_window = MainWindow(user_id)
        self.main_window.show()
        self.loading_screen.close()
        self.close()

        
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

        gradient = QLinearGradient(0, 0, 0, rect.height())

        if self.current_theme == "dark":
            # Fondo oscuro elegante
            gradient.setColorAt(0.0, QColor(10, 10, 10))
            gradient.setColorAt(1.0, QColor(30, 30, 30))
        else:
            # Fondo claro clásico
            gradient.setColorAt(0.0, QColor(0, 0, 0))
            gradient.setColorAt(1.0, QColor(255, 140, 0))

        painter.fillRect(rect, QBrush(gradient))

        # Pintamos el logo giratorio encima
        if hasattr(self, 'logo_container'):
            global_pos = self.logo_container.mapTo(self, self.logo_container.rect().center())
            center_x = global_pos.x()
            center_y = global_pos.y()

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

    # Cargar tema desde settings
    import json
    try:
        with open("config/settings.json", "r") as f:
            config = json.load(f)
            theme = config.get("theme", "light")
    except (FileNotFoundError, json.JSONDecodeError):
        theme = "light"

    if theme == "dark":
        with open("themes/dark.qss", "r") as f:
            app.setStyleSheet(f.read())
    else:
        with open("themes/light.qss", "r") as f:
            app.setStyleSheet(f.read())

    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())