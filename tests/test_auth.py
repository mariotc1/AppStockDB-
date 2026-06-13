"""
test_auth.py

Pruebas unitarias para los endpoints de autenticación:
    POST /register
    POST /login
    POST /forgot-password

Todos los accesos a BD están simulados con unittest.mock para que
las pruebas no requieran un servidor MySQL real.
"""

import bcrypt
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# /register
# ---------------------------------------------------------------------------

class TestRegister:

    def test_register_missing_all_fields(self, client):
        """Devuelve 400 cuando el body JSON está vacío."""
        response = client.post('/register', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_register_missing_email(self, client):
        """Devuelve 400 cuando falta el campo email."""
        response = client.post('/register', json={
            'username': 'testuser',
            'password': 'TestPass123!'
        })
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_register_missing_password(self, client):
        """Devuelve 400 cuando falta el campo password."""
        response = client.post('/register', json={
            'username': 'testuser',
            'email': 'test@example.com'
        })
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_register_success(self, client):
        """
        El registro exitoso devuelve 201 con message, user_id y username.

        Se simula la BD para que cursor.lastrowid devuelva un ID conocido.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.lastrowid = 42

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/register', json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'TestPass123!'
            })

        assert response.status_code == 201
        data = response.get_json()
        assert data['message'] == 'Usuario registrado exitosamente.'
        assert data['user_id'] == 42
        assert data['username'] == 'testuser'

    def test_register_db_error_returns_500(self, client):
        """
        Un error de mysql.connector al insertar devuelve 500.
        """
        import mysql.connector

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error("duplicate entry")

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/register', json={
                'username': 'testuser',
                'email': 'existing@example.com',
                'password': 'TestPass123!'
            })

        assert response.status_code == 500
        assert 'error' in response.get_json()


# ---------------------------------------------------------------------------
# /login
# ---------------------------------------------------------------------------

class TestLogin:

    def test_login_missing_all_fields(self, client):
        """Devuelve 400 cuando el body JSON está vacío."""
        response = client.post('/login', json={})
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_login_missing_password(self, client):
        """Devuelve 400 cuando falta el campo password."""
        response = client.post('/login', json={'email': 'user@example.com'})
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_login_user_not_found(self, client):
        """
        Devuelve 404 cuando el email no existe en la BD.

        La API devuelve 404 (no 401) cuando fetchone() es None.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # usuario no encontrado

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/login', json={
                'email': 'noexiste@example.com',
                'password': 'cualquierpass'
            })

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    def test_login_wrong_password(self, client):
        """
        Devuelve 401 cuando el email existe pero la contraseña es incorrecta.

        Se prepara un hash bcrypt real de 'correctpassword' para que
        bcrypt.checkpw falle al comparar con 'wrongpassword'.
        """
        real_hash = bcrypt.hashpw(b'correctpassword', bcrypt.gensalt()).decode('utf-8')

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 1,
            'username': 'testuser',
            'email': 'user@example.com',
            'password': real_hash
        }

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/login', json={
                'email': 'user@example.com',
                'password': 'wrongpassword'
            })

        assert response.status_code == 401
        assert 'error' in response.get_json()

    def test_login_success(self, client):
        """
        Devuelve 200 con message, user_id y username cuando las credenciales son correctas.
        """
        real_hash = bcrypt.hashpw(b'correctpassword', bcrypt.gensalt()).decode('utf-8')

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 7,
            'username': 'testuser',
            'email': 'user@example.com',
            'password': real_hash
        }

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/login', json={
                'email': 'user@example.com',
                'password': 'correctpassword'
            })

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Inicio de sesión exitoso.'
        assert data['user_id'] == 7
        assert data['username'] == 'testuser'


# ---------------------------------------------------------------------------
# /forgot-password
# ---------------------------------------------------------------------------

class TestForgotPassword:

    def test_forgot_password_missing_email(self, client):
        """Devuelve 400 cuando no se envía el campo email."""
        response = client.post('/forgot-password', json={})
        assert response.status_code == 400
        assert 'error' in response.get_json()

    def test_forgot_password_email_not_registered(self, client):
        """Devuelve 404 cuando el email no está registrado."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/forgot-password', json={
                'email': 'noexiste@example.com'
            })

        assert response.status_code == 404
        assert 'error' in response.get_json()

    def test_forgot_password_success(self, client):
        """
        Devuelve 200 con message y un recovery_code de 6 dígitos
        cuando el email está registrado.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {
            'id': 3,
            'email': 'user@example.com'
        }

        with patch('api.get_db_connection', return_value=mock_conn):
            response = client.post('/forgot-password', json={
                'email': 'user@example.com'
            })

        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Código de recuperación generado.'
        assert 'recovery_code' in data
        assert len(data['recovery_code']) == 6
        assert data['recovery_code'].isdigit()
