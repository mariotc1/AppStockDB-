from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QMessageBox,
    QFrame, QScrollArea, QSpacerItem, QSizePolicy, QCheckBox, QDialog, QLineEdit, QFormLayout
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import requests

API_BASE_URL = "http://localhost:5000"

class SalidaStockView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.load_salida_data()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Área scrollable con scroll invisible
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                width: 0px;
            }
            QScrollBar:horizontal {
                height: 0px;
            }
        """)

        self.scroll_content = QWidget()
        self.grid_layout = QGridLayout(self.scroll_content)
        scroll_area.setWidget(self.scroll_content)

        layout.addWidget(scroll_area)

        # Estilo de botones integrado directamente
        self.button_style = """
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

        # Botones de gestión en lote
        btn_layout = QHBoxLayout()
        self.btn_devolver_lote = QPushButton(" Devolver Seleccionados")
        self.btn_delete_lote = QPushButton(" Eliminar Seleccionados")

        self.btn_devolver_lote.setIcon(QIcon("images/return.png"))
        self.btn_delete_lote.setIcon(QIcon("images/delete.png"))

        self.btn_devolver_lote.setStyleSheet(self.button_style)
        self.btn_delete_lote.setStyleSheet(self.button_style)

        # Establece el tamaño del ícono  
        icon_size = QSize(30, 30)  # Ajusta el tamaño aquí (anchura, altura)  
        self.btn_devolver_lote.setIconSize(icon_size)  
        self.btn_delete_lote.setIconSize(icon_size)  

        self.btn_devolver_lote.setFixedSize(260, 50)
        self.btn_delete_lote.setFixedSize(260, 50)

        self.btn_devolver_lote.clicked.connect(self.devolver_seleccionados)
        self.btn_delete_lote.clicked.connect(self.eliminar_seleccionados)

        btn_layout.addWidget(self.btn_devolver_lote)
        btn_layout.addWidget(self.btn_delete_lote)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def load_salida_data(self):
        response = requests.get(f"{API_BASE_URL}/salidas/listar")
        if response.status_code == 200:
            salidas = response.json()
            if salidas:
                self.populate_salida_cards(salidas)

    def populate_salida_cards(self, salidas):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.checkboxes = []  # Para almacenar los checkboxes

        for i, salida in enumerate(salidas):
            card = self.create_salida_card(salida)
            self.grid_layout.addWidget(card, i // 3, i % 3)

        self.grid_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_salida_card(self, salida):
        def create_icon_label(image_path):
            icon_label = QLabel()
            pixmap = QPixmap(image_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(40, 40)
            icon_label.setStyleSheet("border-radius: 15px; background-color: #FFA500; padding: 3px;")
            return icon_label

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

        checkbox = QCheckBox()
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 25px;
                height: 25px;
            }
            QCheckBox::indicator:checked {
                background-color: #FFA500;
                border: 2px solid #FF8C00;
                border-radius: 5px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #B0B0B0;
                border-radius: 5px;
            }
        """)
        self.checkboxes.append((checkbox, salida))

        layout_checkbox = QHBoxLayout()
        layout_checkbox.addWidget(checkbox)
        layout_checkbox.addStretch()

        font_normal = QFont()
        font_normal.setPointSize(12)

        font_bold = QFont()
        font_bold.setPointSize(12)
        font_bold.setBold(True)

        row_direccion = QHBoxLayout()
        direccion_label = QLabel(f" Dirección: {salida['direccion']}")
        direccion_label.setFont(font_bold)
        row_direccion.addWidget(create_icon_label("images/location.png"))
        row_direccion.addWidget(direccion_label)

        row_producto = QHBoxLayout()
        producto_label = QLabel(f" Producto: {salida['producto']}")
        producto_label.setFont(font_normal)
        row_producto.addWidget(create_icon_label("images/product.png"))
        row_producto.addWidget(producto_label)

        row_cantidad = QHBoxLayout()
        cantidad_label = QLabel(f" Cantidad: {salida['cantidad']}")
        cantidad_label.setFont(font_normal)
        row_cantidad.addWidget(create_icon_label("images/cantidad.png"))
        row_cantidad.addWidget(cantidad_label)

        row_fecha = QHBoxLayout()
        fecha_label = QLabel(f" Fecha/Hora: {salida['fecha_salida']}")
        fecha_label.setFont(font_normal)
        row_fecha.addWidget(create_icon_label("images/calendar.png"))
        row_fecha.addWidget(fecha_label)

        btn_layout = QHBoxLayout()
        
        btn_devolver = QPushButton(" Devolver")
        btn_devolver.setIcon(QIcon("images/return.png"))
        btn_devolver.setIconSize(QSize(22, 22))
        btn_devolver.setMinimumWidth(180)
        btn_devolver.setFixedHeight(40)
        btn_devolver.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
                transition: 0.3s;
                width: 100%;
            }
            QPushButton:hover {
                background-color: #FF8C00;
                transform: scale(1.03);
            }
        """)

        btn_delete = QPushButton(" Eliminar")
        btn_delete.setIcon(QIcon("images/basura.png"))
        btn_delete.setIconSize(QSize(22, 22))
        btn_delete.setMinimumWidth(180)
        btn_delete.setFixedHeight(40)
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
                transition: 0.3s;
                width: 100%;
            }
            QPushButton:hover {
                background-color: #CC0000;
                transform: scale(1.03);
            }
        """)

        # Layout horizontal para que estén en paralelo
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_devolver)
        btn_layout.addWidget(btn_delete)
        btn_layout.setSpacing(10)  # Espaciado entre botones
        btn_layout.setAlignment(Qt.AlignCenter)


        layout.addLayout(layout_checkbox)
        layout.addLayout(row_direccion)
        layout.addLayout(row_producto)
        layout.addLayout(row_cantidad)
        layout.addLayout(row_fecha)
        layout.addLayout(btn_layout)  

        return card


    # Dialogo personalizado para devolver producto
    def show_return_dialog(self, salida):
        dialog = QDialog(self)
        dialog.setWindowTitle("Devolver Producto")
        layout = QFormLayout(dialog)

        cantidad_input = QLineEdit()
        layout.addRow("Cantidad a devolver:", cantidad_input)

        btn_confirmar = QPushButton("Confirmar")
        btn_confirmar.clicked.connect(lambda: self.devolver_producto(salida['id'], cantidad_input.text(), dialog))
        layout.addWidget(btn_confirmar)

        dialog.exec_()

    def devolver_producto(self, salida_id, cantidad, dialog):
        try:
            cantidad = int(cantidad)
            response = requests.put(f"{API_BASE_URL}/salidas/devolver/{salida_id}", json={'cantidad': cantidad})
            if response.status_code == 200:
                QMessageBox.information(self, "Éxito", "Producto devuelto correctamente.")
                dialog.accept()
                self.load_salida_data()
            else:
                QMessageBox.critical(self, "Error", "No se pudo devolver el producto.")
        except ValueError:
            QMessageBox.warning(self, "Error", "Cantidad inválida.")

    # Dialogo personalizado para eliminar producto
    def show_delete_dialog(self, salida):
        respuesta = QMessageBox.question(
            self,
            "Eliminar Producto",
            f"¿Seguro que quieres eliminar el producto '{salida['producto']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.eliminar_producto(salida['id'])

    def eliminar_producto(self, salida_id):
        response = requests.delete(f"{API_BASE_URL}/productos/eliminar/{salida_id}")
        if response.status_code == 200:
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente.")
            self.load_salida_data()
        else:
            QMessageBox.critical(self, "Error", "No se pudo eliminar el producto.")

    def devolver_seleccionados(self):
        for checkbox, salida in self.checkboxes:
            if checkbox.isChecked():
                self.show_return_dialog(salida)

    def eliminar_seleccionados(self):
        for checkbox, salida in self.checkboxes:
            if checkbox.isChecked():
                self.eliminar_producto(salida['id'])