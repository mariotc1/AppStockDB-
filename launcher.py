"""
launcher.py

Punto de entrada principal de la aplicación de escritorio.

Este script lanza la interfaz gráfica de usuario (PyQt5) y arranca simultáneamente
la API REST desarrollada en Flask como un proceso independiente.

Flujo de ejecución:
- Inicia el servidor Flask ejecutando `start_api.py`.
- Carga el tema visual actual desde el `ThemeManager`.
- Verifica si hay una sesión de usuario activa.
    - Si existe, abre la ventana principal de la aplicación con un loader.
    - Si no existe, muestra la ventana de bienvenida.
- Al cerrar la aplicación, finaliza el proceso del servidor Flask.

Este script debe ejecutarse directamente (`__main__`) y no ser importado como módulo.

Requiere:
    - Python 3.x
    - PyQt5
    - start_api.py (API REST)
    - main.py (lógica principal)
    - welcome_window.py (ventana inicial)
    - themes/theme_manager.py (gestión de temas visuales)
"""

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