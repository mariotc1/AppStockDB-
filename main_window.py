import sys, math, requests
from io import BytesIO  
from PyQt5.QtCore import (
    Qt, QTimer, QPropertyAnimation, QEasingCurve, QSize, 
    QEvent, QRect, QPoint, QTimer,QCoreApplication
)
from PyQt5.QtGui import (
    QPainter, QPixmap, QTransform, QLinearGradient, QBrush, 
    QColor, QFont, QIcon,QBitmap, QMovie
)
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QStackedWidget, QFrame, QGraphicsOpacityEffect, QSizePolicy, QTextEdit,
    QDialog, QVBoxLayout, QMessageBox
)
        
# Importación de las vistas
from views.habitaciones_view import HabitacionesView
from views.electrodomesticos_view import ElectrodomesticosView
from views.zonas_comunes_view import ZonasComunesView
from views.bano_view import BanoView
from views.info_view import InfoView
from views.miPerfil_view import MiPerfilView

API_BASE_URL = "http://localhost:5000"

class LateralMenuButton(QPushButton):
    def __init__(self, text, icon_path, is_main_view=True, parent=None):
        super().__init__("", parent)
        self.full_text = text
        self.full_icon = QIcon(icon_path)
        self.setIcon(self.full_icon)
        self.setIconSize(QSize(32, 32))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(60)
        self.is_main_view = is_main_view
        self.setExpanded(False)

    def setExpanded(self, expanded: bool):
        if expanded:
            text_color = "white" if self.is_main_view else "black"
            font_weight = "bold"
            font_size = "16px" if self.is_main_view else "14px"
            self.setText("  " + self.full_text)
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 255, 255, 0.1);
                    color: {text_color};
                    border: none;
                    border-radius: 5px;
                    font-size: {font_size};
                    font-weight: {font_weight};
                    text-align: left;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 165, 0, 0.8);
                }}
            """)
        else:
            self.setText("")
            self.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-radius: 5px;
                    text-align: center;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 165, 0, 0.8);
                }
            """)
        self.update()

