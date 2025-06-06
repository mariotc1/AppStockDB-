"""
main_window.py

Módulo que contiene la ventana principal de la aplicación.

Implementa la navegación entre vistas mediante un menú lateral interactivo y animado.
Se cargan diferentes secciones como: información general, perfil de usuario,
gestión de mobiliario por categoría (habitaciones, electrodomésticos, zonas comunes, baños),
y ajustes/soporte.

Además, la clase se conecta a la API para mostrar la imagen de perfil actualizada
y permite cambiar dinámicamente entre vistas, aplicar temas y mostrar animaciones visuales.

Características:
- Menú lateral colapsable con animaciones.
- Sistema modular de vistas (`QStackedWidget`).
- Icono de usuario dinámico.
- Diseño responsivo y animaciones suaves.

Requiere:
    - PyQt5
    - requests
    - Archivos de configuración y vistas (`config/`, `views/`, `images/`)
"""

import sys, requests

from io import BytesIO  

from PyQt5.QtCore import (
    Qt, QPropertyAnimation, 
    QEasingCurve, QEvent
)

from PyQt5.QtGui import (
    QPainter, QPixmap, QLinearGradient, QBrush, 
    QColor, QFont, QIcon,QBitmap
)

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel, QStackedWidget, 
    QGraphicsOpacityEffect, QVBoxLayout
)

# Importación de los efectos/animaciones
from animations.lateral_menu_button import LateralMenuButton
from animations.rotating_logo_mw import RotatingLogo

# Importación de las vistas
from views.room_view import RoomView
from views.appliances_view import AppliancesView
from views.common_areas_view import CommonAreasView
from views.bathroom_view import BathroomView
from views.info_view import InfoView
from views.my_profile_view import MyProfileView
from views.settings_view import SettingsView

# URL para la conexión y uso de la api rest
API_BASE_URL = "http://localhost:5000"


