"""
test_api_health.py

Pruebas del endpoint de comprobación de estado (/health) y de la
configuración básica de la aplicación Flask.
"""


def test_health_check(client):
    """El endpoint /health devuelve 200 y status 'ok'."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_health_check_content_type(client):
    """El endpoint /health devuelve Content-Type application/json."""
    response = client.get('/health')
    assert 'application/json' in response.content_type


def test_unknown_route_returns_404(client):
    """Una ruta inexistente devuelve 404."""
    response = client.get('/ruta-que-no-existe')
    assert response.status_code == 404
