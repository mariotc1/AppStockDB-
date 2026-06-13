"""
test_products.py

Pruebas unitarias para los endpoints de productos:
    GET  /productos/listar
    POST /productos/agregar
    PUT  /productos/editar/<id>
    DELETE /productos/eliminar/<id>

Todos los accesos a BD están simulados con unittest.mock.
"""

from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# GET /productos/listar
# ---------------------------------------------------------------------------

class TestListarProductos:

    def test_listar_returns_200(self, client):
        """Devuelve 200 y una lista cuando la BD está disponible."""
        sample_products = [
            {'id': 1, 'nombre': 'Teclado', 'estado': 'Nuevo', 'cantidad': 10, 'categoria': 'Informática'},
            {'id': 2, 'nombre': 'Ratón', 'estado': 'Usado', 'cantidad': 5, 'categoria': 'Informática'},
        ]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = sample_products

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.get('/productos/listar')

        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_listar_returns_empty_list(self, client):
        """Devuelve 200 y una lista vacía cuando no hay productos."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.get('/productos/listar')

        assert response.status_code == 200
        assert response.get_json() == []

    def test_listar_product_fields(self, client):
        """Cada producto en la lista contiene los campos esperados."""
        sample_products = [
            {'id': 1, 'nombre': 'Monitor', 'estado': 'Nuevo', 'cantidad': 3, 'categoria': 'Informática'}
        ]

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = sample_products

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.get('/productos/listar')

        data = response.get_json()
        product = data[0]
        for field in ('id', 'nombre', 'estado', 'cantidad', 'categoria'):
            assert field in product, f"Campo '{field}' no encontrado en el producto"


# ---------------------------------------------------------------------------
# POST /productos/agregar
# ---------------------------------------------------------------------------

class TestAgregarProducto:

    def test_agregar_missing_all_fields(self, client):
        """Devuelve 400 cuando el body JSON está vacío."""
        response = client.post('/productos/agregar', json={})
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_agregar_missing_categoria(self, client):
        """Devuelve 400 cuando falta el campo categoria."""
        response = client.post('/productos/agregar', json={
            'nombre': 'Teclado',
            'estado': 'Nuevo',
            'cantidad': 5
        })
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_agregar_missing_nombre(self, client):
        """Devuelve 400 cuando falta el campo nombre."""
        response = client.post('/productos/agregar', json={
            'estado': 'Nuevo',
            'cantidad': 5,
            'categoria': 'Informática'
        })
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_agregar_success(self, client):
        """
        Devuelve 201 con mensaje de confirmación cuando todos los campos están presentes
        y la BD acepta la inserción.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/productos/agregar', json={
                'nombre': 'Teclado mecánico',
                'estado': 'Nuevo',
                'cantidad': 10,
                'categoria': 'Informática'
            })

        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Producto agregado correctamente.'


# ---------------------------------------------------------------------------
# PUT /productos/editar/<id>
# ---------------------------------------------------------------------------

class TestEditarProducto:

    def test_editar_missing_fields(self, client):
        """Devuelve 400 cuando faltan campos obligatorios."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.put('/productos/editar/1', json={'nombre': 'Solo nombre'})

        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_editar_producto_no_encontrado(self, client):
        """Devuelve 404 cuando el producto no existe en la BD."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # producto no existe

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.put('/productos/editar/999', json={
                'nombre': 'Teclado actualizado',
                'cantidad': 15,
                'estado': 'Usado'
            })

        assert response.status_code == 404
        assert 'error' in response.get_json()

    def test_editar_success(self, client):
        """Devuelve 200 con mensaje de confirmación cuando el producto existe."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        # fetchone devuelve una fila (el producto existe)
        mock_cursor.fetchone.return_value = (1, 'Teclado', 'Nuevo', 10, 'Informática')

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.put('/productos/editar/1', json={
                'nombre': 'Teclado actualizado',
                'cantidad': 15,
                'estado': 'Usado'
            })

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Producto actualizado correctamente.'


# ---------------------------------------------------------------------------
# DELETE /productos/eliminar/<id>
# ---------------------------------------------------------------------------

class TestEliminarProducto:

    def test_eliminar_returns_200(self, client):
        """
        Devuelve 200 con mensaje de confirmación.

        La API ejecuta DELETE directamente sin comprobar existencia previa,
        por lo que siempre devuelve 200 si la BD no lanza excepción.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.delete('/productos/eliminar/999')

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Producto eliminado correctamente.'

    def test_eliminar_db_error_returns_500(self, client):
        """Devuelve 500 cuando la BD lanza un error al eliminar."""
        import mysql.connector

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error("foreign key constraint")

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.delete('/productos/eliminar/1')

        assert response.status_code == 500
        assert 'error' in response.get_json()
