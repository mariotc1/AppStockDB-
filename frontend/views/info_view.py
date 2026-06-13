"""
Vista principal de información y ayuda de la aplicación.

Muestra al usuario un manual visual interactivo con tarjetas explicativas, 
cada una con su título, descripción y acceso a un vídeo demostrativo. 
Está diseñada para facilitar la comprensión del funcionamiento de la app.

Las tarjetas abordan temas como navegación, personalización del perfil, 
gestión de stock y uso del chatbot.

:param parent: Widget padre opcional.
"""

import os

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel,
    QSizePolicy, QPushButton
)

from styles.simple_card import SimpleCard
from styles.circular_icon import CircularIcon
from styles.styled_button import StyledButton
from dialogs.videoPlayer_dialog import VideoPlayerDialog


class InfoView(QWidget):

    """
    Inicializa la vista de información, cargando el tema actual desde configuración
    y construyendo toda la interfaz visual de ayuda.
    
    :param parent: Widget padre opcional.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        import json

        # Leer el tema actual
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_theme = "light"

        self.initUI()


    """
    Crea una tarjeta visual informativa con icono, título, descripción y botón para ver video.

    :param icon_path: Ruta al icono que se mostrará en la parte superior de la tarjeta.
    :param title_text: Título principal de la tarjeta.
    :param content_text: Texto descriptivo con viñetas o explicación.
    :param video_file: Nombre del archivo de video explicativo asociado.
    :return: Widget completo de la tarjeta (SimpleCard).
    """
    def createCard(self, icon_path, title_text, content_text, video_file):
        card = SimpleCard()
        card.setMinimumSize(250, 280)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)

        icon_label = CircularIcon(icon_path, size=80)
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        title_label = QLabel(title_text)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: white; letter-spacing: 0.5px;")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        content_label = QLabel(content_text)
        content_label.setFont(QFont("Arial", 14))
        content_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        content_label.setWordWrap(True)
        content_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        card_layout.addWidget(content_label)

        learn_more_btn = StyledButton("Aprender más", theme=self.current_theme)
        learn_more_btn.setIcon(QIcon("images/b_aprendeMas.png"))

        learn_more_btn.clicked.connect(lambda: self.show_video(video_file))
        card_layout.addWidget(learn_more_btn, alignment=Qt.AlignCenter)

        return card

    
    """
    Muestra el video explicativo correspondiente a una tarjeta mediante un cuadro de diálogo.

    :param video_file: Nombre del archivo de video (ubicado en la carpeta 'videos').
    """
    def show_video(self, video_file):
        video_path = os.path.join('videos', video_file)
        if os.path.exists(video_path):
            video_dialog = VideoPlayerDialog(video_path)
            video_dialog.exec_()
        else:
            print(f"ERROR: No se encontró el archivo de video: {video_file}")


    """
    Construye y organiza visualmente toda la vista, incluyendo el título principal 
    y las tarjetas de ayuda agrupadas en un `QGridLayout`.
    """
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        main_title = QLabel("Manual de Uso y Funcionalidades")
        main_title.setFont(QFont("Arial", 28, QFont.Bold))
        main_title.setStyleSheet("color: white; letter-spacing: 1px;")
        main_layout.addWidget(main_title, alignment=Qt.AlignHCenter | Qt.AlignTop)

        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(0, 10, 0, 0)
        grid_layout.setSpacing(20)
        grid_layout.setAlignment(Qt.AlignCenter)

        # Card Navegación inteigente: explicaión + video
        card_nav = self.createCard("images/navigation.png", 
                                   "Navegación Inteligente",
                                     "• Menú lateral expandible al acercar el ratón, para acceder a las funciones.\n"
                                     "• Acceso rápido a todas las secciones con un solo click.\n"
                                     "• Cambio entre modo oscuro y claro en toda la app.\n"
                                     "• Guarda tú sesión.\n", 
                                     "navegacion_inteligente.mp4")
        grid_layout.addWidget(card_nav, 0, 0)

        # Card Personalización de tu Perfil: explicación + video
        card_op = self.createCard("images/usuario.png", 
                                "Personalización de Tu Perfil", 
                                "• Cambia la imagen de perfil por una personalizada.\n"
                                "• Tu foto saldrá de forma sincronizada en el menú lateral\n"
                                "• Consulta y edita tu nombre de usuario si lo necesitas.\n"
                                "• Cambia tu contraseña si lo necesitas\n", 
                                "mi_perfil.mp4")

        grid_layout.addWidget(card_op, 0, 1)

        # Card Gestión de Moviliario Avanzada: explicación + *falta el video
        card_mob = self.createCard("images/en_stock.png", 
                                   "Gestión de Mobiliario Avanzada", 
                                   "• Gestión integral del ciclo de vida del mobiliario\n"
                                   "• Seguimiento en tiempo real de la ubicación y estado.\n"
                                   "• Sistema de etiquetado avanzado\n"
                                   "• Seguimiento en tiempo real", 
                                   "gestion_de_stock.mp4")
        grid_layout.addWidget(card_mob, 1, 0)

        # Card Chat Bot: explicación + video
        card_chat = self.createCard("images/chatbot_icon.png", 
                                    "Chat-Bot Inteligente", 
                                    "• Asistente virtual para la resolución de tus dudas sobre la app\n"
                                    "• Aprendizaje continuo basado en interacciones\n"
                                    "• Análisis de sentimientos para mejorar la experiencia\n"
                                    "• Integración con base de conocimientos", 
                                    "uso_de_chatbot.mp4")
        grid_layout.addWidget(card_chat, 1, 1)

        main_layout.addLayout(grid_layout)