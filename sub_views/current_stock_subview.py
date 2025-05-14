"""
Subvista de la aplicación que muestra el stock actual de una categoría específica de productos.

Esta clase permite visualizar los productos disponibles en una categoría mediante tarjetas interactivas.
Incluye funcionalidades de búsqueda con autocompletado, filtrado, exportación a Excel, y operaciones
CRUD como añadir, editar, eliminar o asignar productos. La información se obtiene dinámicamente desde
una API REST, y se presenta en una interfaz moderna y scrollable.

:param categoria: Categoría de productos a mostrar (ej. 'Habitaciones', 'Electrodomésticos').
:param parent: Widget padre opcional.
"""

import requests

from PyQt5.QtCore import Qt, QSize, QStringListModel

from PyQt5.QtGui import QFont, QIcon, QPixmap

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QGridLayout, QFrame, QMessageBox, QCompleter,
    QScrollArea, QSpacerItem, QSizePolicy, QLineEdit
)

# Imporatación de los cuadros de diálogos
from dialogs.add_product_dialog import AddProductDialog
from dialogs.assign_product_dialog import AssignProductDialog
from dialogs.edit_product_dialog import EditProductDialog
from dialogs.delete_product_dialog import DeleteProductDialog

# URL para la conexión con la base de datos
API_BASE_URL = "http://localhost:5000"