# Clase principal de la app
class MainWindow(QWidget):

    """
    Inicializa la ventana principal, carga el tema, configura las vistas y el menú lateral.

    Args:
        user_id (int): ID del usuario autenticado.
    """
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id 
        
        # Veo si la app está en modo claro/oscuro desde el archivo de configuración
        import json
        try:
            with open("config/settings.json", "r") as f:
                config = json.load(f)
                self.current_theme = config.get("theme", "light")
        except (FileNotFoundError, json.JSONDecodeError):
            self.current_theme = "light"
        
        self.collapsed_width = 60
        self.expanded_width = 320
        
        self.initUI()
        self.fadeIn()
        self.setWindowTitle("AppStockDB")
        self.setWindowIcon(QIcon("images/logoDB_Blanco.png"))
        self.showMaximized()


    """
    Construye la interfaz completa: menú lateral, cabecera y área de vistas.

    Agrega botones de navegación, configura el QStackedWidget y conecta señales.
    """
    def initUI(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Menú lateral 
        self.lateral_menu = QWidget()
        self.lateral_menu.setMinimumWidth(self.collapsed_width)
        self.lateral_menu.setMaximumWidth(self.collapsed_width)
        
        lateral_layout = QVBoxLayout(self.lateral_menu)
        lateral_layout.setContentsMargins(5, 10, 5, 10)
        lateral_layout.setSpacing(10)

        self.logo_widget = RotatingLogo()
        lateral_layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Creo los botones de las vistas
        menu_items = ["Información del programa", 
                      "Mi Perfil", 
                      "Mobiliario Habitaciones", 
                      "Mobiliario Electrodomesticos", 
                      "Mobiliario Zonas Comunes", 
                      "Mobiliario Baño",
                      "Ajustes/Soporte"]

        menu_icons = {
            "Información del programa": "images/informacion.png",
            "Mi Perfil": "images/b_usuario.png",
            "Mobiliario Habitaciones": "images/b_habitaciones.jpg",
            "Mobiliario Electrodomesticos": "images/b_electodomesticos.png",
            "Mobiliario Zonas Comunes": "images/b_zonasComunes.png",
            "Mobiliario Baño": "images/b_bano.png",
            "Ajustes/Soporte": "images/b_ajustes.png"
        }

        self.menu_buttons = []

        # Creo el botón de la vista Información del programa
        info_button = LateralMenuButton("Información del programa", menu_icons["Información del programa"], is_main_view=True)
        info_button.clicked.connect(lambda: self.showView("Información del programa"))
        lateral_layout.addWidget(info_button)
        self.menu_buttons.append(info_button)

        # Creo el botón de la vista Mi Perfil
        self.user_icon_button = LateralMenuButton("Mi Perfil", "images/b_usuario.png", is_main_view=True)
        self.user_icon_button.setIcon(self.createCircularIcon("images/b_usuario.png"))
        self.user_icon_button.clicked.connect(lambda: self.showView("Mi Perfil"))
        lateral_layout.addWidget(self.user_icon_button)
        self.menu_buttons.append(self.user_icon_button)

        # Creo el resto de botones
        for item in menu_items[2:]:
            icon_path = menu_icons.get(item, "images/default.png")
            btn = LateralMenuButton(item, icon_path, is_main_view=True)
            btn.clicked.connect(lambda checked, name=item: self.showView(name))
            lateral_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        lateral_layout.addStretch()

        # Botones para salir y volver
        self.btn_volver = LateralMenuButton("Volver - pantalla bienvenida", "images/b_volver.png", is_main_view=False)
        self.btn_volver.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_volver.clicked.connect(self.volverWelcome)
        lateral_layout.addWidget(self.btn_volver)
        self.menu_buttons.append(self.btn_volver)

        self.btn_cerrar = LateralMenuButton("Salir del programa", "images/salir.png", is_main_view=False)
        self.btn_cerrar.setFont(QFont("Arial", 12, QFont.Bold))
        self.btn_cerrar.clicked.connect(self.closeApp)
        lateral_layout.addWidget(self.btn_cerrar)
        self.menu_buttons.append(self.btn_cerrar)

        self.main_layout.addWidget(self.lateral_menu)

        # Área de contenido
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)

        # Cabecera
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        self.title_label = QLabel("  Gestión de Stock DB Inmuebles")
        self.title_label.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        content_layout.addWidget(header)

        # Stacked widget 
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack, stretch=1)  

        # Añado las vistas (situadas en la carpeta views)
        self.info_view = InfoView()
        self.miPerfil_view = MyProfileView(user_id=self.user_id)  
        self.habitaciones_view = RoomView(categoria="Habitaciones")
        self.electrodomesticos_view = AppliancesView(categoria="Electrodomésticos")
        self.zonas_comunes_view = CommonAreasView(categoria="Zonas Comunes")
        self.bano_view = BathroomView(categoria="Baños")
        self.settings_view = SettingsView()
        
        # Diccionario de vistas
        self.views = {
            "Información del programa": self.info_view,
            "Mi Perfil": self.miPerfil_view,
            "Mobiliario Habitaciones": self.habitaciones_view,
            "Mobiliario Electrodomesticos": self.electrodomesticos_view,
            "Mobiliario Zonas Comunes": self.zonas_comunes_view,
            "Mobiliario Baño": self.bano_view,
            "Ajustes/Soporte": self.settings_view
        }

        # Añadir vistas al QStackedWidget
        for view in self.views.values():
            self.content_stack.addWidget(view)

        # Vista por defecto: Información
        self.content_stack.setCurrentWidget(self.info_view)

        content_layout.addWidget(self.content_stack)
        self.main_layout.addWidget(content_widget, stretch=1)
        self.lateral_menu.installEventFilter(self)
        self.load_profile_picture()
        self.miPerfil_view.profile_pic_updated.connect(self.updateUserIcon)


    """
    Actualiza dinámicamente el icono del usuario en el menú lateral.

    Args:
        new_icon_path (str): Ruta o URL de la nueva imagen.
    """
    def updateUserIcon(self, new_icon_path):
        try:

            if new_icon_path.startswith("http"):  
                img_data = requests.get(new_icon_path).content
                pixmap = QPixmap()
                pixmap.loadFromData(BytesIO(img_data).read())
            else:
                pixmap = QPixmap(new_icon_path)

            self.user_icon_button.setIcon(self.createCircularIcon(pixmap))

        except Exception as e:
            print(f"Error al actualizar el icono del usuario: {e}")
            self.user_icon_button.setIcon(self.createCircularIcon("images/b_usuario.png"))  # Imagen por defecto


    """
    Consulta la API para cargar la foto de perfil del usuario al iniciar la aplicación.
    """
    def load_profile_picture(self):
        try:

            response = requests.get(f"{API_BASE_URL}/get-user/{self.user_id}")

            if response.status_code == 200:

                user_data = response.json()
                profile_pic_url = user_data.get("profile_picture", "")

                # Verifico si la imagen está en la API o si sino poner la imagen por defecto
                if profile_pic_url.startswith("http"):
                    self.updateUserIcon(profile_pic_url)

                else:
                    self.updateUserIcon("images/b_usuario.png")  # Imagen por defecto si no hay personalizada

            else:
                print("Error al obtener datos del usuario.")
                self.updateUserIcon("images/b_usuario.png")  # Imagen por defecto en caso de error en la API

        except Exception as e:
            print(f"Error al cargar la imagen de perfil al iniciar la app: {e}")
            self.updateUserIcon("images/b_usuario.png")


    """
    Crea un icono redondo a partir de una imagen.

    Args:
        image_path (str or QPixmap): Ruta o imagen ya cargada.
        icon_size (int): Tamaño del icono (por defecto 32).

    Returns:
        QIcon: Icono con máscara circular aplicada.
    """
    def createCircularIcon(self, image_path, icon_size=32):
        pixmap = QPixmap(image_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Creo una máscara circular
        mask = QBitmap(pixmap.size())
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, pixmap.width(), pixmap.height())
        painter.end()

        pixmap.setMask(mask)

        return QIcon(pixmap)


    """
    Detecta si el cursor entra o sale del menú lateral para expandir o colapsar el menú.

    Args:
        source (QObject): Componente que emite el evento.
        event (QEvent): Evento recibido.

    Returns:
        bool: True si el evento fue procesado.
    """
    def eventFilter(self, source, event):
        if source == self.lateral_menu:
            if event.type() == QEvent.Enter:
                self.expandMenu()
            elif event.type() == QEvent.Leave:
                self.collapseMenu()
        return super().eventFilter(source, event)


    """
    Expande el menú lateral mediante una animación suave y muestra los textos de los botones.
    """
    def expandMenu(self):
        anim = QPropertyAnimation(self.lateral_menu, b"maximumWidth")
        anim.setDuration(300)
        anim.setStartValue(self.lateral_menu.width())
        anim.setEndValue(self.expanded_width)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        self.menu_anim = anim
        for btn in self.menu_buttons:
            btn.setExpanded(True)
    
    
    """
    Colapsa el menú lateral ocultando los textos, con una animación suave.
    """
    def collapseMenu(self):
        anim = QPropertyAnimation(self.lateral_menu, b"maximumWidth")
        anim.setDuration(300)
        anim.setStartValue(self.lateral_menu.width())
        anim.setEndValue(self.collapsed_width)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        self.menu_anim = anim
        for btn in self.menu_buttons:
            btn.setExpanded(False)


    """
    Muestra la vista correspondiente al nombre recibido en el área central.

    Args:
        view_name (str): Nombre de la vista a mostrar.
    """
    def showView(self, view_name):
        print(f"Mostrando vista: {view_name}")
        widget = self.views.get(view_name)
        if widget:
            self.content_stack.setCurrentWidget(widget)
        else:
            print("Vista no definida.")


    """
    Cierra la ventana actual y regresa a la pantalla de bienvenida.
    """
    def volverWelcome(self):
        print("Volviendo a la pantalla de bienvenida...")
        from welcome_window import WelcomeWindow
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()
        self.close()


    """
    Cierra completamente la aplicación.
    """
    def closeApp(self):
        print("Cerrando aplicación...")
        self.close()


    """
    Aplica un efecto de fade-in al abrir la ventana principal.
    """
    def fadeIn(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        anim = QPropertyAnimation(effect, b"opacity")
        anim.setDuration(1000)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        anim.start()
        self.fade_anim = anim


    """
    Dibuja el fondo de la ventana con un degradado dinámico según el tema visual.
    """
    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())

        if self.current_theme == "dark":
            # Fondo oscuro
            gradient.setColorAt(0.0, QColor(10, 10, 10))  
            gradient.setColorAt(1.0, QColor(30, 30, 30))  
        else:
            # Fondo claro
            gradient.setColorAt(0.0, QColor(0, 0, 0))
            gradient.setColorAt(1.0, QColor(255, 140, 0))

        painter.fillRect(rect, QBrush(gradient))
        super().paintEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Cargo el tema desde settings
    import json
    try:
        with open("config/settings.json", "r") as f:
            config = json.load(f)
            theme = config.get("theme", "light")
    except (FileNotFoundError, json.JSONDecodeError):
        theme = "light"

    if theme == "dark":
        with open("themes/dark.qss", "r") as f:
            app.setStyleSheet(f.read())
    else:
        with open("themes/light.qss", "r") as f:
            app.setStyleSheet(f.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())