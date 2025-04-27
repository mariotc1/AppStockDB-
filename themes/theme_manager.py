import json
import os

# Clase para gestionar el tema de la aplicación
class ThemeManager:

    # Archivo de configuración donde se guarda el tema
    CONFIG_FILE = "config/settings.json"
    DARK_THEME = "themes/dark.qss"
    LIGHT_THEME = "themes/light.qss"

    
    # Carga el tema guardado en el archivo de configuración
    @staticmethod
    def load_theme(app):
        if not os.path.exists(ThemeManager.CONFIG_FILE):
            ThemeManager.save_theme("light")  # Por defecto light si no existe
        
        with open(ThemeManager.CONFIG_FILE, "r") as f:
            config = json.load(f)
            theme = config.get("theme", "light")
            ThemeManager.apply_theme(app, theme)

   
    # Guarda el tema actual en configuración
    @staticmethod
    def save_theme(theme):
        os.makedirs(os.path.dirname(ThemeManager.CONFIG_FILE), exist_ok=True)
        with open(ThemeManager.CONFIG_FILE, "w") as f:
            json.dump({"theme": theme}, f)

    
    # Aplica el tema ligth/dark a toda la aplicación
    @staticmethod
    def apply_theme(app, theme):
        if theme == "dark":
            qss_file = ThemeManager.DARK_THEME
        else:
            qss_file = ThemeManager.LIGHT_THEME
        
        with open(qss_file, "r") as f:
            app.setStyleSheet(f.read())

    
    # Cambia entre light y dark
    @staticmethod
    def toggle_theme(app):
        with open(ThemeManager.CONFIG_FILE, "r") as f:
            config = json.load(f)
            current_theme = config.get("theme", "light")

        new_theme = "dark" if current_theme == "light" else "light"
        ThemeManager.apply_theme(app, new_theme)
        ThemeManager.save_theme(new_theme)