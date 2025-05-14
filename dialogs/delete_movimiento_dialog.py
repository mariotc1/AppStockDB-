"""
delete_movimiento_dialog.py

Define el cuadro de diálogo `DeleteMovimientoDialog`, que permite al usuario confirmar
la eliminación de un movimiento específico en el historial de la aplicación.

Características:
- Diálogo con diseño oscuro y estilizado.
- Incluye advertencias claras para evitar confusión.
- Conexión con la API REST vía método DELETE: `/historial/eliminar/<id>`
- Confirma el borrado al usuario o muestra mensajes de error.

Requiere:
    - requests
    - PyQt5
    - Imagen: `logoDB_Blanco.png`, `check.png`, `cancel.png`
"""

import requests

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, 
    QPushButton, QHBoxLayout, QMessageBox
)

# URL para la conexión con la API
API_BASE_URL = "http://localhost:5000"


class DeleteMovimientoDialog(QDialog):

    """
    Inicializa el cuadro de diálogo con el estilo visual y los botones de acción.

    Args:
        movimiento_id (int): ID del movimiento a eliminar.
        parent (QWidget, optional): Componente padre del diálogo (opcional).
    """
    def __init__(self, movimiento_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Movimiento")
        self.setFixedSize(420, 310)

        # estilo del cuadro de diálogo
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

        self.movimiento_id = movimiento_id

        layout = QVBoxLayout(self)

        logo = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(100, 100, Qt.KeepAspectRatio)
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title_label = QLabel("\u00bfDeseas eliminar este movimiento?")
        title_label.setFont(QFont("Arial", 16))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; margin-bottom: 10px;")
        layout.addWidget(title_label)

        warning_label = QLabel("Este registro no volver\u00e1 a mostrarse en el historial, pero no elimina el producto original.")
        warning_label.setWordWrap(True)
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("color: orange; font-size: 14px;")
        layout.addWidget(warning_label)

        self.btn_confirm = QPushButton("Confirmar Eliminaci\u00f3n")
        self.btn_confirm.setIcon(QIcon("images/check.png"))
        self.btn_confirm.clicked.connect(self.delete_movimiento)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setIcon(QIcon("images/cancel.png"))
        self.btn_cancel.setObjectName("btn_cancel")
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_confirm)

        layout.addLayout(btn_layout)

    """
    Envía una petición DELETE a la API para eliminar el movimiento especificado.

    - Si la operación es exitosa, muestra un mensaje informativo y cierra el diálogo.
    - Si ocurre un error (status != 200 o excepción), muestra un mensaje de error.

    Endpoint usado:
        DELETE /historial/eliminar/<movimiento_id>
    """
    def delete_movimiento(self):
        try:
            response = requests.delete(f"{API_BASE_URL}/historial/eliminar/{self.movimiento_id}")
            if response.status_code == 200:
                QMessageBox.information(self, "\u00c9xito", "Movimiento eliminado correctamente.")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el movimiento.\nC\u00f3digo: {response.status_code}")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error de conexi\u00f3n", f"No se pudo conectar con el servidor:\n{str(e)}")