from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QLabel,
    QGraphicsDropShadowEffect, QScrollArea, QGridLayout, QFrame, QSizePolicy, QSpacerItem, QLineEdit
)
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap
from PyQt5.QtCore import Qt, QSize
import requests

# Importa sub vistas
from sub_views.stockActual_view import StockActualView
from sub_views.salidaStock_view import SalidaStockView
from sub_views.historialMovimientos_view import HistorialMovimientosView
from chatbot.chat_popup import ChatPopup  

API_BASE_URL = "http://localhost:5000"

class HabitacionesView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_popup = None
        self.initUI()
    
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
            ("en_stock.png", "Stock Actual"),
            ("salida.png", "Salida de Stock"),
            ("historial.png", "Historial de movimientos")
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
        
        self.stock_widget = StockActualView()
        self.salida_widget = SalidaStockView()
        self.historial_widget = HistorialMovimientosView()
        
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
    
    def positionChatbotButton(self):
        margin = 20
        self.chatbot_btn.move(
            self.width() - self.chatbot_btn.width() - margin,
            self.height() - self.chatbot_btn.height() - margin
        )
    
    def change_tab(self, index):
        self.content_stack.setCurrentIndex(index)
    
    def toggleChatPopup(self):
        if self.chat_popup and self.chat_popup.isVisible():
            self.chat_popup.close()
            self.chat_popup = None
        else:
            self.chat_popup = ChatPopup(self.chatbot_btn, self)
            self.chat_popup.show()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.positionChatbotButton()