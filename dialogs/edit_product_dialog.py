import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QFormLayout, 
    QLineEdit, QComboBox, QPushButton, QHBoxLayout, 
    QSpacerItem, QSizePolicy, QMessageBox
)

# URL para la conexion con la api
API_BASE_URL = "http://localhost:5000"

# Dialog para editar un producto (Stock Actual)
class EditProductDialog(QDialog):
    def __init__(self, producto, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar/Eliminar Producto")
        self.setFixedSize(500, 400)
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

        self.producto_id = producto['id']

        layout = QVBoxLayout(self)

        # Logo
        logo = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(100, 100, Qt.KeepAspectRatio)
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title_label = QLabel("Editar/Eliminar Producto")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title_label)

        form_layout = QFormLayout()

        self.input_nombre = QLineEdit(producto['nombre'])
        self.input_cantidad = QLineEdit(str(producto['cantidad']))

        self.input_estado = QComboBox()
        self.input_estado.addItems(["Nuevo", "Usado", "Dañado"])
        self.input_estado.setCurrentText(producto['estado'])

        form_layout.addRow(QLabel("Nombre del Producto:"), self.input_nombre)
        form_layout.addRow(QLabel("Cantidad:"), self.input_cantidad)
        form_layout.addRow(QLabel("Estado:"), self.input_estado)

        layout.addLayout(form_layout)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.btn_confirm = QPushButton("Guardar")
        self.btn_confirm.setIcon(QIcon("images/check.png"))
        self.btn_confirm.clicked.connect(self.save_edited_product)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setIcon(QIcon("images/cancel.png"))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_delete = QPushButton("Eliminar")
        self.btn_delete.setIcon(QIcon("images/basura.png"))
        self.btn_delete.setStyleSheet("background-color: #E74C3C;")
        self.btn_delete.clicked.connect(self.confirm_delete_product)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_confirm)

        layout.addLayout(btn_layout)


    #  Guardar los cambios de la edicion del producto
    def save_edited_product(self):
        nombre = self.input_nombre.text().strip()
        cantidad = self.input_cantidad.text().strip()
        estado = self.input_estado.currentText()

        if not nombre or not cantidad.isdigit():
            QMessageBox.warning(self, "Error", "Por favor, ingrese un nombre válido y una cantidad numérica.")
            return

        try:
            response = requests.put(
                f"{API_BASE_URL}/productos/editar/{self.producto_id}",
                json={"nombre": nombre, "cantidad": int(cantidad), "estado": estado}
            )

            if response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Producto actualizado exitosamente.")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo actualizar el producto. Código de estado: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar con el servidor: {str(e)}")


    # Eliminacion de un producto desde la edición
    def confirm_delete_product(self):
        reply = QMessageBox.question(
            self, "Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este producto?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                response = requests.delete(f"{API_BASE_URL}/productos/eliminar/{self.producto_id}")
                if response.status_code == 200:
                    QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto. Código de estado: {response.status_code}")
            except requests.RequestException as e:
                QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar con el servidor: {str(e)}")
