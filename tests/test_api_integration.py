"""
test_api_integration.py

Pruebas de integración que requieren una instancia real de MySQL.

Estas pruebas están marcadas con el marcador 'integration' y se omiten
en las ejecuciones estándar de pruebas unitarias.

Para ejecutar solo estas pruebas:
    pytest tests/test_api_integration.py -m integration

Para ejecutar todas las pruebas incluyendo las de integración:
    pytest -m integration

En CI/CD, configura un servicio MySQL y establece las variables de entorno:
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
antes de ejecutar estas pruebas.
"""

import pytest

# Marca todos los tests de este archivo como 'integration'
pytestmark = pytest.mark.integration


def test_placeholder():
    """
    Las pruebas de integración requieren una instancia MySQL en ejecución.

    Consulta el archivo CI para configurar el servicio de base de datos
    antes de ejecutar este archivo de pruebas.
    """
    pass


# ---------------------------------------------------------------------------
# Ejemplos de pruebas de integración (requieren BD real)
# ---------------------------------------------------------------------------
# Descomenta y adapta estos tests cuando tengas una BD de prueba disponible.
#
# def test_health_check_integration(client):
#     """El endpoint /health responde correctamente con servidor real."""
#     response = client.get('/health')
#     assert response.status_code == 200
#     assert response.get_json()['status'] == 'ok'
#
#
# def test_listar_productos_integration(client):
#     """GET /productos/listar responde con una lista real de la BD."""
#     response = client.get('/productos/listar')
#     assert response.status_code == 200
#     assert isinstance(response.get_json(), list)
#
#
# def test_register_and_login_flow(client):
#     """Flujo completo: registro de usuario y posterior inicio de sesión."""
#     import time
#     email = f"integtest_{int(time.time())}@example.com"
#
#     # Registro
#     reg = client.post('/register', json={
#         'username': 'integration_user',
#         'email': email,
#         'password': 'IntegPass123!'
#     })
#     assert reg.status_code == 201
#
#     # Login
#     login = client.post('/login', json={
#         'email': email,
#         'password': 'IntegPass123!'
#     })
#     assert login.status_code == 200
#     assert login.get_json()['username'] == 'integration_user'
