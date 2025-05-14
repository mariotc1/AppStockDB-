"""
main.py

Este módulo gestiona la carga de sesión del usuario y el arranque de la ventana principal
de la aplicación PyQt5.

Incluye funciones para:
- Cargar el identificador de sesión guardado localmente.
- Mostrar una pantalla de carga mientras se recuperan los datos del usuario desde la API.
- Lanzar la ventana principal (`MainWindow`) con el usuario autenticado.

Requiere que el servidor Flask esté corriendo localmente (`http://localhost:5000`).
"""

import sys, json, os, requests

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from welcome_window import WelcomeWindow
from main_window import MainWindow
from themes.theme_manager import ThemeManager
from session_loading import SessionLoading

"""
Carga el ID de usuario desde el archivo local de sesión.

Returns:
    int or None: ID del usuario si existe, o None si no hay sesión válida.
"""
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


"""
Muestra una pantalla de carga y luego lanza la ventana principal.

Consulta la API para recuperar el nombre del usuario y lo muestra
durante el splash de carga (`SessionLoading`).

Args:
    user_id (int): ID del usuario autenticado.
"""
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

    # Delay para mostrar la pantalla de carga por 2 segundos
    QTimer.singleShot(2000, open_main)