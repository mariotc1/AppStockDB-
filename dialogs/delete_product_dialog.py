"""
delete_product_dialog.py

Define el cuadro de diálogo `DeleteProductDialog` para eliminar un producto
desde la vista de stock actual. Muestra una confirmación al usuario y realiza
la petición DELETE a la API correspondiente.
"""

import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, 
    QPushButton, QHBoxLayout, QMessageBox
)

# URL para la conexion con la api
API_BASE_URL = "http://localhost:5000"

class DeleteProductDialog(QDialog):

    """
    Cuadro de diálogo para confirmar y ejecutar la eliminación de un producto.

    Este diálogo se utiliza en la subvista de Stock Actual para permitir
    al usuario eliminar definitivamente un producto del sistema.

    Hereda:
        QDialog

    Args:
        producto_id (int): ID del producto a eliminar.
        parent (QWidget, optional): Ventana que lanza este diálogo.

    Atributos:
        producto_id (int): ID del producto que se eliminará.
    """

    def __init__(self, producto_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Producto")
        self.setFixedSize(400, 300)

        # estilo de lso botones
        self.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #1F1F1F, stop:1 #2C3E50);
                border-radius: 20px;
            }
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 12px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton#btn_cancel {
                background-color: #7F8C8D;
            }
            QPushButton#btn_cancel:hover {
                background-color: #566573;
            }
            """
        )

        self.producto_id = producto_id

        layout = QVBoxLayout(self)

        # Logo de la empresa
        logo = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(100, 100, Qt.KeepAspectRatio)
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title_label = QLabel("¿Deseas eliminar este producto?")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 20px;")
        layout.addWidget(title_label)

        self.btn_confirm = QPushButton("Confirmar Eliminación")
        self.btn_confirm.setIcon(QIcon("images/check.png"))
        self.btn_confirm.clicked.connect(self.delete_product)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setIcon(QIcon("images/cancel.png"))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_confirm)

        layout.addLayout(btn_layout)


    """
    Envía una solicitud DELETE a la API para eliminar el producto.

    - Si la operación es exitosa, muestra un mensaje de éxito y cierra el diálogo.
    - Si falla, informa al usuario del código de error o fallo de conexión.
    """
    def delete_product(self):
        try:
            response = requests.delete(f"{API_BASE_URL}/productos/eliminar/{self.producto_id}")
            
            if response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
                self.accept()

            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto. Código de estado: {response.status_code}")

        except requests.RequestException as e:
            QMessageBox.critical(self, "Error de conexión", f"No se pudo conectar con el servidor: {str(e)}")
