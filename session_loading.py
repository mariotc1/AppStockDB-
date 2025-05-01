import sys, json, os
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPainter, QLinearGradient, QBrush, QColor, QFont, QIcon
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect,
    QApplication, QFrame
)

class SessionLoading(QWidget):
    def __init__(self, username):
        super().__init__()

        self.username = username
        self.animations = []

        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except:
            self.current_theme = "light"

        self.initUI()
        self.setWindowTitle("AppStockDB")
        self.setWindowIcon(QIcon("images/logoDB_Blanco.png"))
        self.showMaximized()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        # Logo siempre blanco
        logo = QPixmap("images/logoDB_Blanco.png").scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label = QLabel()
        logo_label.setPixmap(logo)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Título en negrita
        title = QLabel("¡Inicio exitoso en AppStockDB!")
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setStyleSheet("color: white;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Subtítulo
        subtitle = QLabel(f"Preparando todo para ti, {self.username}...")
        subtitle.setFont(QFont("Arial", 18))
        subtitle.setStyleSheet("color: white;")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        # Card decorativo centrado
        card = QFrame()
        card.setFixedSize(600, 300)
        card.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
            border-radius: 20px;
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(15)
        card_layout.setAlignment(Qt.AlignCenter)

        card_img = QLabel()
        card_img.setPixmap(QPixmap("images/cargaDatos.png").scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        card_img.setStyleSheet("background-color: transparent;")
        card_img.setAlignment(Qt.AlignCenter)

        card_text = QLabel("Estamos cargando sus datos para que pueda trabajar.\nPor favor, espere un momento...")
        card_text.setStyleSheet("color: white; font-size: 20px; background-color: transparent;")
        card_text.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(card_img)
        card_layout.addWidget(card_text)
        layout.addWidget(card)

        layout.addStretch()

        footer = QLabel("© 2025 DB Inmuebles. Todos los derechos reservados.")
        footer.setStyleSheet("color: white; font-size: 18px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.fadeInWidget(title, 1500)
        self.fadeInWidget(subtitle, 2000)
        self.fadeInWidget(card, 2300)

    def fadeInWidget(self, widget, duration):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(duration)
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self.animations.append(anim)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())

        if self.current_theme == "dark":
            gradient.setColorAt(0.0, QColor(10, 10, 10))
            gradient.setColorAt(1.0, QColor(30, 30, 30))
        else:
            gradient.setColorAt(0.0, QColor(0, 0, 0))
            gradient.setColorAt(1.0, QColor(255, 140, 0))

        painter.fillRect(rect, QBrush(gradient))

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
    win = SessionLoading("Mario")
    win.show()
    sys.exit(app.exec_())