# Clase principal de la subvista de salida de stock
class CurrentStockSubview(QWidget):

    """
    Inicializa la subvista de stock actual para una categoría específica.

    :param categoria: Nombre de la categoría de productos (e.g., 'Habitaciones').
    :param parent: Widget padre opcional.
    """
    def __init__(self, categoria, parent=None):
        super().__init__(parent)
        self.categoria = categoria
        self.all_productos = []  # Lista para almacenar todos los productos
        self.suggestions = []  # Lista para almacenar sugerencias
        self.completer = QCompleter(self.suggestions, self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.initUI()
        self.load_stock_data()

    """
    Configura la interfaz de usuario: filtros, botones, área scrollable y conectores de señales.
    """
    def initUI(self):
        main_layout = QVBoxLayout(self)

        # FILTROS - INICIO
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)

        self.line_edit_filtro = QLineEdit()
        self.line_edit_filtro.setPlaceholderText("🔍 Buscar producto...")
        self.line_edit_filtro.setFixedWidth(250)
        self.line_edit_filtro.setStyleSheet("""
            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 2px solid #FFA500;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
            }
        """)
        self.line_edit_filtro.setCompleter(self.completer)  # Asigna el completer al line edit
        filter_layout.addWidget(self.line_edit_filtro)

        self.btn_filtrar = QPushButton(" Filtrar")
        self.btn_filtrar.setIcon(QIcon("images/b_filtrar.png"))
        self.btn_filtrar.setIconSize(QSize(18, 18))
        self.btn_filtrar.setFixedSize(140, 40)
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
        filter_layout.addWidget(self.btn_filtrar)
        filter_layout.addStretch()

        main_layout.addLayout(filter_layout)

        # Area srollable para las cards
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
        scroll_layout = QVBoxLayout(self.scroll_content)
        scroll_area.setWidget(self.scroll_content)

        # Layout para solo los cards
        self.grid_layout = QGridLayout()
        scroll_layout.addLayout(self.grid_layout)

        # Sección fija para los botones, para que no estén en el scroll
        btn_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()  
        self.btn_add = QPushButton(" Añadir Producto")  
        self.btn_assign = QPushButton(" Asignar Producto a Mobiliario")  
        self.btn_export = QPushButton(" Exportar a Excel")  

        self.btn_add.setIcon(QIcon("images/b_agregar.png"))  
        self.btn_assign.setIcon(QIcon("images/b_asignar.png"))  
        self.btn_export.setIcon(QIcon("images/b_ConvertirExcel.png"))  

        # Tamaño de lso iconos
        icon_size = QSize(30, 30) 
        self.btn_add.setIconSize(icon_size)  
        self.btn_assign.setIconSize(icon_size)  
        self.btn_export.setIconSize(icon_size)  

        self.btn_add.setFixedSize(200, 50)  
        self.btn_assign.setFixedSize(400, 50)  
        self.btn_export.setFixedSize(200, 50)  

        # Estilos de botones
        button_style = """
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
        
        self.btn_add.setStyleSheet(button_style)
        self.btn_assign.setStyleSheet(button_style)
        self.btn_export.setStyleSheet(button_style)

        self.btn_add.clicked.connect(self.add_product)
        self.btn_assign.clicked.connect(self.assign_product)
        self.btn_export.clicked.connect(self.export_to_excel)

        self.btn_filtrar.clicked.connect(self.filtrar_productos)
        self.line_edit_filtro.textChanged.connect(self.update_suggestions)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_assign)
        btn_layout.addWidget(self.btn_export)

        main_layout.addWidget(scroll_area)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)


    """
    Carga los productos desde la API REST, filtra por la categoría correspondiente
    y los almacena para su visualización en la UI.
    """
    def load_stock_data(self):
        response = requests.get(f"{API_BASE_URL}/productos/listar")
        if response.status_code == 200:
            productos = response.json()
            
            # Filtro por la categoría actual (habitaciones/electrodomesticos/Baño/ZonasComunes)
            productos_filtrados = [p for p in productos if p["categoria"] == self.categoria]

            # Almacena todos los productos filtrados
            self.all_productos = productos_filtrados
            self.populate_stock_cards(productos_filtrados)


    """
    Genera y muestra las tarjetas visuales de los productos en el grid.

    :param productos: Lista de productos que se deben representar visualmente.
    """
    def populate_stock_cards(self, productos):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        for i, producto in enumerate(productos):
            card = self.create_product_card(producto)
            self.grid_layout.addWidget(card, i // 3, i % 3)
        
        self.grid_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


    """
    Aplica un filtro al listado de productos basado en el texto introducido
    en el campo de búsqueda y actualiza la vista en consecuencia.
    """
    def filtrar_productos(self):
        filter_text = self.line_edit_filtro.text().strip().lower()

        if not filter_text:
            self.load_stock_data()  # Si no hay texto, cargar todos los productos
            return

        productos_filtrados = [
            producto for producto in self.all_productos
            if filter_text in producto['nombre'].lower()
        ]

        if productos_filtrados:
            self.populate_stock_cards(productos_filtrados)
        else:
            QMessageBox.information(self, "Información", "No se encontraron productos con este filtro.")


    """
    Actualiza la lista de sugerencias del autocompletado en base al texto actual.

    :param text: Texto actual escrito en el campo de búsqueda.
    """
    def update_suggestions(self, text):
        text = text.strip().lower()

        suggestions = [
            producto['nombre'] for producto in self.all_productos
            if text in producto['nombre'].lower()
        ]

        # Eliminar duplicados
        self.suggestions = list(dict.fromkeys(suggestions))

        # Actualizar el modelo del QCompleter
        model = QStringListModel(self.suggestions)
        self.completer.setModel(model)


    """
    Crea una tarjeta visual (QFrame) para representar la información de un producto.

    :param producto: Diccionario con los datos del producto.
    :return: Widget QFrame representando el producto.
    """
    def create_product_card(self, producto):
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
        
        # Iconos en círculos
        def create_icon_label(image_path):
            icon_label = QLabel()
            pixmap = QPixmap(image_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(pixmap)
            icon_label.setFixedSize(40, 40)
            icon_label.setStyleSheet("border-radius: 15px; background-color: #FFA500; padding: 3px;")
            return icon_label
        
        icon_nombre = create_icon_label("images/b_product_icon.png")
        icon_estado = create_icon_label("images/b_estado.png")
        icon_cantidad = create_icon_label("images/b_cantidad.png")
        
        # Etiquetas con iconos y texto mejorado
        label_nombre = QLabel(f" {producto['nombre']}")
        label_nombre.setFont(QFont("Arial", 12, QFont.Bold))
        
        label_estado = QLabel(f" Estado: {producto['estado']}")
        label_estado.setFont(QFont("Arial", 12))
        
        label_cantidad = QLabel(f" Stock: {producto['cantidad']}")
        label_cantidad.setFont(QFont("Arial", 12))
        
        # Layouts para alinear iconos y texto
        row_nombre = QHBoxLayout()
        row_nombre.addWidget(icon_nombre)
        row_nombre.addWidget(label_nombre)
        
        row_estado = QHBoxLayout()
        row_estado.addWidget(icon_estado)
        row_estado.addWidget(label_estado)
        
        row_cantidad = QHBoxLayout()
        row_cantidad.addWidget(icon_cantidad)
        row_cantidad.addWidget(label_cantidad)
        
        # Botones de acción 
        btn_edit = QPushButton(" Editar")
        btn_edit.setIcon(QIcon("images/b_edit.png"))
        btn_edit.setIconSize(QSize(22, 22))  
        btn_edit.setMinimumWidth(180)   
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #FFA500;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
                transition: 0.3s;
                width: 100%; /* Para que ocupe el ancho completo */
            }
            QPushButton:hover {
                background-color: #FF8C00;
                transform: scale(1.03);
            }
        """)
        btn_edit.clicked.connect(lambda: self.edit_product(producto))

        btn_delete = QPushButton(" Eliminar")
        btn_delete.setIcon(QIcon("images/b_basura.png"))
        btn_delete.setIconSize(QSize(22, 22))  
        btn_delete.setMinimumWidth(180)  
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
                padding: 5px;
                transition: 0.3s;
                width: 100%; /* Para que ocupe el ancho completo */
            }
            QPushButton:hover {
                background-color: #CC0000;
                transform: scale(1.03);
            }
        """)
        btn_delete.clicked.connect(lambda: self.delete_product(producto['id']))

        # Layout horizontal para mantenerlos en paralelo y al ancho completo del card
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_delete)
        btn_layout.setSpacing(10)  # Espacio moderado entre botones
        btn_layout.setAlignment(Qt.AlignCenter)

            
        layout.addLayout(row_nombre)
        layout.addLayout(row_estado)
        layout.addLayout(row_cantidad)
        layout.addLayout(btn_layout)
        
        return card
    

    """
    Abre el cuadro de diálogo para añadir un nuevo producto y recarga los datos si se confirma.
    """
    def add_product(self):
        dialog = AddProductDialog(self, categoria=self.categoria)  # Crea la ventana de añadir producto
        if dialog.exec_():  # Si el usuario confirma se recargam los datos
            self.load_stock_data()

    
    """
    Guarda un nuevo producto enviando los datos a la API.

    :param dialog: Diálogo actual desde donde se hace la operación.
    :param nombre: Nombre del producto.
    :param cantidad: Cantidad del producto (como string, debe ser un número).
    :param estado: Estado del producto (Nuevo, Usado, Dañado).
    """
    def save_product(self, dialog, nombre, cantidad, estado):
        if not nombre or not cantidad.isdigit():
            QMessageBox.warning(self, "Error", "Datos inválidos.")
            return
        
        response = requests.post(f"{API_BASE_URL}/productos/agregar", json={
            "nombre": nombre,
            "cantidad": cantidad,
            "estado": estado,
            "categoria": self.categoria
        })

        if response.status_code == 201:
            QMessageBox.information(self, "Éxito", "Producto añadido correctamente.")
            dialog.accept()
            self.load_stock_data()
        else:
            QMessageBox.critical(self, "Error", "No se pudo añadir el producto.")
    

    """
    Abre el cuadro de diálogo para editar un producto existente.

    :param producto: Diccionario con los datos del producto a editar.
    """
    def edit_product(self, producto):
        dialog = EditProductDialog(producto, self)
        if dialog.exec_():
            self.load_stock_data()  # Recarga los datos si se ha editado 


    """
    Abre el cuadro de diálogo para confirmar la eliminación de un producto.

    :param producto_id: ID del producto a eliminar.
    """
    def delete_product(self, producto_id):
        dialog = DeleteProductDialog(producto_id, self)
        if dialog.exec_():  # Si el usuario confirma se recargan los datos
            self.load_stock_data()


    """
    Abre el diálogo para asignar un producto a un inmueble y recarga los datos si se confirma.
    """
    def assign_product(self):
        dialog = AssignProductDialog(self, categoria=self.categoria)
        if dialog.exec_():  
            self.load_stock_data()


    """
    Realiza una petición a la API para exportar los datos del stock actual en un archivo Excel.
    """
    def export_to_excel(self):
        try:
            response = requests.get(f"{API_BASE_URL}/productos/exportar")
            if response.status_code == 200:
                with open("StockExport.xlsx", "wb") as f:
                    f.write(response.content)
                self.mostrar_mensaje("Éxito", "Exportación a Excel completada correctamente.", "info")
            else:
                self.mostrar_mensaje("Error", "No se pudo exportar a Excel.", "error")
        except Exception as e:
            self.mostrar_mensaje("Error", f"Error durante la exportación: {str(e)}", "error")

    
    """
    Muestra un cuadro de diálogo con un mensaje personalizado.

    :param titulo: Título de la ventana del mensaje.
    :param mensaje: Texto informativo a mostrar.
    :param tipo: Tipo de mensaje ('info', 'error', 'warning').
    """
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