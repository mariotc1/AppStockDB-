import requests

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
    QPushButton, QScrollArea, QFrame, QComboBox, 
    QLineEdit, QMessageBox, QGridLayout, QSpacerItem, QSizePolicy
)

from dialogs.delete_movimiento_dialog import DeleteMovimientoDialog

API_BASE_URL = "http://localhost:5000"

# Clase de la subvista de Historial de movmientos
class HistorialMovimientosView(QWidget):
    def __init__(self, categoria, parent=None):
        super().__init__(parent)
        self.categoria = categoria
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Filtros
        filtros_layout = QHBoxLayout()
        filtros_layout.setSpacing(15)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Todos", "Entrada", "Salida"])
        self.tipo_combo.setFixedWidth(180)
        self.tipo_combo.setStyleSheet("""
            QComboBox {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #FFA500;
                border-radius: 10px;
                padding: 8px 30px 8px 8px;
                font-size: 14px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left: 1px solid #FFA500;
            }
            QComboBox::down-arrow {
                image: url(images/desplegable.png);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                selection-background-color: #FFA500;
                font-size: 14px;
            }
        """)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("🔍 Buscar por producto...")
        self.nombre_input.setFixedWidth(250)
        self.nombre_input.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #FFA500;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
        """)

        self.btn_filtrar = QPushButton(" Filtrar")
        self.btn_filtrar.setIcon(QIcon("images/filtrar.png"))
        self.btn_filtrar.setIconSize(QSize(18, 18))
        self.btn_filtrar.setFixedSize(140, 40)
        self.btn_filtrar.clicked.connect(self.filtrar_movimientos)
        self.btn_filtrar.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)

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
        scroll_layout = QVBoxLayout(self.scroll_content)  # NUEVO layout vertical contenedor

        self.grid_layout = QGridLayout()
        scroll_layout.addLayout(self.grid_layout)  # Mete el grid dentro

        scroll_area.setWidget(self.scroll_content)

        layout.addWidget(scroll_area)

        # Botón refrescar y exportar a excel
        btn_layout = QHBoxLayout()

        self.btn_refresh = QPushButton(" Refrescar Datos")
        self.btn_refresh.setIcon(QIcon("images/refrescar.png"))
        self.btn_refresh.setFixedSize(200, 50)
        self.btn_refresh.clicked.connect(self.cargar_movimientos)

        self.btn_export = QPushButton(" Exportar a Excel")
        self.btn_export.setIcon(QIcon("images/ConvertirExcel.png"))
        self.btn_export.setFixedSize(200, 50)
        self.btn_export.clicked.connect(self.exportar_excel)

        self.btn_refresh.setStyleSheet("""
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
        """)

        self.btn_export.setStyleSheet("""
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
        """)

        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_export)
        layout.addLayout(btn_layout)


        self.setLayout(layout)
        self.cargar_movimientos()

    def cargar_movimientos(self):
        response = requests.get(f"{API_BASE_URL}/historial/listar", params={"categoria": self.categoria})
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
        titulo_text = "DEVOLUCIÓN A ALMACÉN" if tipo == "Entrada" else "SALIDA DEL ALMACÉN"

        card = QFrame()
        card.setMaximumWidth(590)
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
        card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout = QVBoxLayout(card)
        font_bold = QFont()
        font_bold.setPointSize(12)
        font_bold.setBold(True)

        layout_icon_title = QHBoxLayout()
        icon_label = self.create_icon_label(icon_path)
        title = QLabel(titulo_text)
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout_icon_title.addWidget(icon_label)
        layout_icon_title.addWidget(title)
        layout.addLayout(layout_icon_title)

        row_producto = QHBoxLayout()
        producto_label = QLabel(f" Producto: {mov['producto']}")
        producto_label.setFont(QFont("Arial", 12))
        row_producto.addWidget(self.create_icon_label("images/product.png"))
        row_producto.addWidget(producto_label)

        row_cantidad = QHBoxLayout()
        cantidad_label = QLabel(f" Cantidad: {mov['cantidad']}")
        cantidad_label.setFont(QFont("Arial", 12))
        row_cantidad.addWidget(self.create_icon_label("images/cantidad.png"))
        row_cantidad.addWidget(cantidad_label)

        row_fecha = QHBoxLayout()
        fecha_label = QLabel(f" Fecha/Hora: {mov['fecha_movimiento']}")
        fecha_label.setFont(QFont("Arial", 12))
        row_fecha.addWidget(self.create_icon_label("images/calendar.png"))
        row_fecha.addWidget(fecha_label)

        layout.addLayout(row_producto)
        layout.addLayout(row_cantidad)
        layout.addLayout(row_fecha)

        if mov['direccion']:
            row_dir = QHBoxLayout()
            direccion_label = QLabel(f" Dirección: {mov['direccion']}")
            direccion_label.setFont(QFont("Arial", 12))
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
        dialog = DeleteMovimientoDialog(mov_id, self, categoria=self.categoria)
        if dialog.exec_():
            self.cargar_movimientos()

    def filtrar_movimientos(self):
        tipo_filtro = self.tipo_combo.currentText()
        nombre_filtro = self.nombre_input.text().lower()

        response = requests.get(f"{API_BASE_URL}/historial/listar", params={"categoria": self.categoria})
        if response.status_code == 200:
            movimientos = response.json()
            if tipo_filtro != "Todos":
                movimientos = [m for m in movimientos if m['tipo_movimiento'] == tipo_filtro]
            if nombre_filtro:
                movimientos = [m for m in movimientos if nombre_filtro in m['producto'].lower()]
            self.populate_movimiento_cards(movimientos)

    def exportar_excel(self):
        try:
            response = requests.get(f"{API_BASE_URL}/historial/exportar")
            if response.status_code == 200:
                with open("HistorialMovimientos.xlsx", "wb") as f:
                    f.write(response.content)
                self.mostrar_mensaje("Éxito", "Historial exportado correctamente a 'HistorialMovimientos.xlsx'", "info")
            else:
                QMessageBox.warning(self, "Error", "No se pudo exportar el historial.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al exportar: {str(e)}")

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)

        # Icono según el tipo
        if tipo == "info":
            msg_box.setIcon(QMessageBox.Information)
        elif tipo == "error":
            msg_box.setIcon(QMessageBox.Critical)
        elif tipo == "warning":
            msg_box.setIcon(QMessageBox.Warning)

        # Personalización visual elegante
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
                font-size: 14px;
            }
            QLabel {
                color: black;
            }
            QPushButton {
                background-color: #FFA500;
                color: black;
                padding: 6px 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FF8C00;
            }
        """)

        msg_box.exec_()