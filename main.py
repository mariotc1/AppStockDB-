import sys
from PyQt5.QtWidgets import QApplication
from welcome_window import WelcomeWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Crear e iniciar la ventana de bienvenida
    welcome_window = WelcomeWindow()
    welcome_window.show()
    
    sys.exit(app.exec_())