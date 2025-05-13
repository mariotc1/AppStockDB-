import sys
import subprocess
import time
from PyQt5.QtWidgets import QApplication
from main import show_main_with_loader, load_session
from themes.theme_manager import ThemeManager
import os

if __name__ == '__main__':
    # Lazon el proceso externo de Flask para arrancar la API
    flask_process = subprocess.Popen([sys.executable, 'start_api.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    time.sleep(2)

    app = QApplication(sys.argv)
    ThemeManager.load_theme(app)

    user_id = load_session()
    if user_id:
        show_main_with_loader(user_id)
    else:
        from welcome_window import WelcomeWindow
        welcome_window = WelcomeWindow()
        welcome_window.show()

    try:
        sys.exit(app.exec_())
    finally:
        # Cierro la API al cerrar la app
        flask_process.terminate()