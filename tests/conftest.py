"""
conftest.py

Configuración compartida para el conjunto de pruebas pytest.

Añade el directorio backend al path de Python, establece las variables
de entorno requeridas antes de importar la app, y expone fixtures
reutilizables para el cliente de prueba y las conexiones a BD simuladas.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Añadir backend al path para poder importar la app Flask
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Establecer las variables de entorno requeridas ANTES de importar la app
# (db_config llama a os.getenv en tiempo de importación)
os.environ.setdefault('DB_HOST', '127.0.0.1')
os.environ.setdefault('DB_PORT', '3306')
os.environ.setdefault('DB_USER', 'testuser')
os.environ.setdefault('DB_PASSWORD', 'testpassword')
os.environ.setdefault('DB_NAME', 'db_test')

from api import app  # noqa: E402


@pytest.fixture
def client():
    """Cliente de prueba de Flask con modo TESTING activado."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_db():
    """
    Proporciona una conexión y cursor de BD simulados (MagicMock).

    Uso:
        mock_conn, mock_cursor = mock_db
    """
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    # Soporte para uso como gestor de contexto (por si se usa en el futuro)
    mock_conn.__enter__ = lambda s: s
    mock_conn.__exit__ = MagicMock(return_value=False)
    return mock_conn, mock_cursor
