import smtplib, sys, math, requests

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from PyQt5.QtCore import ( 
    Qt, QTimer, QPropertyAnimation, 
    QEasingCurve, QSize
)

from PyQt5.QtGui import (
    QPainter, QPixmap, QTransform, QLinearGradient, 
    QBrush, QColor, QFont, QIcon
)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QGraphicsOpacityEffect, QLineEdit, 
    QGraphicsDropShadowEffect, QMessageBox, QToolButton
)

# Pantalla de inicio de sesión
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Inicializo la lista de animaciones
        self.animations = []

        # Cargo el logo y lo escalo
        self.logo = QPixmap("images/logoDB_Blanco.png")
        self.logo = self.logo.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Variables para la rotación del logo
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)  # velocidad del giro

        self.initUI()

        # Ahora que todo está creado, recién ahora maximizas
        self.showMaximized()

    # Creacion de la interfaz
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)

        # Contenedor para el logo
        logo_container = QWidget()
        logo_container.setFixedSize(300, 300)
        main_layout.addWidget(logo_container, alignment=Qt.AlignCenter)
        self.logo_container = logo_container

        # Título
        title_label = QLabel("Inicia Sesión")
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Contenedor para los campos de entrada
        fields_layout = QVBoxLayout()
        fields_layout.setSpacing(15)

        # Campo: Correo
        self.email_field = self.createInputField("Correo", "images/icon_email.png", is_password=False)
        fields_layout.addLayout(self.email_field)

        # Campo: Contraseña
        self.password_field = self.createInputField("Contraseña", "images/icon_password.png", is_password=True)
        fields_layout.addLayout(self.password_field)

        main_layout.addLayout(fields_layout)

        # Botones de Iniciar Sesión y Volver (pantalla de bienvenida)
        bottom_buttons_layout = QHBoxLayout()
        self.btn_login = QPushButton("INICIAR SESIÓN")
        self.btn_back = QPushButton("VOLVER")

        # Estilo de lso botones
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

        self.btn_login.setStyleSheet(btn_style)
        self.btn_back.setStyleSheet(btn_style)
        
        self.applyShadow(self.btn_login)
        self.applyShadow(self.btn_back)

        bottom_buttons_layout.addWidget(self.btn_login)
        bottom_buttons_layout.addWidget(self.btn_back)
        
        main_layout.addLayout(bottom_buttons_layout)

        main_layout.addSpacing(20)

        # Enlaces a otras pantallas con QToolButton
        additional_layout = QHBoxLayout()
        additional_layout.setSpacing(40)
        
        self.btn_no_account = QToolButton()
        self.btn_no_account.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_no_account.setText("¿No tienes cuenta?\nRegístrate")
        self.btn_no_account.setIcon(QIcon("images/registrate.png"))
        self.btn_no_account.setIconSize(QSize(48, 48))
        self.btn_no_account.setAutoRaise(True)
        
        self.btn_forgot_password = QToolButton()
        self.btn_forgot_password.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.btn_forgot_password.setText("¿Has olvidado la\ncontraseña?")
        self.btn_forgot_password.setIcon(QIcon("images/olvido.png"))
        self.btn_forgot_password.setIconSize(QSize(48, 48))
        self.btn_forgot_password.setAutoRaise(True)
        
        additional_layout.addStretch()
        
        additional_layout.addWidget(self.btn_no_account)
        additional_layout.addWidget(self.btn_forgot_password)
        
        additional_layout.addStretch()
        
        main_layout.addLayout(additional_layout)

        main_layout.addStretch()

        # Footer
        footer_label = QLabel("© 2025 DB Inmuebles. Todos los derechos reservados.")
        footer_label.setStyleSheet("color: white; font-size: 18px;")
        footer_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(footer_label)

        # Animaciones de aparición de los elementos
        self.fadeInWidget(title_label, 1500, QEasingCurve.OutCubic)
        self.fadeInWidget(self.btn_login, 2000, QEasingCurve.OutCubic)
        self.fadeInWidget(self.btn_back, 2000, QEasingCurve.OutCubic)
        self.fadeInWidget(self.btn_no_account, 2000, QEasingCurve.OutCubic)
        self.fadeInWidget(self.btn_forgot_password, 2000, QEasingCurve.OutCubic)

        # Conexión de señales
        self.btn_login.clicked.connect(self.login)
        self.btn_back.clicked.connect(self.goBack)
        self.btn_no_account.clicked.connect(self.openRegister)
        self.btn_forgot_password.clicked.connect(self.forgotPassword)

        self.setLayout(main_layout)


    # Efecto de sombra a un widget
    def applyShadow(self, widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        widget.setGraphicsEffect(shadow)


    # Creo un layout horizontal que contiene el icno del ojo, y si is_password es True se añade el botón para mostrar/ocultar contraseña
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


    # Cambio de icono dependiendo de si se muestra/oculta la contraseña
    def togglePasswordVisibility(self, checked, line_edit, button):
        if checked:
            line_edit.setEchoMode(QLineEdit.Normal)
            button.setIcon(QIcon("images/icon_eye.png"))

        else:
            line_edit.setEchoMode(QLineEdit.Password)
            button.setIcon(QIcon("images/icon_eye_off.png"))


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


    # Método de conexión con la api rest para inicar sesión
    def login(self):
        url = "http://localhost:5000/login"

        data = {
            "email": self.email_field.itemAt(1).widget().text(),
            "password": self.password_field.itemAt(1).widget().text()
        }

        try:
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                user_data = response.json()
                user_id = user_data.get("user_id", "")

                if not user_id:
                    self.showDialog("Error", "No se ha recibido el ID del usuario.", QMessageBox.Critical)
                    return

                self.showDialog("Inicio de Sesión", f"Inicio de sesión exitoso. ¡Bienvenido, {user_data.get('username', '')}!", QMessageBox.Information)

                # Muestra Loading Screen
                from dialogs.loading_screen import LoadingScreen
                self.loading_screen = LoadingScreen()
                self.loading_screen.show()

                # Carga MainWindow con un pequeño delay para permitir la animación
                QTimer.singleShot(100, lambda: self.openMainWindow(user_id))

            else:
                error_message = response.json().get("error", "Error desconocido.")
                self.showDialog("Error de Inicio de Sesión", error_message, QMessageBox.Critical)

        except Exception as e:
            self.showDialog("Error de Conexión", str(e), QMessageBox.Critical)


    def openMainWindow(self, user_id):
        from main_window import MainWindow
        self.main_window = MainWindow(user_id)
        self.main_window.show()
        self.loading_screen.close()
        self.close()



    # Dialog personalizado: muestra un cuadro de diálogo con un título, mensaje y logo
    def showDialog(self, title, message, icon=QMessageBox.Information):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(icon)
        logo = QPixmap("images/logoDB_Negro.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        msg_box.setIconPixmap(logo)
        msg_box.exec_()


    # Volver a la pantalla de bienvenida
    def goBack(self):
        print("Volviendo a la pantalla de bienvenida...")
        from welcome_window import WelcomeWindow
        self.close()
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()


    # LLevar a la pantalla de resgistro
    def openRegister(self):
        print("Abriendo pantalla de registro...")
        from register_window import RegisterWindow
        self.close()
        self.register_window = RegisterWindow()
        self.register_window.show()


    # Enviar un correo de recuperción de la contraseña
    def send_recovery_email(self, recipient_email, recovery_code):
        """Envía un correo de recuperación de contraseña con un código temporal."""
        sender_email = "gestionstockdb@gmail.com"
        subject = "Recuperación de Contraseña - Gestión de Stock"
        body = f"""
        <html>
            <body>
                <h2>Recuperación de Contraseña</h2>
                <p>Has solicitado restablecer tu contraseña.</p>
                <p>Usa este código para continuar con el proceso de recuperación:</p>
                <h3>{recovery_code}</h3>
                <p>Si no solicitaste este cambio, ignora este mensaje.</p>
                <p>Para más ayuda, contacta a <a href='mailto:gestionstockdb@gmail.com'>gestionstockdb@gmail.com</a>.</p>
            </body>
        </html>
        """

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, "tjjw gvdp tlot rege") # contraseña genera para este proyecto por seguridad
                server.sendmail(sender_email, recipient_email, msg.as_string())
                print("Correo de recuperación enviado con éxito")

        except Exception as e:
            print(f"Error al enviar el correo: {e}")


    # Valido el formato del correo con una regex
    def is_valid_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None


    # Funcion para recuperar la contraseña 
    def forgotPassword(self):
        email = self.email_field.itemAt(1).widget().text().strip()
        
        if not email:
            self.showDialog("Error", "Por favor, introduce tu correo electrónico.", QMessageBox.Critical)
            return

        if not self.is_valid_email(email):
            self.showDialog("Error", "El correo electrónico no es válido.", QMessageBox.Critical)
            return

        url = "http://localhost:5000/forgot-password"
        data = {"email": email}

        try:
            response = requests.post(url, json=data)
            
            if response.status_code != 200:
                try:
                    error_message = response.json().get("error", "Error desconocido.")
                except ValueError:
                    error_message = "Respuesta no válida del servidor."
                self.showDialog("Error", error_message, QMessageBox.Critical)

                return

            # Si la API responde correctamente
            json_response = response.json()
            recovery_code = json_response.get("recovery_code", "000000")
            self.send_recovery_email(email, recovery_code)
            self.showDialog("Correo Enviado", "Se ha enviado un código de recuperación a tu correo", QMessageBox.Information)

        except requests.exceptions.RequestException as e:
            self.showDialog("Error de Conexión", f"No se pudo conectar con el servidor: {e}", QMessageBox.Critical)

        except ValueError:
            self.showDialog("Error", "Respuesta inválida del servidor", QMessageBox.Critical)


    # Mostrar un mensaje de error
    def showError(self, message):
        print("Error:", message)


    # Mostrar un mensaje
    def showMessage(self, message):
        print("Mensaje:", message)


    # Actualizar la rotación del logo
    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()


    # 'Pinto' el fondo de la pantalla con un degradado de negro a naranja
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        
        # Degradado de negro a naranja
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0.0, QColor(0, 0, 0))
        gradient.setColorAt(1.0, QColor(255, 140, 0))
        painter.fillRect(rect, QBrush(gradient))

        # 'Dibujo' el logo giratorio usando la geometría del logo_container si existe
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


    # Animación de fade in para la ventana
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
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())