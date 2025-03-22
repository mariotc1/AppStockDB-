import random
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QLabel, QFrame, QGraphicsDropShadowEffect, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt, QPoint, QSize, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap, QPainter, QPainterPath

class BubbleWidget(QWidget):
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.text = text
        self.is_user = is_user
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Icono circular del usuario o bot
        icon_label = QLabel()
        pixmap = QPixmap("images/usuaria.png" if self.is_user else "images/chatbot_icon.png")
        pixmap = pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Convertir imagen a circular
        mask = QPixmap(40, 40)
        mask.fill(Qt.transparent)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(0, 0, 40, 40)
        painter.end()

        pixmap.setMask(mask.mask())
        icon_label.setPixmap(pixmap)

        # Burbuja de texto
        bubble = QLabel(self.text)
        bubble.setWordWrap(True)
        bubble.setMaximumWidth(280)  # Mejor control del texto largo
        bubble.setStyleSheet(f"""
            background-color: {'#0078D7' if self.is_user else '#2C3E50'};
            border-radius: 12px;
            padding: 12px;
            color: white;
            font-size: 16px; /* Aumentado */
        """)

        if self.is_user:
            layout.addStretch()
            layout.addWidget(bubble)
            layout.addWidget(icon_label)
        else:
            layout.addWidget(icon_label)
            layout.addWidget(bubble)
            layout.addStretch()

