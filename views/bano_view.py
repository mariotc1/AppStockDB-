from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton, QLabel,
    QGraphicsDropShadowEffect, QFrame
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize

from chatbot.chat_popup import ChatPopup  

class BanoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_popup = None
        self.initUI()
        
    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título centrado en negrita
        title = QLabel("Mobiliario del Baño")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        main_layout.addWidget(title)
        
        # Menú de iconos superior
        icon_menu = QWidget()
        icon_menu.setFixedHeight(100)
        icon_menu_layout = QHBoxLayout(icon_menu)
        icon_menu_layout.setSpacing(30)
        icon_menu_layout.setContentsMargins(0,0,0,0)
        
        icons = [
            ("stock.png", "Stock Actual"),
            ("salida.png", "Salida de Stock"),
            ("historial.png", "Historial de movimientos")
        ]
        self.icon_buttons = []
        for i, (icon, text) in enumerate(icons):
            btn_widget = QWidget()
            btn_widget.setContentsMargins(5,5,5,5)
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setSpacing(10)
            btn_layout.setContentsMargins(0,0,0,0)
            
            btn = QPushButton()
            btn.setIcon(QIcon(f"images/{icon}"))
            btn.setIconSize(QSize(50, 50))
            btn.setFixedSize(70, 70)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 35px;
                    padding: 0px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 165, 0, 0.3);
                }
            """)
            btn.clicked.connect(lambda _, idx=i: self.change_tab(idx))
            
            label = QLabel(text)
            label.setStyleSheet("color: white; font-size: 16px;")
            
            btn_layout.addWidget(btn)
            btn_layout.addWidget(label)
            
            icon_menu_layout.addWidget(btn_widget)
            self.icon_buttons.append(btn)
            
            if i < len(icons) - 1:
                separator = QFrame()
                separator.setFrameShape(QFrame.VLine)
                separator.setStyleSheet("background-color: rgba(255, 255, 255, 0.3);")
                separator.setFixedWidth(1)
                icon_menu_layout.addWidget(separator)
        
        icon_menu_layout.addStretch()
        main_layout.addWidget(icon_menu)
        
        # Contenido de las pestañas
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("""
            QWidget {
                background-color: rgba(30, 30, 30, 0.7);
                border-radius: 15px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        self.content_stack.setGraphicsEffect(shadow)
        
        for content in [self.create_stock_widget(), self.create_salida_widget(), self.create_historial_widget()]:
            self.content_stack.addWidget(content)
        
        main_layout.addWidget(self.content_stack, 1)
        
        # Botón flotante del chatbot
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
        self.chatbot_btn.show()
        self.chatbot_btn.raise_()
        
        self.positionChatbotButton()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.positionChatbotButton()
    
    def positionChatbotButton(self):
        margin = 20
        self.chatbot_btn.move(self.width() - self.chatbot_btn.width() - margin,
                              self.height() - self.chatbot_btn.height() - margin)
    
    def change_tab(self, index):
        self.content_stack.setCurrentIndex(index)
    
    def create_stock_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("Información del stock actual")
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        return widget
    
    def create_salida_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("Información de salida de stock")
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        return widget
    
    def create_historial_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel("Historial de movimientos")
        label.setStyleSheet("color: white; font-size: 18px;")
        layout.addWidget(label)
        return widget
    
    def toggleChatPopup(self):
        if self.chat_popup and self.chat_popup.isVisible():
            self.chat_popup.close()
            self.chat_popup = None
        else:
            from chatbot.chat_popup import ChatPopup
            self.chat_popup = ChatPopup(self.chatbot_btn, self)
            self.chat_popup.show()