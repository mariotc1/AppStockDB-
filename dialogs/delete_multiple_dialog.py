from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpinBox, QScrollArea, QWidget, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class DeleteMultipleDialog(QDialog):
    def __init__(self, salidas, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Productos Seleccionados")
        self.setFixedSize(600, 600)
        self.salidas = salidas
        self.resultados = {}  # salida['id']: cantidad a eliminar

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2C3E50, stop:1 #1F1F1F);
                border-radius: 20px;
            }
            QLabel { color: #FFFFFF; font-size: 16px; }
            QSpinBox {
                background-color: #FFFFFF;
                color: #000000;
                padding: 6px;
                border-radius: 8px;
                font-size: 18px;
            }
            QPushButton {
                font-size: 16px;
                padding: 8px 16px;
                border-radius: 10px;
            }
            QPushButton#btn_confirmar {
                background-color: #27AE60;
                color: #FFFFFF;
            }
            QPushButton#btn_confirmar:hover {
                background-color: #229954;
            }
            QPushButton#btn_cancelar {
                background-color: #E74C3C;
                color: #FFFFFF;
            }
            QPushButton#btn_cancelar:hover {
                background-color: #C0392B;
            }
        """
        )

        layout = QVBoxLayout(self)

        # Logo superior
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(90, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Instrucciones
        title = QLabel("Selecciona la cantidad a eliminar para cada producto:")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        self.spinboxes = {}

        for salida in self.salidas:
            container = QHBoxLayout()
            label = QLabel(f"{salida['producto']} ({salida['cantidad']} uds)")
            label.setFont(QFont("Arial", 14))
            label.setMinimumWidth(300)

            spin = QSpinBox()
            spin.setRange(1, salida['cantidad'])
            spin.setValue(salida['cantidad'])
            self.spinboxes[salida['id']] = spin

            container.addWidget(label)
            container.addWidget(spin)
            scroll_layout.addLayout(container)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        btn_layout = QHBoxLayout()
        btn_cancelar = QPushButton(" Cancelar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.setIcon(QIcon("images/cancel.png"))
        btn_cancelar.clicked.connect(self.reject)

        btn_confirmar = QPushButton(" Confirmar")
        btn_confirmar.setObjectName("btn_confirmar")
        btn_confirmar.setIcon(QIcon("images/check.png"))
        btn_confirmar.clicked.connect(self.confirmar)

        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_confirmar)
        layout.addLayout(btn_layout)

    def confirmar(self):
        for salida in self.salidas:
            cantidad = self.spinboxes[salida['id']].value()
            self.resultados[salida['id']] = cantidad
        self.accept()