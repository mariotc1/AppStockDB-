from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QScrollArea,
    QFrame, QComboBox, QLineEdit, QMessageBox, QGridLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import requests

API_BASE_URL = "http://localhost:5000"

class HistorialMovimientosView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Filtros superiores
        filtros_layout = QHBoxLayout()
        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Todos", "Entrada", "Salida"])
        self.tipo_combo.setFixedWidth(150)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Buscar por producto...")
        self.nombre_input.setFixedWidth(250)

        self.btn_filtrar = QPushButton("Filtrar")
        self.btn_filtrar.setFixedHeight(30)
        self.btn_filtrar.clicked.connect(self.filtrar_movimientos)

        filtros_layout.addWidget(self.tipo_combo)
        filtros_layout.addWidget(self.nombre_input)
        filtros_layout.addWidget(self.btn_filtrar)
        filtros_layout.addStretch()
        layout.addLayout(filtros_layout)

        # Scroll invisible con estilo
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

        # Botón refrescar
        btn_layout = QHBoxLayout()
        self.btn_refresh = QPushButton(" Refrescar Datos")
        self.btn_refresh.setIcon(QIcon("images/refresh.png"))
        self.btn_refresh.setFixedSize(200, 50)
        self.btn_refresh.clicked.connect(self.cargar_movimientos)

        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)
        btn_layout.addWidget(self.btn_refresh)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.cargar_movimientos()

    def cargar_movimientos(self):
        response = requests.get(f"{API_BASE_URL}/historial/listar")
        if response.status_code == 200:
            movimientos = response.json()
            self.populate_movimiento_cards(movimientos)

    def populate_movimiento_cards(self, movimientos):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for i, mov in enumerate(movimientos):
            card = self.create_mov_card(mov)
            self.grid_layout.addWidget(card, i // 3, i % 3)

        self.grid_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_icon_label(self, image_path):
        icon_label = QLabel()
        pixmap = QPixmap(image_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setFixedSize(40, 40)
        icon_label.setStyleSheet("border-radius: 15px; background-color: #FFA500; padding: 3px;")
        return icon_label

    def create_mov_card(self, mov):
        tipo = mov['tipo_movimiento']
        color_border = "#27ae60" if tipo == "Entrada" else "#e74c3c"
        icon_path = "images/up.png" if tipo == "Entrada" else "images/down.png"
        titulo_text = "Devolución a Almacén" if tipo == "Entrada" else "Salida de Stock"

        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid {color_border};
                border-radius: 15px;
                padding: 15px;
            }}
            QFrame:hover {{
                background-color: rgba(255, 255, 255, 0.4);
            }}
        """)

        layout = QVBoxLayout(card)
        font_bold = QFont()
        font_bold.setPointSize(12)
        font_bold.setBold(True)

        layout_icon_title = QHBoxLayout()
        icon_label = self.create_icon_label(icon_path)
        title = QLabel(titulo_text)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout_icon_title.addWidget(icon_label)
        layout_icon_title.addWidget(title)
        layout.addLayout(layout_icon_title)

        row_producto = QHBoxLayout()
        producto_label = QLabel(f" Producto: {mov['producto']}")
        producto_label.setFont(font_bold)
        row_producto.addWidget(self.create_icon_label("images/product.png"))
        row_producto.addWidget(producto_label)

        row_cantidad = QHBoxLayout()
        cantidad_label = QLabel(f" Cantidad: {mov['cantidad']}")
        cantidad_label.setFont(font_bold)
        row_cantidad.addWidget(self.create_icon_label("images/cantidad.png"))
        row_cantidad.addWidget(cantidad_label)

        row_fecha = QHBoxLayout()
        fecha_label = QLabel(f" Fecha/Hora: {mov['fecha_movimiento']}")
        fecha_label.setFont(font_bold)
        row_fecha.addWidget(self.create_icon_label("images/calendar.png"))
        row_fecha.addWidget(fecha_label)

        layout.addLayout(row_producto)
        layout.addLayout(row_cantidad)
        layout.addLayout(row_fecha)

        if mov['direccion']:
            row_dir = QHBoxLayout()
            direccion_label = QLabel(f" Dirección: {mov['direccion']}")
            direccion_label.setFont(font_bold)
            row_dir.addWidget(self.create_icon_label("images/location.png"))
            row_dir.addWidget(direccion_label)
            layout.addLayout(row_dir)

        btn_eliminar = QPushButton(" Eliminar")
        btn_eliminar.setIcon(QIcon("images/basura.png"))
        btn_eliminar.setIconSize(QSize(22, 22))
        btn_eliminar.setFixedHeight(40)
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #CC0000;
            }
        """)
        btn_eliminar.clicked.connect(lambda: self.eliminar_movimiento(mov['id']))

        layout.addWidget(btn_eliminar)

        return card

    def eliminar_movimiento(self, mov_id):
        response = requests.delete(f"{API_BASE_URL}/historial/eliminar/{mov_id}")
        if response.status_code == 200:
            self.cargar_movimientos()
        else:
            QMessageBox.warning(self, "Error", "No se pudo eliminar el movimiento")

    def filtrar_movimientos(self):
        tipo_filtro = self.tipo_combo.currentText()
        nombre_filtro = self.nombre_input.text().lower()

        response = requests.get(f"{API_BASE_URL}/historial/listar")
        if response.status_code == 200:
            movimientos = response.json()
            if tipo_filtro != "Todos":
                movimientos = [m for m in movimientos if m['tipo_movimiento'] == tipo_filtro]
            if nombre_filtro:
                movimientos = [m for m in movimientos if nombre_filtro in m['producto'].lower()]
            self.populate_movimiento_cards(movimientos)