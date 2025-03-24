import requests
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QPushButton, QHBoxLayout, 
    QRadioButton, QButtonGroup, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

API_BASE_URL = "http://localhost:5000"

class DeleteSelectedProductDialog(QDialog):
    def __init__(self, salida, parent=None):
        super().__init__(parent)
        self.salida = salida
        self.setWindowTitle("Eliminar Producto")
        self.setFixedSize(500, 500)
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

        # Botones de opción para eliminar total o parcial
        self.opcion_total = QRadioButton("Eliminar toda la cantidad")
        self.opcion_parcial = QRadioButton("Eliminar cantidad parcial")
        self.opcion_total.setChecked(True)  # Por defecto, eliminar toda la cantidad

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
        if enabled:
            self.cantidad_input.setEnabled(True)
        else:
            self.cantidad_input.setValue(self.salida['cantidad'])
            self.cantidad_input.setEnabled(False)

    def confirmar_eliminacion(self):
        confirmacion = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            "¿Estás seguro de que deseas eliminar este producto? Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            self.eliminar_producto()

    def eliminar_producto(self):
        if self.opcion_total.isChecked():
            cantidad_a_eliminar = self.salida['cantidad']  # Eliminar toda la cantidad
        else:
            cantidad_a_eliminar = self.cantidad_input.value()

        try:
            response = requests.delete(f"{API_BASE_URL}/productos/eliminar/{self.salida['id']}",
                                        json={'cantidad': cantidad_a_eliminar})
            if response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el producto.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar el producto: {str(e)}")