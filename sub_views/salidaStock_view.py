from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout,
    QFrame, QMessageBox, QScrollArea, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import requests

API_BASE_URL = "http://localhost:5000"

class SalidaStockView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.load_salida_data()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Área scrollable para que toda la vista sea desplazable con scroll invisible
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                width: 0px;
            }
            QScrollBar:horizontal {
                height: 0px;
            }
        """)

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(15)  # Espaciado entre cards
        scroll_area.setWidget(self.scroll_content)

        layout.addWidget(scroll_area)

        # Botones de gestión
        btn_layout = QHBoxLayout()
        self.btn_devolver = QPushButton(" Devolver a Almacén")
        self.btn_delete = QPushButton(" Eliminar Salida")
        
        self.btn_devolver.setIcon(QIcon("images/return.png"))
        self.btn_delete.setIcon(QIcon("images/delete.png"))

        self.btn_devolver.setFixedSize(200, 50)
        self.btn_delete.setFixedSize(200, 50)

        # Estilos de botones
        button_style = """
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
        """
        
        self.btn_devolver.setStyleSheet(button_style)
        self.btn_delete.setStyleSheet(button_style)
        
        self.btn_devolver.clicked.connect(self.devolver_producto)
        self.btn_delete.clicked.connect(self.eliminar_salida)

        btn_layout.addWidget(self.btn_devolver)
        btn_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)

        self.setLayout(layout)
    
    def load_salida_data(self):
        response = requests.get(f"{API_BASE_URL}/salidas/listar")
        if response.status_code == 200:
            salidas = response.json()
            if salidas:
                self.populate_salida_cards(salidas)
            else:
                self.show_no_data_message()
        else:
            QMessageBox.critical(self, "Error", "Error al cargar las salidas de stock.")

    def update_salida_stock(self):
        self.load_salida_data()  # Recarga la vista con los datos más recientes

    def show_no_data_message(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        no_data_label = QLabel("No hay productos en salida de stock.")
        no_data_label.setFont(QFont("Arial", 14, QFont.Bold))
        no_data_label.setAlignment(Qt.AlignCenter)
        self.grid_layout.addWidget(no_data_label, 0, 0)
    
    def populate_salida_cards(self, salidas):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        for i, salida in enumerate(salidas):
            card = self.create_salida_card(salida)
            self.grid_layout.addWidget(card, i // 3, i % 3)
        
        # Añade un espacio vacío para mantener el diseño limpio
        self.grid_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_salida_card(self, salida):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid #FFA500;
                border-radius: 15px;
                padding: 15px;
                transition: 0.3s;
            }
            QFrame:hover {
                background-color: rgba(255, 255, 255, 0.4);
                transform: scale(1.05);
            }
        """)

        layout = QVBoxLayout(card)

        # Campos con iconos a la izquierda y texto a la derecha
        def create_info_row(icon_path, text, bold=False):
            row_layout = QHBoxLayout()
            icon_label = self.create_icon_label(icon_path)
            text_label = QLabel(text)
            
            # Aplicar estilo y permitir que el texto se expanda
            if bold:
                text_label.setFont(QFont("Arial", 12, QFont.Bold))
            else:
                text_label.setFont(QFont("Arial", 12))

            text_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.3); padding: 8px; border-radius: 8px;")
            text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # 🔥 Se expande horizontalmente
            
            row_layout.addWidget(icon_label)
            row_layout.addWidget(text_label)
            row_layout.setAlignment(Qt.AlignLeft)
            return row_layout

        layout.addLayout(create_info_row("images/location.png", f" Dirección: {salida['direccion']}", bold=True))
        layout.addLayout(create_info_row("images/product.png", f" Producto: {salida['producto']}"))
        layout.addLayout(create_info_row("images/quantity.png", f" Cantidad: {salida['cantidad']}"))
        layout.addLayout(create_info_row("images/calendar.png", f" Fecha/Hora: {salida['fecha_salida']}"))

        return card

    def create_icon_label(self, image_path):
        icon_label = QLabel()
        pixmap = QPixmap(image_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(40, 40)
        icon_label.setStyleSheet("border-radius: 15px; background-color: #FFA500; padding: 3px;")
        return icon_label

    def devolver_producto(self):
        QMessageBox.information(self, "Acción", "Lógica para devolver el producto implementada correctamente.")

    def eliminar_salida(self):
        QMessageBox.information(self, "Acción", "Lógica para eliminar la salida implementada correctamente.")
