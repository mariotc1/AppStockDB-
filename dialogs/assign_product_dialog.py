import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, 
    QLineEdit, QPushButton, QHBoxLayout, QSpinBox,
    QScrollArea, QWidget, QMessageBox
)

# URL para la conexion con la api
API_BASE_URL = "http://localhost:5000"

# Dialog para asignar uno o varios productos a una direccion 
class AssignProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("Asignar Productos")
        self.setFixedSize(600, 600)

        # estilo del dialog
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
            QComboBox, QLineEdit, QSpinBox {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                border: 1px solid #BDC3C7;
            }
            QComboBox:focus, QLineEdit:focus, QSpinBox:focus {
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
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            """
        )
        
        main_layout = QVBoxLayout(self)
        
        # Logo
        logo = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(100, 100, Qt.KeepAspectRatio)
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo)
        
        title_label = QLabel("Asignar Productos a Dirección")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 20px;")
        main_layout.addWidget(title_label)
        
        # Área desplazable para productos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
        
        self.product_entries = []
        self.add_product_entry()
        
        self.btn_add_more = QPushButton(" Añadir otro producto")
        self.btn_add_more.setIcon(QIcon("images/add.png"))
        self.btn_add_more.clicked.connect(self.add_product_entry)
        main_layout.addWidget(self.btn_add_more)
        
        main_layout.addWidget(QLabel("Dirección de destino:"))
        self.input_direccion = QLineEdit()
        self.input_direccion.setPlaceholderText("Ingrese la dirección de destino")
        main_layout.addWidget(self.input_direccion)
        
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setIcon(QIcon("images/cancel.png"))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_confirm = QPushButton("Asignar")
        self.btn_confirm.setIcon(QIcon("images/check.png"))
        self.btn_confirm.clicked.connect(self.assign_products)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_confirm)
        
        main_layout.addLayout(btn_layout)
    

    # Añadir el producto y su respectiva cantidad
    def add_product_entry(self):
        entry_layout = QHBoxLayout()
        product_dropdown = QComboBox()
        quantity_spinbox = QSpinBox()
        quantity_spinbox.setMinimum(1)
        
        self.load_products(product_dropdown, quantity_spinbox)
        
        entry_layout.addWidget(QLabel("Producto:"))
        entry_layout.addWidget(product_dropdown)
        entry_layout.addWidget(QLabel("Cantidad:"))
        entry_layout.addWidget(quantity_spinbox)
        
        self.form_layout.addLayout(entry_layout)
        self.product_entries.append((product_dropdown, quantity_spinbox))
    

    # Cargo todos los proctos creados
    def load_products(self, dropdown, spinbox):
        try:
            response = requests.get(f"{API_BASE_URL}/productos/listar")
            response.raise_for_status()
            productos = response.json()
            dropdown.clear()  

            for producto in productos:
                dropdown.addItem(f"{producto['nombre']} (Disponible: {producto['cantidad']})", producto["id"])
                spinbox.setMaximum(producto['cantidad'])

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo cargar la lista de productos: {str(e)}")
    

    # Asigano uno o varios a una direccion
    def assign_products(self):
        asignaciones = []

        for product_dropdown, quantity_spinbox in self.product_entries:
            producto_id = product_dropdown.currentData()
            cantidad = quantity_spinbox.value()

            if cantidad > 0:
                asignaciones.append({
                    "producto_id": producto_id,
                    "cantidad": cantidad,
                    "direccion": self.input_direccion.text()
                })

        if not asignaciones:
            QMessageBox.warning(self, "Error", "Por favor, seleccione al menos un producto y especifique una cantidad.")
            return

        if not self.input_direccion.text().strip():
            QMessageBox.warning(self, "Error", "Por favor, ingrese una dirección de destino.")
            return

        try:
            # Primero: Asignar productos al destino (salida de stock)
            response = requests.post(
                f"{API_BASE_URL}/productos/asignar_multiples",
                json={"asignaciones": asignaciones}
            )
            response.raise_for_status()

            # Segundo: Registrar cada asignación como movimiento de salida en historial
            for asignacion in asignaciones:
                movimiento = {
                    "producto_id": asignacion["producto_id"],
                    "tipo_movimiento": "Salida",
                    "cantidad": asignacion["cantidad"],
                    "direccion": asignacion["direccion"],
                    "detalles": "Asignación registrada automáticamente"
                }
                try:
                    requests.post(f"{API_BASE_URL}/historial/registrar", json=movimiento)
                except requests.RequestException as e:
                    print(f"[WARN] No se pudo registrar en historial: {e}")

            QMessageBox.information(self, "Éxito", "Productos asignados correctamente.")
            self.accept()

            # Recargar vista de salida de stock si existe
            if self.parent and hasattr(self.parent, 'show_salida_stock'):
                self.parent.show_salida_stock()
                if hasattr(self.parent, 'load_salida_data'):
                    self.parent.load_salida_data()

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", f"No se pudieron asignar los productos: {str(e)}")