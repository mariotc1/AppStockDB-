from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpinBox, QScrollArea, QWidget, QMessageBox, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class DeleteMultipleDialog(QDialog):
    def __init__(self, salidas, parent=None, categoria=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Productos Seleccionados")
        self.setFixedSize(600, 600)
        self.salidas = salidas
        self.categoria = categoria
        self.resultados = {}

        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2C3E50, stop:1 #1F1F1F);
                border-radius: 20px;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
            }
            QSpinBox {
                background-color: #FFFFFF;
                color: #000000;
                padding: 10px;
                border-radius: 8px;
                font-size: 20px;
                min-width: 100px;
                min-height: 35px;
            }
            QPushButton {
                font-size: 18px;
                padding: 14px 0;
                border-radius: 10px;
                font-weight: bold;
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
        """)

        layout = QVBoxLayout(self)

        # Logo superior
        logo_label = QLabel()
        logo_pixmap = QPixmap("images/logoDB_Blanco.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Título
        title = QLabel("Selecciona la cantidad a eliminar para cada producto:")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Advertencia
        warning = QLabel("⚠️ ¡Advertencia! Esta acción es irreversible.\nLos productos seleccionados se perderán permanentemente del sistema.")
        warning.setFont(QFont("Arial", 12, QFont.Bold))
        warning.setStyleSheet("color: #E74C3C;")
        warning.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning)

        # Zona scroll con los productos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        self.spinboxes = {}

        for salida in self.salidas:
            row_layout = QHBoxLayout()
            label = QLabel(f"{salida['producto']} ({salida['cantidad']} unidad/es)")
            label.setFont(QFont("Arial", 16, QFont.Bold))

            spin = QSpinBox()
            spin.setRange(1, salida['cantidad'])
            spin.setValue(salida['cantidad'])
            self.spinboxes[salida['id']] = spin

            row_layout.addWidget(label)
            row_layout.addStretch()
            row_layout.addWidget(spin)
            scroll_layout.addLayout(row_layout)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        # Botones inferior: 50% - 50%
        btn_layout = QHBoxLayout()
        btn_cancelar = QPushButton("  Cancelar")
        btn_cancelar.setObjectName("btn_cancelar")
        btn_cancelar.setIcon(QIcon("images/cancel.png"))
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        btn_confirmar = QPushButton("  Confirmar")
        btn_confirmar.setObjectName("btn_confirmar")
        btn_confirmar.setIcon(QIcon("images/check.png"))
        btn_confirmar.clicked.connect(self.confirmar)
        btn_confirmar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_confirmar)
        layout.addLayout(btn_layout)

    def confirmar(self):
        # Confirmación visual antes de aceptar
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmar Eliminación")
        msg_box.setText("¿Estás seguro de que deseas eliminar los productos seleccionados?\nEsta acción no se puede deshacer.")
        msg_box.setIcon(QMessageBox.Warning)

        btn_si = QPushButton("Sí")
        btn_si.setStyleSheet("background-color: #27AE60; color: white; padding: 8px 16px; border-radius: 8px;")
        btn_no = QPushButton("No")
        btn_no.setStyleSheet("background-color: #E74C3C; color: white; padding: 8px 16px; border-radius: 8px;")

        msg_box.addButton(btn_si, QMessageBox.YesRole)
        msg_box.addButton(btn_no, QMessageBox.NoRole)

        btn_si.clicked.connect(self.ejecutar_confirmacion)
        msg_box.exec_()

    def ejecutar_confirmacion(self):
        for salida in self.salidas:
            cantidad = self.spinboxes[salida['id']].value()
            self.resultados[salida['id']] = cantidad
        self.accept()