class ChatPopup(QDialog):
    def __init__(self, parent_button, parent=None):
        super().__init__(parent)
        self.parent_button = parent_button
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(400, 600)
        self.initUI()
        self.showAnimation()
        self.positionPopup()

    def positionPopup(self):
        """Posiciona el chat emergente en la esquina inferior derecha."""
        self.show()
        QTimer.singleShot(50, self.recalculatePosition)

    def recalculatePosition(self):
        """Recalcula la posición tras renderizar la ventana."""
        if self.parent_button:
            global_pos = self.parent_button.mapToGlobal(QPoint(0, 0))
            x = global_pos.x() + self.parent_button.width() - self.width()
            y = global_pos.y() - self.height() - 10
            self.move(x, y)

    def showAnimation(self):
        """Animación de apertura."""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.recalculatePosition()
        start_rect = self.geometry()
        end_rect = self.geometry()
        start_rect.setY(start_rect.y() + 50)
        self.setGeometry(start_rect)

        self.animation.setDuration(300)
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Marco del chat
        main_frame = QFrame(self)
        main_frame.setStyleSheet("""
            background-color: #1E272E;
            border-radius: 10px;
            border: 1px solid #CCCCCC;
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 0)
        main_frame.setGraphicsEffect(shadow)

        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(10, 10, 10, 10)
        frame_layout.setSpacing(10)

        # Barra de título con botón de cerrar
        title_bar = QHBoxLayout()
        title_label = QLabel("Asistente Virtual")
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        close_button = QPushButton()
        close_button.setIcon(QIcon("images/cerrar.png"))
        close_button.setIconSize(QSize(16, 16))
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet("background-color: transparent;")
        close_button.clicked.connect(self.closeChat)
        title_bar.addWidget(title_label)
        title_bar.addStretch()
        title_bar.addWidget(close_button)
        frame_layout.addLayout(title_bar)

        # Área de chat
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #34495E;
            }
            QScrollBar:vertical {
                width: 0px; /* 🔥 Scroll invisible */
            }
            QScrollBar:horizontal {
                height: 0px; /* 🔥 Scroll invisible */
            }
        """)
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_area.setWidget(self.chat_widget)
        frame_layout.addWidget(self.chat_area)

        # Campo de entrada y botón de enviar
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(lambda: self.send_button.click())
        self.input_field.setPlaceholderText("Pregunta al asistente tu duda...")
        self.input_field.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 5px 15px;
            font-size: 16px; /* Aumentado */
        """)
        self.send_button = QPushButton()
        self.send_button.setIcon(QIcon("images/enviar.png"))
        self.send_button.setIconSize(QSize(24, 24))
        self.send_button.setFixedSize(40, 40)
        self.send_button.setStyleSheet("border-radius: 20px; background-color: #0078D7;")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        frame_layout.addLayout(input_layout)

        main_layout.addWidget(main_frame)
        self.input_field.returnPressed.connect(self.send_message)
        self.add_bot_message("¡Hola! ¿En qué puedo ayudarte hoy?")

    def closeChat(self):
        self.close()

    def send_message(self):
        user_message = self.input_field.text().strip()
        if not user_message:
            return
        self.add_user_message(user_message)
        self.input_field.clear()
        QTimer.singleShot(1000, lambda: self.get_bot_response(user_message))

    # Al pulsar la tecla 'enter' se envía el mensaje
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.send_message()
        else:
            super().keyPressEvent(event)

    def get_bot_response(self, user_message):
        response = self.generate_response(user_message)
        self.add_bot_message(response)

    def generate_response(self, message):
        """Genera respuestas basadas en palabras clave y frases comunes."""
        message = message.lower()

        # 🟢 Respuestas a saludos y preguntas generales
        saludos = ["hola", "buenas", "qué tal", "hey", "holi", "saludos"]
        estado = ["cómo estás", "cómo te va", "cómo te encuentras"]
        identidad = ["quién eres", "qué eres", "cómo te llamas"]

        if any(palabra in message for palabra in saludos):
            return random.choice([
                "¡Hola! ¿En qué puedo ayudarte hoy?",
                "¡Hey! ¿Necesitas ayuda con algo en la aplicación?",
                "¡Hola! Estoy aquí para asistirte. Pregunta lo que quieras."
            ])

        if any(palabra in message for palabra in estado):
            return random.choice([
                "Estoy funcionando al 100% para ayudarte. ¿En qué necesitas ayuda?",
                "¡Todo en orden! Pregunta lo que necesites.",
                "Aquí estoy, listo para responder tus dudas sobre la aplicación."
            ])

        if any(palabra in message for palabra in identidad):
            return random.choice([
                "Soy tu asistente virtual de Stock DB Inmuebles. Estoy aquí para resolver tus dudas.",
                "Soy un chatbot diseñado para ayudarte a gestionar el stock de tu empresa.",
                "Me llaman Asistente Virtual, pero puedes llamarme como quieras. 😉"
            ])

        # 🔹 Respuestas sobre el inicio de sesión y registro
        if "registro" in message or "registrar" in message:
            return "Para registrarte, proporciona un nombre, correo y una contraseña segura con mayúsculas, minúsculas, números y símbolos."

        if "contraseña" in message or "clave" in message:
            return "Si olvidaste tu contraseña, intenta recuperarla desde la pantalla de inicio. Recuerda que debe ser segura con mayúsculas, minúsculas, números y símbolos."

        if "iniciar sesión" in message or "login" in message:
            return "Para iniciar sesión, introduce tu correo y contraseña en la pantalla de acceso."

        if "no puedo iniciar sesión" in message or "error de login" in message:
            return "Si tienes problemas para iniciar sesión, verifica que tu correo y contraseña sean correctos. Si olvidaste la contraseña, intenta recuperarla."

        # 🔹 Respuestas sobre la gestión de stock
        if "stock" in message or "almacén" in message:
            return "Puedes gestionar el stock desde la vista 'Stock Actual'. Allí puedes agregar, modificar o eliminar productos."

        if "añadir producto" in message or "nuevo producto" in message:
            return "Para agregar un producto, dirígete a la vista 'Stock Actual' y pulsa en 'Añadir'. Completa los datos y guarda los cambios."

        if "modificar producto" in message or "editar producto" in message:
            return "Para modificar un producto, selecciónalo en la tabla de 'Stock Actual' y edita la información."

        if "eliminar producto" in message or "borrar producto" in message:
            return "Para eliminar un producto, selecciónalo en 'Stock Actual' y pulsa en 'Eliminar'. ¡Cuidado! No podrás recuperarlo."

        if "exportar stock" in message or "descargar stock" in message:
            return "Puedes exportar el stock a Excel desde la vista 'Stock Actual'. Busca la opción de 'Exportar' y guarda el archivo."

        # 🔹 Respuestas sobre la salida de stock
        if "salida de stock" in message or "producto salió" in message:
            return "Para registrar la salida de un producto, ve a la pestaña 'Salida de Stock' y añade la información necesaria."

        if "devolver producto" in message or "producto regresó" in message:
            return "Si un producto debe regresar al almacén, puedes hacer la devolución en 'Salida de Stock'."

        if "editar salida" in message or "modificar salida" in message:
            return "Para modificar una salida de stock, ve a la pestaña 'Salida de Stock', selecciona el producto y edítalo."

        # 🔹 Historial de movimientos
        if "historial" in message or "movimientos" in message:
            return "En 'Historial de Movimientos' puedes ver todas las entradas y salidas de stock."

        if "notificación de stock" in message or "correo de stock" in message:
            return "Cuando hay cambios en el stock, se envía una notificación automática a los correos asignados."

        # 🔹 Respuestas sobre el perfil del usuario
        if "perfil" in message or "mi cuenta" in message:
            return "Desde 'Mi Perfil' puedes cambiar tu nombre, foto y contraseña."

        if "cambiar foto" in message or "actualizar imagen" in message:
            return "Puedes cambiar tu foto de perfil en 'Mi Perfil'. Solo sube una imagen nueva y guárdala."

        if "cambiar nombre" in message:
            return "Para cambiar tu nombre de usuario, ve a 'Mi Perfil' y edita el campo correspondiente."

        if "cambiar contraseña" in message or "modificar clave" in message:
            return "Para cambiar tu contraseña, ve a 'Mi Perfil', introduce la nueva clave y guárdala."

        # 🔹 Preguntas generales sobre la aplicación
        if "cómo funciona" in message or "cómo usar" in message:
            return "La aplicación está organizada en vistas dentro del menú lateral. Explora cada una para ver sus funciones."

        if "cerrar sesión" in message:
            return "Para cerrar sesión, dirígete a la vista 'Volver a la pantalla de bienvenida'."

        if "salir" in message or "cerrar aplicación" in message:
            return "Para salir del programa, usa la opción 'Salir' en el menú lateral."

        if "problema" in message or "error" in message:
            return "Si tienes problemas con la aplicación, intenta reiniciarla. Si el error persiste, revisa la documentación o contacta al soporte."

        # 🔴 Si no encuentra una respuesta adecuada
        respuestas_genericas = [
            "No estoy seguro de entender tu pregunta. ¿Podrías reformularla?",
            "Parece que no tengo información sobre eso. ¿Puedes darme más detalles?",
            "Lo siento, pero no entiendo bien. ¿Podrías preguntar de otra forma?",
            "Interesante pregunta. Déjame pensar... ¿Podrías explicarlo de otro modo?"
        ]

        return random.choice(respuestas_genericas)

    def add_user_message(self, message):
        self.chat_layout.addWidget(BubbleWidget(message, is_user=True))
        self.scroll_to_bottom()

    def add_bot_message(self, message):
        self.chat_layout.addWidget(BubbleWidget(message, is_user=False))
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        self.chat_area.verticalScrollBar().setValue(self.chat_area.verticalScrollBar().maximum())