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
        pixmap = QPixmap("images/usuario.png" if self.is_user else "images/chatbot_icon.png")
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
        bubble.setMaximumWidth(280)
        bubble.setStyleSheet(f"""
            background-color: {'#0078D7' if self.is_user else '#2C3E50'};
            border-radius: 12px;
            padding: 12px;
            color: white;
            font-size: 14px;
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
        self.chat_area.setStyleSheet("border: none; background-color: #34495E;")
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_area.setWidget(self.chat_widget)
        frame_layout.addWidget(self.chat_area)

        # Campo de entrada y botón de enviar
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Pregunta al asistente tu duda...")  # Sugerencia en gris
        self.input_field.setStyleSheet("""
            background-color: white;
            border-radius: 15px;
            padding: 5px 15px;
            font-size: 16px; /* Aumentamos el tamaño del texto */
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

    def get_bot_response(self, user_message):
        response = self.generate_response(user_message)
        self.add_bot_message(response)