"""
launcher.py

Punto de entrada de la aplicación de escritorio AppStockDB.

La API REST corre en un contenedor Docker (desarrollo) o en un servidor
en la nube (producción). Este proceso solo arranca la interfaz PyQt5 y
se conecta a la API a través de la URL configurada en API_BASE_URL.

Variables de entorno relevantes (se cargan desde .env):
    API_BASE_URL — URL de la API REST (por defecto http://127.0.0.1:5001)
"""

import sys
import os
import time

_FROZEN = getattr(sys, 'frozen', False)

if _FROZEN:
    _BASE_DIR = getattr(sys, '_MEIPASS')  # type: ignore[attr-defined]
    os.chdir(_BASE_DIR)
else:
    _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.join(_BASE_DIR, 'frontend'))


def _wait_for_api(url: str, retries: int = 5, delay: float = 1.5) -> bool:
    """Intenta conectar con /health hasta 'retries' veces antes de rendirse."""
    import requests
    for attempt in range(retries):
        try:
            r = requests.get(f"{url}/health", timeout=3)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        if attempt < retries - 1:
            time.sleep(delay)
    return False


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMessageBox
    from themes.theme_manager import ThemeManager
    from config import API_BASE_URL

    app = QApplication(sys.argv)
    ThemeManager.load_theme(app)

    if not _wait_for_api(API_BASE_URL):
        QMessageBox.critical(
            None,
            "No se puede conectar",
            f"La API no responde en:\n{API_BASE_URL}\n\n"
            "Asegúrate de que los contenedores Docker están activos:\n\n"
            "  make up\n\n"
            "o consulta los logs con:\n\n"
            "  make api-logs",
        )
        sys.exit(1)

    from main import show_main_with_loader, load_session

    user_id = load_session()
    if user_id:
        show_main_with_loader(user_id)
    else:
        from welcome_window import WelcomeWindow
        welcome_window = WelcomeWindow()
        welcome_window.show()

    sys.exit(app.exec_())
