"""
Vista principal de la sección 'Habitaciones' en la aplicación de gestión de stock.

Integra múltiples subvistas relacionadas con el mobiliario de habitaciones:
- Visualización del stock actual
- Gestión de salidas de stock
- Historial de movimientos

También incluye un botón de acceso al chatbot para asistencia contextual.

:param categoria: Categoría de productos a gestionar (habitaciones).
:param parent: Widget padre opcional.
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QStackedWidget, QPushButton, QLabel,
)

# Importación del chatbot
from chatbot.chat_popup import ChatPopup  

# Importación de las subvistas
from sub_views.current_stock_subview import CurrentStockSubview
from sub_views.stock_removal_subview import StockRemovalSubview
from sub_views.transaction_history_subview import TransactionHistorySubview

# URL para la conexión con la api rest
API_BASE_URL = "http://localhost:5000"

# Clase principal de la svista de Habitaciones
class RoomView(QWidget):

    """
    Inicializa la vista RoomView con la categoría 'Habitaciones' y construye la interfaz principal.

    :param categoria: Categoría a la que pertenece la vista ('Habitaciones').
    :param parent: Widget padre opcional.
    """
    def __init__(self, categoria, parent=None):
        super().__init__(parent)
        self.categoria = categoria
        self.chat_popup = None
        self.initUI()
    
    
    """
    Construye la interfaz de usuario con título, menú de navegación por iconos,
    contenedor de subvistas (stock, salidas, historial) y botón flotante del chatbot.
    """
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        title = QLabel("Mobiliario de Habitaciones")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        main_layout.addWidget(title)
        
        icon_menu = QWidget()
        icon_menu.setFixedHeight(100)
        icon_menu_layout = QHBoxLayout(icon_menu)
        icon_menu_layout.setSpacing(30)
        
        icons = [
            ("b_stock.png", "Stock Actual"),
            ("b_salida.png", "Salida de Stock"),
            ("b_historial.png", "Historial de movimientos")
        ]

        self.icon_buttons = []
        
        for i, (icon, text) in enumerate(icons):
            btn = QPushButton()
            btn.setIcon(QIcon(f"images/{icon}"))
            btn.setIconSize(QSize(50, 50))
            btn.setFixedSize(70, 70)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 35px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 165, 0, 0.3);
                }
            """)
            btn.clicked.connect(lambda _, idx=i: self.change_tab(idx))
            
            label = QLabel(text)
            label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
            
            icon_menu_layout.addWidget(btn)
            icon_menu_layout.addWidget(label)
            self.icon_buttons.append(btn)
        
        icon_menu_layout.addStretch()
        main_layout.addWidget(icon_menu)
        
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background: transparent;")
        
        self.stock_widget = CurrentStockSubview(categoria=self.categoria)
        self.salida_widget = StockRemovalSubview(categoria=self.categoria)
        self.historial_widget = TransactionHistorySubview(categoria=self.categoria)
        
        self.content_stack.addWidget(self.stock_widget)
        self.content_stack.addWidget(self.salida_widget)
        self.content_stack.addWidget(self.historial_widget)
        
        main_layout.addWidget(self.content_stack, 1)
        
        self.chatbot_btn = QPushButton(self)
        self.chatbot_btn.setIcon(QIcon("images/chatbot_icon.png"))
        self.chatbot_btn.setIconSize(QSize(40, 40))
        self.chatbot_btn.setFixedSize(60, 60)
        self.chatbot_btn.setStyleSheet("""
            QPushButton {
                background-color: #2C3E50;
                border: 2px solid #ECF0F1;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #34495E;
            }
        """)
        self.chatbot_btn.clicked.connect(self.toggleChatPopup)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        self.positionChatbotButton()
    

    """
    Calcula y establece la posición del botón del chatbot en la esquina inferior derecha.
    Se llama inicialmente y también en cada redimensionado de la ventana.
    """
    def positionChatbotButton(self):
        margin = 20
        self.chatbot_btn.move(
            self.width() - self.chatbot_btn.width() - margin,
            self.height() - self.chatbot_btn.height() - margin
        )
    

    """
    Cambia la subvista activa del `QStackedWidget` según el índice seleccionado.

    :param index: Índice de la vista a mostrar (0: stock, 1: salida, 2: historial).
    """
    def change_tab(self, index):
        self.content_stack.setCurrentIndex(index)
    

    """
    Cambia la subvista activa del `QStackedWidget` según el índice seleccionado.

    :param index: Índice de la vista a mostrar (0: stock, 1: salida, 2: historial).
    """
    def toggleChatPopup(self):
        if self.chat_popup and self.chat_popup.isVisible():
            self.chat_popup.close()
            self.chat_popup = None
        else:
            self.chat_popup = ChatPopup(self.chatbot_btn, self)
            self.chat_popup.show()
    

    """
    Evento de redimensionamiento. Reposiciona el botón del chatbot automáticamente.

    :param event: Evento de redimensionamiento de la ventana.
    """
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.positionChatbotButton()