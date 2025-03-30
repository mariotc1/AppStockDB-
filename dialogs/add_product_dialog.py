import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFormLayout, QLineEdit, 
    QComboBox, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox
)

# URL para la conexión con la api rest
API_BASE_URL = "http://localhost:5000"

# Cuadro de diálogo para añadir un producto en la subvista de Stock Actual
class AddProductDialog(QDialog):
    def __init__(self, parent=None, categoria=None):
        super().__init__(parent)
        self.categoria = categoria
        self.setWindowTitle("Añadir Producto")
        self.setFixedSize(500, 400)

        # Estilo del dialog
        self.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #1F1F1F, stop:1 #2C3E50);
                border-radius: 20px;
            }
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid #BDC3C7;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #3498DB;
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton#btn_cancel {
                background-color: #E74C3C;
            }
            QPushButton#btn_cancel:hover {
                background-color: #C0392B;
            }
            """
        )
        
        layout = QVBoxLayout(self)
        
        # Logo
        logo = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(100, 100, Qt.KeepAspectRatio)
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        
        # Título del dialog
        title_label = QLabel("Añadir Nuevo Producto")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title_label)
        
        form_layout = QFormLayout()
        
        # Campo del nombre del producto
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ingrese el nombre del producto")
        
        # Campo de cantidad del producto
        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Ingrese la cantidad (solo números)")
        
        # Estados a elegir en los que se encuentra el producto
        self.input_estado = QComboBox()
        self.input_estado.addItems(["Nuevo", "Usado", "Dañado"])
        
        form_layout.addRow(QLabel("Nombre del Producto:"), self.input_nombre)
        form_layout.addRow(QLabel("Cantidad:"), self.input_cantidad)
        form_layout.addRow(QLabel("Estado:"), self.input_estado)
        
        layout.addLayout(form_layout)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)
        
        self.btn_confirm = QPushButton("Confirmar")
        self.btn_confirm.setIcon(QIcon("images/check.png"))
        self.btn_confirm.clicked.connect(self.save_product)
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setIcon(QIcon("images/cancel.png"))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_confirm)
        
        layout.addLayout(btn_layout)


    # Conexión con la api para guardar el nuevo producto
    def save_product(self):
        nombre = self.input_nombre.text().strip()
        cantidad = self.input_cantidad.text().strip()
        estado = self.input_estado.currentText()
        
        if not nombre or not cantidad.isdigit():
            QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre válido y una cantidad numérica")
            return
        
        try:
            response = requests.post(
                f"{API_BASE_URL}/productos/agregar",
                json={"nombre": nombre, "cantidad": int(cantidad), "estado": estado, "categoria": self.categoria}
            )
            
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Producto guardado exitosamente.")
                self.accept()

            else:
                QMessageBox.warning(self, "Error", f"No se pudo guardar el producto. Código de estado: {response.status_code}")

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar con el servidor: {str(e)}")