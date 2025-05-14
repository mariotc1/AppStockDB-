"""
start_api.py

Script de arranque para el servidor Flask de la aplicación.

Importa la instancia `app` definida en `api.py` y la lanza en el puerto 5000
en modo producción (debug=False). Este archivo se utiliza como proceso
externo desde el launcher de la aplicación PyQt5.

Este script debe ejecutarse directamente y no ser importado como módulo.

Uso típico:
    python start_api.py

Notas:
    - El host está configurado como '127.0.0.1', por lo tanto, accesible solo localmente.
    - No activar debug=True en entorno de producción.
"""

from api import app

if __name__ == '__main__':
    print("[INFO] Servidor Flask arrancando desde start_api.py...")
    app.run(host="127.0.0.1", port=5000, debug=False)