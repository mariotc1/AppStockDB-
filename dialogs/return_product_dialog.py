"""
return_product_dialog.py

Este módulo define el cuadro de diálogo `ReturnProductDialog`, que permite
devolver total o parcialmente un producto previamente asignado.

La devolución genera automáticamente un movimiento de tipo "Entrada" 
en el historial de movimientos y, si la cantidad devuelta es total, 
el producto se elimina de las salidas.

Requiere conexión con la API REST para actualizar los datos en la base de datos.
"""

import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QRadioButton, QButtonGroup,
    QPushButton, QHBoxLayout, QMessageBox
)

# URL para la conexión con la api rest
API_BASE_URL = "http://localhost:5000"

# Cuadro de diálogo para devolver los productos
class ReturnProductDialog(QDialog):

    """
    Inicializa el diálogo con la información del producto a devolver.

    Carga el diseño visual, las opciones de cantidad total/parcial y
    prepara los botones de acción para cancelar o confirmar la devolución.
    """
    def __init__(self, salida, parent=None, categoria=None):
        super().__init__(parent)
        self.salida = salida
        self.categoria = categoria
        self.setWindowTitle("Devolver Producto")
        self.setFixedSize(500, 450)
        self.setStyleSheet(
            "QDialog {"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2C3E50, stop:1 #1F1F1F);"
            "border-radius: 20px;"
            "}"
            "QLabel { color: #FFFFFF; font-size: 18px; }"
            "QRadioButton { color: #FFFFFF; font-size: 16px; }"
            "QPushButton#btn_confirmar { background-color: #27AE60; color: #FFFFFF; border-radius: 10px; padding: 10px; font-size: 16px; }"
            "QPushButton#btn_confirmar:hover { background-color: #229954; }"
            "QPushButton#btn_cancelar { background-color: #E74C3C; color: #FFFFFF; border-radius: 10px; padding: 10px; font-size: 16px; }"
            "QPushButton#btn_cancelar:hover { background-color: #C0392B; }"
            "QSpinBox { background-color: #FFFFFF; color: #000000; padding: 8px; border-radius: 8px; font-size: 20px; }"
        )

        layout = QVBoxLayout(self)

        # Logo de la empresa
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(100, 100, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Título
        title_label = QLabel(f"Devolver '{salida['producto']}'")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        cantidad_total = salida['cantidad']
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setMinimum(1)
        self.cantidad_input.setMaximum(cantidad_total)
        self.cantidad_input.setValue(cantidad_total)
        self.cantidad_input.setEnabled(False)

        self.opcion_total = QRadioButton("Devolver toda la cantidad")
        self.opcion_parcial = QRadioButton("Devolver cantidad parcial")
        self.opcion_total.setChecked(True)

        self.opcion_total.toggled.connect(lambda: self.toggle_cantidad(False))
        self.opcion_parcial.toggled.connect(lambda: self.toggle_cantidad(True))

        self.opcion_group = QButtonGroup(self)
        self.opcion_group.addButton(self.opcion_total)
        self.opcion_group.addButton(self.opcion_parcial)

        layout.addWidget(self.opcion_total)
        layout.addWidget(self.opcion_parcial)
        layout.addWidget(QLabel("Cantidad a devolver:"))
        layout.addWidget(self.cantidad_input)

        # Botones de Confirmar y Cancelar
        btn_layout = QHBoxLayout()
        btn_confirmar = QPushButton(" Confirmar")
        btn_confirmar.setObjectName("btn_confirmar")
        btn_confirmar.setIcon(QIcon("images/check.png"))
        btn_confirmar.clicked.connect(self.devolver_producto)

        btn_cancelar = QPushButton(" Cancelar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.setIcon(QIcon("images/cancel.png"))
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_confirmar)

        layout.addLayout(btn_layout)


    """
    Habilita o deshabilita el campo de entrada de cantidad según 
    la opción de devolución seleccionada por el usuario.

    Args:
        enabled (bool): Si True, el usuario puede introducir una cantidad personalizada.
    """
    def toggle_cantidad(self, enabled):
        self.cantidad_input.setEnabled(enabled)


    """
    Realiza la devolución del producto a través de la API REST.

    1. Envía una petición PUT para devolver el producto.
    2. Si es exitoso, registra un nuevo movimiento de tipo "Entrada".
    3. Muestra mensajes según el resultado (éxito, error parcial o total).
    4. Cierra el diálogo si todo fue correcto.
    """
    def devolver_producto(self):
        cantidad_a_devolver = self.cantidad_input.value()
        try:
            response = requests.put(f"{API_BASE_URL}/salidas/devolver/{self.salida['id']}",
                                    json={'cantidad': cantidad_a_devolver})
            if response.status_code == 200:
                data = response.json()
                nueva_cantidad = data.get('nueva_cantidad')

                movimiento = {
                    "producto_id": self.salida['producto_id'],
                    "tipo_movimiento": "Entrada",
                    "cantidad": cantidad_a_devolver,
                    "direccion": self.salida.get('direccion'),
                    "detalles": "Devolución desde ReturnProductDialog"
                }
                try:
                    requests.post(f"{API_BASE_URL}/historial/registrar", json=movimiento)
                except requests.RequestException as e:
                    print(f"[WARN] No se pudo registrar el movimiento de entrada: {e}")

                if nueva_cantidad == 0:
                    self.mostrar_mensaje("Éxito", "Producto devuelto completamente y eliminado de salidas.", "success")
                else:
                    self.mostrar_mensaje("Éxito", f"Producto devuelto parcialmente. Nueva cantidad en salidas: {nueva_cantidad}", "success")

                self.accept()
            else:
                self.mostrar_mensaje("Error", "No se pudo devolver el producto.", "error")
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al devolver el producto: {str(e)}", "error")


    """
    Muestra un cuadro de mensaje personalizado según el tipo.

    Args:
        titulo (str): Título de la ventana del mensaje.
        mensaje (str): Contenido del mensaje.
        tipo (str): Tipo de mensaje ("success", "error", "confirm").

    Dependiendo del tipo se aplican estilos e íconos diferentes.
    """
    def mostrar_mensaje(self, titulo, mensaje, tipo):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)

        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.setStyleSheet(
            "QPushButton {"
            "background-color: #4CAF50; color: #FFFFFF; padding: 8px 16px; border-radius: 8px;"
            "}"
            "QPushButton:hover { background-color: #45A049; }"
        )
        btn_aceptar.clicked.connect(msg_box.accept)

        btn_si = QPushButton("Sí")
        btn_si.setStyleSheet(
            "QPushButton {"
            "background-color: #4CAF50; color: #FFFFFF; padding: 8px 16px; border-radius: 8px;"
            "}"
            "QPushButton:hover { background-color: #45A049; }"
        )

        btn_no = QPushButton("No")
        btn_no.setStyleSheet(
            "QPushButton {"
            "background-color: #E74C3C; color: #FFFFFF; padding: 8px 16px; border-radius: 8px;"
            "}"
            "QPushButton:hover { background-color: #C0392B; }"
        )

        if tipo == "success":
            msg_box.setIcon(QMessageBox.Information)
            msg_box.addButton(btn_aceptar, QMessageBox.AcceptRole)

        elif tipo == "error":
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.addButton(btn_aceptar, QMessageBox.AcceptRole)

        elif tipo == "confirm":
            msg_box.setIcon(QMessageBox.Question)
            msg_box.addButton(btn_si, QMessageBox.YesRole)
            msg_box.addButton(btn_no, QMessageBox.NoRole)

        msg_box.exec_()