class RotatingLogo(QWidget):
    def __init__(self, logo_path="images/logoDB_Blanco.png", parent=None):
        super().__init__(parent)
        self.logo = QPixmap(logo_path)
        self.logo = self.logo.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start(50)
        self.setFixedSize(60, 60)

    def updateRotation(self):
        self.angle = (self.angle + 1) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        center_x = rect.width() // 2
        center_y = rect.height() // 2
        angle_radians = math.radians(self.angle)
        scale_x = abs(math.cos(angle_radians))
        transform = QTransform()
        transform.translate(center_x, center_y)
        transform.scale(scale_x, 1.0)
        transform.translate(-self.logo.width() // 2, -self.logo.height() // 2)
        painter.setTransform(transform)
        painter.drawPixmap(0, 0, self.logo)
        painter.resetTransform()


# Clase principal MainWindow
class MainWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id  # ✅ Ahora sí recibe el ID desde LoginWindow
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()
        self.collapsed_width = 60
        self.expanded_width = 320
        self.initUI()
        self.fadeIn()

    def initUI(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # MENÚ LATERAL
        self.lateral_menu = QWidget()
        self.lateral_menu.setMinimumWidth(self.collapsed_width)
        self.lateral_menu.setMaximumWidth(self.collapsed_width)
        lateral_layout = QVBoxLayout(self.lateral_menu)
        lateral_layout.setContentsMargins(5, 10, 5, 10)
        lateral_layout.setSpacing(10)

        self.logo_widget = RotatingLogo()
        lateral_layout.addWidget(self.logo_widget, alignment=Qt.AlignCenter)

        # Crear botones con vistas
        menu_items = ["Información del programa", "Mi Perfil", "Mobiliario Habitaciones", 
                    "Mobiliario Electrodomesticos", "Mobiliario Zonas Comunes", "Mobiliario Baño"]

        menu_icons = {
            "Información del programa": "images/informacion.png",
            "Mi Perfil": "images/usuario.png",
            "Mobiliario Habitaciones": "images/mobiliario_Habitaciones.png",
            "Mobiliario Electrodomesticos": "images/mobiliario_Electrodomesticos.png",
            "Mobiliario Zonas Comunes": "images/zonas_comunes.png",
            "Mobiliario Baño": "images/mobiliario_Bano.png"
        }

        self.menu_buttons = []

        # Crear el botón "Información del programa" (Primero)
        info_button = LateralMenuButton("Información del programa", menu_icons["Información del programa"], is_main_view=True)
        info_button.clicked.connect(lambda: self.showView("Información del programa"))
        lateral_layout.addWidget(info_button)
        self.menu_buttons.append(info_button)

        # Crear el botón "Mi Perfil" (Segundo)
        self.user_icon_button = LateralMenuButton("Mi Perfil", "images/usuario.png", is_main_view=True)
        self.user_icon_button.setIcon(self.createCircularIcon("images/usuario.png"))
        self.user_icon_button.clicked.connect(lambda: self.showView("Mi Perfil"))
        lateral_layout.addWidget(self.user_icon_button)
        self.menu_buttons.append(self.user_icon_button)

        # Crear el resto de botones
        for item in menu_items[2:]:
            icon_path = menu_icons.get(item, "images/default.png")
            btn = LateralMenuButton(item, icon_path, is_main_view=True)
            btn.clicked.connect(lambda checked, name=item: self.showView(name))
            lateral_layout.addWidget(btn)
            self.menu_buttons.append(btn)

        lateral_layout.addStretch()

        # Botones para salir y volver
        self.btn_volver = LateralMenuButton("Volver - pantalla bienvenida", "images/volver.png", is_main_view=False)
        self.btn_volver.clicked.connect(self.volverWelcome)
        lateral_layout.addWidget(self.btn_volver)
        self.menu_buttons.append(self.btn_volver)

        self.btn_cerrar = LateralMenuButton("Salir del programa", "images/salir.png", is_main_view=False)
        self.btn_cerrar.clicked.connect(self.closeApp)
        lateral_layout.addWidget(self.btn_cerrar)
        self.menu_buttons.append(self.btn_cerrar)

        self.main_layout.addWidget(self.lateral_menu)

        # ÁREA DE CONTENIDO
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)

        # CABECERA
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(5, 5, 5, 5)
        header_layout.setSpacing(10)
        self.title_label = QLabel("Gestión de Stock DB Inmuebles")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setStyleSheet("color: white; letter-spacing: 1px;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        content_layout.addWidget(header)

        # ✅ CORRECTO: Definir content_stack antes de usarlo
        self.content_stack = QStackedWidget()  # 🔥 Crear el QStackedWidget primero
        self.content_stack.setMaximumHeight(self.height() - 100)
        self.content_stack.update()
        self.update()

        # Ahora sí puedes agregarlo al layout
        content_layout.addWidget(self.content_stack, stretch=1)  # ✅ Ahora sí es correcto

        # Vistas
        self.info_view = InfoView()
        self.miPerfil_view = MiPerfilView(user_id=self.user_id)  
        self.habitaciones_view = HabitacionesView()
        self.electrodomesticos_view = ElectrodomesticosView()
        self.zonas_comunes_view = ZonasComunesView()
        self.bano_view = BanoView()

        # Diccionario de vistas
        self.views = {
            "Información del programa": self.info_view,
            "Mi Perfil": self.miPerfil_view,
            "Mobiliario Habitaciones": self.habitaciones_view,
            "Mobiliario Electrodomesticos": self.electrodomesticos_view,
            "Mobiliario Zonas Comunes": self.zonas_comunes_view,
            "Mobiliario Baño": self.bano_view
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

    def updateUserIcon(self, new_icon_path):
        """Actualiza el icono del usuario en el menú lateral en tiempo real con formato circular."""
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
            self.user_icon_button.setIcon(self.createCircularIcon("images/usuario.png"))  # Imagen por defecto


    def load_profile_picture(self):
        """Carga la foto de perfil del usuario desde la API al iniciar la aplicación"""
        try:
            response = requests.get(f"{API_BASE_URL}/get-user/{self.user_id}")
            if response.status_code == 200:
                user_data = response.json()
                profile_pic_url = user_data.get("profile_picture", "")

                # 🔥 Verificar si la imagen está en la API o si se trata de la imagen por defecto
                if profile_pic_url.startswith("http"):
                    self.updateUserIcon(profile_pic_url)
                else:
                    self.updateUserIcon("images/usuario.png")  # Imagen por defecto si no hay personalizada

            else:
                print("Error al obtener datos del usuario.")
                self.updateUserIcon("images/usuario.png")  # Imagen por defecto en caso de error en la API

        except Exception as e:
            print(f"Error al cargar la imagen de perfil al iniciar la app: {e}")
            self.updateUserIcon("images/usuario.png")

    def createCircularIcon(self, image_path, icon_size=32):
        """Crea un icono circular a partir de una imagen."""
        pixmap = QPixmap(image_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Crear una máscara circular
        mask = QBitmap(pixmap.size())
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, pixmap.width(), pixmap.height())
        painter.end()

        # Aplicar la máscara circular
        pixmap.setMask(mask)

        return QIcon(pixmap)

    def eventFilter(self, source, event):
        if source == self.lateral_menu:
            if event.type() == QEvent.Enter:
                self.expandMenu()
            elif event.type() == QEvent.Leave:
                self.collapseMenu()
        return super().eventFilter(source, event)

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

    def showView(self, view_name):
        print(f"Mostrando vista: {view_name}")
        widget = self.views.get(view_name)
        if widget:
            self.content_stack.setCurrentWidget(widget)
        else:
            print("Vista no definida.")

    def volverWelcome(self):
        print("Volviendo a la pantalla de bienvenida...")
        from welcome_window import WelcomeWindow
        self.welcome_window = WelcomeWindow()
        self.welcome_window.show()
        self.close()

    def closeApp(self):
        print("Cerrando aplicación...")
        self.close()

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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0.0, QColor(0, 0, 0))
        gradient.setColorAt(1.0, QColor(255, 140, 0))
        painter.fillRect(rect, QBrush(gradient))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())