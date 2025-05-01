import sys
import json
import os
import requests
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from welcome_window import WelcomeWindow
from main_window import MainWindow
from themes.theme_manager import ThemeManager
from session_loading import SessionLoading

def load_session():
    session_path = os.path.join("config", "session.json")
    if os.path.exists(session_path):
        try:
            with open(session_path, "r") as f:
                session = json.load(f)
                return session.get("user_id")
        except Exception:
            return None
    return None

def show_main_with_loader(user_id):
    try:
        response = requests.get(f"http://localhost:5000/get-user/{user_id}")
        if response.status_code == 200:
            username = response.json().get("username", "Usuario")
        else:
            username = "Usuario"
    except:
        username = "Usuario"

    splash = SessionLoading(username)
    splash.show()

    def open_main():
        main_window = MainWindow(user_id)
        main_window.show()
        splash.close()

    # Delay para mostrar la pantalla de carga (ajustable)
    QTimer.singleShot(2000, open_main)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ThemeManager.load_theme(app)

    user_id = load_session()

    if user_id:
        show_main_with_loader(user_id)
    else:
        welcome_window = WelcomeWindow()
        welcome_window.show()

    sys.exit(app.exec_())
