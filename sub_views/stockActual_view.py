from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QFrame, QMessageBox, QDialog, QFormLayout, QLineEdit, QComboBox
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize
from dialogs.add_product_dialog import AddProductDialog
from dialogs.assign_product_dialog import AssignProductDialog
from dialogs.edit_product_dialog import EditProductDialog
from dialogs.delete_product_dialog import DeleteProductDialog
import requests

API_BASE_URL = "http://localhost:5000"

class StockActualView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.load_stock_data()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        # Botones de gestión
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton(" Añadir Producto")
        self.btn_assign = QPushButton(" Asignar Producto/s a Mobiliario")
        self.btn_export = QPushButton(" Exportar a Excel")
        
        self.btn_add.setIcon(QIcon("images/add.png"))
        self.btn_assign.setIcon(QIcon("images/assign.png"))
        self.btn_export.setIcon(QIcon("images/excel.png"))

        self.btn_add.setFixedSize(200, 50)
        self.btn_assign.setFixedSize(300, 50)
        self.btn_export.setFixedSize(200, 50)

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
        
        self.btn_add.setStyleSheet(button_style)
        self.btn_assign.setStyleSheet(button_style)
        self.btn_export.setStyleSheet(button_style)
        
        self.btn_add.clicked.connect(self.add_product)
        self.btn_assign.clicked.connect(self.assign_product)
        self.btn_export.clicked.connect(self.export_to_excel)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_assign)
        btn_layout.addWidget(self.btn_export)
        layout.addStretch()
        layout.addLayout(btn_layout)

        self.setLayout(layout)
    
    def load_stock_data(self):
        response = requests.get(f"{API_BASE_URL}/productos/listar")
        if response.status_code == 200:
            productos = response.json()
            self.populate_stock_cards(productos)
    
    def populate_stock_cards(self, productos):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        for i, producto in enumerate(productos):
            card = self.create_product_card(producto)
            self.grid_layout.addWidget(card, i // 3, i % 3)
    
    def create_product_card(self, producto):
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
        
        # Iconos en círculos
        def create_icon_label(image_path):
            icon_label = QLabel()
            pixmap = QPixmap(image_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(40, 40)
            icon_label.setStyleSheet("border-radius: 15px; background-color: #FFA500; padding: 3px;")
            return icon_label
        
        icon_nombre = create_icon_label("images/product_icon.png")
        icon_estado = create_icon_label("images/estado.png")
        icon_cantidad = create_icon_label("images/cantidad.png")
        
        # Etiquetas con iconos y texto mejorado
        label_nombre = QLabel(f" {producto['nombre']}")
        label_nombre.setFont(QFont("Arial", 12, QFont.Bold))
        
        label_estado = QLabel(f" Estado: {producto['estado']}")
        label_estado.setFont(QFont("Arial", 12))
        
        label_cantidad = QLabel(f" Stock: {producto['cantidad']}")
        label_cantidad.setFont(QFont("Arial", 12))
        
        # Layouts para alinear iconos y texto
        row_nombre = QHBoxLayout()
        row_nombre.addWidget(icon_nombre)
        row_nombre.addWidget(label_nombre)
        
        row_estado = QHBoxLayout()
        row_estado.addWidget(icon_estado)
        row_estado.addWidget(label_estado)
        
        row_cantidad = QHBoxLayout()
        row_cantidad.addWidget(icon_cantidad)
        row_cantidad.addWidget(label_cantidad)
        
        # Botones de acción más juntos
        btn_edit = QPushButton()
        btn_edit.setIcon(QIcon("images/edit.png"))
        btn_edit.setFixedSize(40, 40)
        btn_edit.setStyleSheet("border: none; background-color: transparent;")
        btn_edit.clicked.connect(lambda: self.edit_product(producto))
        
        btn_delete = QPushButton()
        btn_delete.setIcon(QIcon("images/delete.png"))
        btn_delete.setFixedSize(38, 38)
        btn_delete.setStyleSheet("border: none; background-color: transparent;")
        btn_delete.clicked.connect(lambda: self.delete_product(producto['id']))
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.setSpacing(5)  # Espacio reducido entre botones
        btn_layout.setAlignment(Qt.AlignRight)
        
        layout.addLayout(row_nombre)
        layout.addLayout(row_estado)
        layout.addLayout(row_cantidad)
        layout.addLayout(btn_layout)
        
        return card
    
    def add_product(self):
        dialog = AddProductDialog(self)  # Crea la ventana de añadir producto
        if dialog.exec_():  # Si el usuario confirma, recargamos los datos
            self.load_stock_data()

    def save_product(self, dialog, nombre, cantidad, estado):
        if not nombre or not cantidad.isdigit():
            QMessageBox.warning(self, "Error", "Datos inválidos.")
            return
        
        response = requests.post(f"{API_BASE_URL}/productos/agregar", json={"nombre": nombre, "cantidad": cantidad, "estado": estado, "categoria": "Habitaciones"})
        if response.status_code == 201:
            QMessageBox.information(self, "Éxito", "Producto añadido correctamente.")
            dialog.accept()
            self.load_stock_data()
        else:
            QMessageBox.critical(self, "Error", "No se pudo añadir el producto.")
    
    def edit_product(self, producto):
        dialog = EditProductDialog(producto, self)
        if dialog.exec_():
            self.load_stock_data()  # Recarga los datos si se ha editado con éxito

    def delete_product(self, producto_id):
        dialog = DeleteProductDialog(producto_id, self)
        if dialog.exec_():  # Si el usuario confirma, recargamos los datos
            self.load_stock_data()

    def assign_product(self):
        dialog = AssignProductDialog(self)
        if dialog.exec_():  
            self.load_stock_data()

    def export_to_excel(self):
        response = requests.get(f"{API_BASE_URL}/productos/exportar")
        if response.status_code == 200:
            QMessageBox.information(self, "Éxito", "Exportación a Excel completada correctamente.")
        else:
            QMessageBox.critical(self, "Error", "No se pudo exportar a Excel.")