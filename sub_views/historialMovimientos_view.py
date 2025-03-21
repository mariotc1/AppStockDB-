from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

class HistorialMovimientosView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Título principal
        title_label = QLabel("Historial de Movimientos")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Layout para futuros datos
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        # Botón de "Refrescar Datos"
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton(" Refrescar Datos")
        self.btn_refresh.setIcon(QIcon("images/refresh.png"))
        self.btn_refresh.setFixedSize(200, 50)

        # Estilo del botón
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
                transition: 0.3s;
            }
            QPushButton:hover {
                background-color: #FF8C00;
                transform: scale(1.05);
            }
        """)

        btn_layout.addWidget(self.btn_refresh)
        layout.addStretch()  # Empuja el botón hacia abajo
        layout.addLayout(btn_layout)

        self.setLayout(layout)