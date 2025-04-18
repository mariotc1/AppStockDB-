import sys
from PyQt5.QtWidgets import QApplication
from welcome_window import WelcomeWindow
from themes.theme_manager import ThemeManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Aplicar el último tema usado
    ThemeManager.load_theme(app)

    # Iniciar la ventana de bienvenida
    welcome_window = WelcomeWindow()
    welcome_window.show()
    
    sys.exit(app.exec_())