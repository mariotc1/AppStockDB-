"""
Clase encargada de gestionar y aplicar los temas de la interfaz (modo claro u oscuro) en la aplicación.

Permite cargar, guardar y alternar entre temas a través de archivos `.qss`, aplicándolos globalmente
a la instancia de la aplicación. Guarda la configuración persistente en un archivo JSON.

Temas soportados:
- Modo claro: 'themes/light.qss'
- Modo oscuro: 'themes/dark.qss'
"""

import json
import os

# Clase para gestionar el tema de la aplicación
class ThemeManager:

    # Archivo de configuración donde se guarda el tema
    CONFIG_FILE = "config/settings.json"
    DARK_THEME = "themes/dark.qss"
    LIGHT_THEME = "themes/light.qss"

    
    """
    Carga y aplica el tema guardado en el archivo de configuración JSON.  
    Si no existe, se crea por defecto con el tema claro.

    :param app: Instancia de QApplication a la que se aplica el estilo visual.
    """
    @staticmethod
    def load_theme(app):
        if not os.path.exists(ThemeManager.CONFIG_FILE):
            ThemeManager.save_theme("light")  # Por defecto light si no existe
        
        with open(ThemeManager.CONFIG_FILE, "r") as f:
            config = json.load(f)
            theme = config.get("theme", "light")
            ThemeManager.apply_theme(app, theme)

   
    """
    Guarda el tema actual en el archivo de configuración para su persistencia.

    :param theme: Nombre del tema a guardar ('light' o 'dark').
    """
    @staticmethod
    def save_theme(theme):
        os.makedirs(os.path.dirname(ThemeManager.CONFIG_FILE), exist_ok=True)
        with open(ThemeManager.CONFIG_FILE, "w") as f:
            json.dump({"theme": theme}, f)

    
    """
    Aplica el tema visual a la instancia de la aplicación leyendo el archivo `.qss`.

    :param app: Instancia de QApplication a modificar.
    :param theme: Nombre del tema a aplicar ('light' o 'dark').
    """
    @staticmethod
    def apply_theme(app, theme):
        if theme == "dark":
            qss_file = ThemeManager.DARK_THEME
        else:
            qss_file = ThemeManager.LIGHT_THEME
        
        with open(qss_file, "r") as f:
            app.setStyleSheet(f.read())

    
    """
    Alterna entre el modo claro y oscuro, aplica el nuevo tema y actualiza la configuración.

    :param app: Instancia de QApplication sobre la que se hace el cambio de estilo.
    """
    @staticmethod
    def toggle_theme(app):
        with open(ThemeManager.CONFIG_FILE, "r") as f:
            config = json.load(f)
            current_theme = config.get("theme", "light")

        new_theme = "dark" if current_theme == "light" else "light"
        ThemeManager.apply_theme(app, new_theme)
        ThemeManager.save_theme(new_theme)