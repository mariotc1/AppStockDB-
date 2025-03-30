import requests
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QHBoxLayout, 
    QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

API_BASE_URL = "http://localhost:5000"

class DeleteSelectedProductDialog(QDialog):
    def __init__(self, salida, parent=None, categoria=None):
        super().__init__(parent)
        self.salida = salida
        self.categoria = categoria
        self.setWindowTitle("Eliminar Producto")
        self.setFixedSize(500, 500)
        self.setStyleSheet(
            "QDialog {"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2C3E50, stop:1 #1F1F1F);"
            "border-radius: 20px;"
            "} "
            "QLabel { color: #FFFFFF; font-size: 18px; } "
            "QRadioButton { color: #FFFFFF; font-size: 16px; } "
            "QPushButton#btn_confirmar { background-color: #27AE60; color: #FFFFFF; border-radius: 10px; padding: 10px; font-size: 16px; } "
            "QPushButton#btn_confirmar:hover { background-color: #229954; } "
            "QPushButton#btn_cancelar { background-color: #E74C3C; color: #FFFFFF; border-radius: 10px; padding: 10px; font-size: 16px; } "
            "QPushButton#btn_cancelar:hover { background-color: #C0392B; } "
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
        title_label = QLabel(f"Eliminar '{salida['producto']}'")
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Advertencia
        warning_label = QLabel("⚠️ ¡Advertencia! Esta acción es irreversible.\nEl producto se perderá permanentemente del sistema.")
        warning_label.setFont(QFont("Arial", 12, QFont.Bold))
        warning_label.setStyleSheet("color: #E74C3C;")
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label)

        cantidad_total = salida['cantidad']
        self.cantidad_input = QSpinBox()
        self.cantidad_input.setMinimum(1)
        self.cantidad_input.setMaximum(cantidad_total)
        self.cantidad_input.setValue(cantidad_total)

        # Opciones de eliminación
        self.opcion_total = QRadioButton("Eliminar toda la cantidad")
        self.opcion_parcial = QRadioButton("Eliminar cantidad parcial")
        self.opcion_total.setChecked(True)

        self.opcion_group = QButtonGroup(self)
        self.opcion_group.addButton(self.opcion_total)
        self.opcion_group.addButton(self.opcion_parcial)

        self.opcion_total.toggled.connect(lambda: self.toggle_cantidad(False))
        self.opcion_parcial.toggled.connect(lambda: self.toggle_cantidad(True))

        layout.addWidget(self.opcion_total)
        layout.addWidget(self.opcion_parcial)
        layout.addWidget(QLabel("Cantidad a eliminar:"))
        layout.addWidget(self.cantidad_input)

        # Botones de Confirmar y Cancelar
        btn_layout = QHBoxLayout()
        btn_confirmar = QPushButton(" Confirmar")
        btn_confirmar.setObjectName("btn_confirmar")
        btn_confirmar.setIcon(QIcon("images/check.png"))
        btn_confirmar.clicked.connect(self.confirmar_eliminacion)

        btn_cancelar = QPushButton(" Cancelar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.setIcon(QIcon("images/cancel.png"))
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_confirmar)

        layout.addLayout(btn_layout)

    def toggle_cantidad(self, enabled):
        self.cantidad_input.setEnabled(enabled)

    def confirmar_eliminacion(self):
        self.mostrar_mensaje(
            "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer.",
            "confirm"
        )

    def eliminar_producto(self):
        if self.opcion_total.isChecked():
            cantidad_a_eliminar = self.salida['cantidad']
        else:
            cantidad_a_eliminar = self.cantidad_input.value()

        try:
            response = requests.delete(
                f"{API_BASE_URL}/salidas/eliminar/{self.salida['id']}",
                json={'cantidad': cantidad_a_eliminar}
            )

            if response.status_code == 200:
                movimiento = {
                    "producto_id": self.salida['producto_id'],  # ¡IMPORTANTE! Asegúrate que tienes el campo correcto.
                    "tipo_movimiento": "Salida",
                    "cantidad": cantidad_a_eliminar,
                    "direccion": self.salida.get("direccion", "Sin dirección"),
                    "detalles": "Eliminación manual de producto desde DeleteSelectedProductDialog"
                }
                try:
                    requests.post(f"{API_BASE_URL}/historial/registrar", json=movimiento)
                except requests.RequestException as e:
                    print(f"[WARN] No se pudo registrar el movimiento de eliminación: {e}")

                self.mostrar_mensaje("Éxito", "Producto eliminado correctamente.", "success")
                self.accept()
            else:
                self.mostrar_mensaje("Error", "No se pudo eliminar el producto.", "error")
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al eliminar el producto: {str(e)}", "error")

    def mostrar_mensaje(self, titulo, mensaje, tipo):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)

        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.setStyleSheet("background-color: #3498DB; color: #FFFFFF; padding: 8px 16px; border-radius: 8px;")
        btn_aceptar.clicked.connect(msg_box.accept)

        btn_si = QPushButton("Sí")
        btn_si.setStyleSheet("background-color: #27AE60; color: #FFFFFF; padding: 8px 16px; border-radius: 8px;")

        btn_no = QPushButton("No")
        btn_no.setStyleSheet("background-color: #E74C3C; color: #FFFFFF; padding: 8px 16px; border-radius: 8px;")

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
            btn_si.clicked.connect(self.eliminar_producto)

        msg_box.exec_()