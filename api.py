"""
api.py

Módulo principal que define la API REST de la aplicación de gestión de stock mediante Flask.

Contiene todos los endpoints necesarios para la autenticación de usuarios,
gestión de productos, control de salidas de stock, historial de movimientos,
actualización de perfil, subida de imágenes y exportación de datos a Excel.

Características principales:
- Registro, login y recuperación de contraseña de usuarios.
- CRUD completo de productos (añadir, editar, listar, eliminar).
- Gestión de salidas de stock, con posibilidad de asignación múltiple y devolución.
- Registro y eliminación de movimientos en el historial.
- Subida de foto de perfil de usuario.
- Exportación de productos e historial en formato Excel.
- Servidor preparado para trabajar con respuestas JSON por defecto.

Dependencias:
    - Flask
    - mysql-connector-python
    - bcrypt
    - pandas
    - PyMySQL (si se cambia driver)
    - werkzeug

Este módulo está pensado para ser ejecutado como backend y conectado desde
una interfaz PyQt5 vía HTTP.
"""

import mysql.connector, bcrypt, os, string, random
import pandas as pd

from flask import Flask, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv()  # Carga las variables desde el archivo .env

db_config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT")),
    'database': os.getenv("DB_NAME")
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


"""
Registra un nuevo usuario en la base de datos.

Recibe un JSON con username, email y password. Hashea la contraseña
y guarda el nuevo usuario.

Returns:
    Response: JSON con mensaje de éxito o error.
"""
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Faltan campos obligatorios.'}), 400

    # Hashear la contraseña para mayor seguridad
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Insertar usuario en la base de datos
        sql = "INSERT INTO usuarios (username, email, password, profile_picture) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, email, hashed_password.decode('utf-8'), None))
        cnx.commit()

        # Obtener el ID del usuario recién creado
        user_id = cursor.lastrowid

        return jsonify({
            'message': 'Usuario registrado exitosamente.',
            'user_id': user_id,
            'username': username
        }), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        cnx.close()


"""
Inicia sesión de un usuario validando sus credenciales.

Recibe email y password, y compara con la base de datos.

Returns:
    Response: JSON con datos del usuario si es exitoso, o error.
"""
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Faltan campos obligatorios.'}), 400

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        sql = "SELECT * FROM usuarios WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        if user:
            stored_password = user['password'].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                return jsonify({
                    'message': 'Inicio de sesión exitoso.',
                    'user_id': user['id'],
                    'username': user['username']
                }), 200
            else:
                return jsonify({'error': 'Credenciales inválidas.'}), 401
        else:
            return jsonify({'error': 'Usuario no encontrado.'}), 404
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Genera un código de recuperación para un usuario dado su email.

Returns:
    Response: JSON con el código generado o mensaje de error.
"""
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        if not data:
            print("[ERROR] JSON vacío recibido en la API")
            return jsonify({"error": "Solicitud inválida, JSON vacío."}), 400

        email = data.get('email')
        if not email:
            print("[ERROR] No se recibió un correo en la solicitud")
            return jsonify({"error": "El correo electrónico es obligatorio."}), 400

        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            print("[ERROR] El correo no está registrado:", email)
            return jsonify({"error": "El correo no está registrado."}), 404

        # Generar código de recuperación
        recovery_code = ''.join(random.choices(string.digits, k=6))
        cursor.execute("UPDATE usuarios SET recovery_code = %s WHERE email = %s", (recovery_code, email))
        cnx.commit()

        print("[INFO] Código de recuperación generado correctamente:", recovery_code)
        return jsonify({"message": "Código de recuperación generado.", "recovery_code": recovery_code}), 200

    except Exception as e:
        print(f"[ERROR] Excepción en forgot_password: {e}")
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        cnx.close()


"""
Actualiza el nombre de usuario o la contraseña de un usuario.

Requiere validación de contraseña actual para cambios sensibles.

Returns:
    Response: Mensaje de éxito o error.
"""
@app.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    user_id = data.get('user_id')
    new_username = data.get('username')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')

    if not user_id:
        return jsonify({'error': 'Se requiere el ID del usuario'}), 400
    
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # Actualizar el nombre de usuario si se proporciona
        if new_username:
            cursor.execute("UPDATE usuarios SET username = %s WHERE id = %s", (new_username, user_id))
        
        # Cambiar la contraseña si se proporciona
        if current_password and new_password and confirm_password:
            stored_password = user['password'].encode('utf-8')
            if not bcrypt.checkpw(current_password.encode('utf-8'), stored_password):
                return jsonify({'error': 'Contraseña actual incorrecta'}), 401
            if new_password != confirm_password:
                return jsonify({'error': 'Las contraseñas nuevas no coinciden'}), 400
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute("UPDATE usuarios SET password = %s WHERE id = %s", (hashed_password.decode('utf-8'), user_id))
        
        cnx.commit()
        return jsonify({'message': 'Perfil actualizado correctamente'}), 200
        
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Sube y guarda una imagen de perfil para el usuario.

Guarda la imagen en el sistema de archivos y actualiza su referencia en la base de datos.

Returns:
    Response: Ruta del archivo subido o error.
"""
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload-profile-picture', methods=['POST'])
def upload_profile_picture():
    """Subir una foto de perfil para un usuario."""
    if 'file' not in request.files or 'user_id' not in request.form:
        return jsonify({'error': 'Archivo de imagen y user_id requeridos'}), 400
    
    file = request.files['file']
    user_id = request.form['user_id']
    
    if file.filename == '':
        return jsonify({'error': 'Nombre de archivo inválido'}), 400
    
    # Guardar solo el nombre del archivo en la BD
    filename = secure_filename(f"user_{user_id}.jpg")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        # Guardar solo el nombre del archivo en la BD, no la ruta completa
        cursor.execute("UPDATE usuarios SET profile_picture = %s WHERE id = %s", (filename, user_id))
        cnx.commit()
        
        return jsonify({'message': 'Foto de perfil actualizada', 'file_path': f"http://localhost:5000/uploads/{filename}"}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Obtiene la información pública de un usuario.

Args:
    user_id (int): ID del usuario.

Returns:
    Response: JSON con username, email y foto de perfil.
"""
@app.route('/get-user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT username, email, profile_picture FROM usuarios WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        # Verificar si hay foto de perfil guardada
        if user["profile_picture"]:
            # Asegurarse que siempre se construya correctamente la URL
            user["profile_picture"] = f"http://localhost:5000/uploads/{user['profile_picture']}"
        else:
            # Devolver la imagen por defecto si no hay personalizada
            user["profile_picture"] = "images/b_usuario.png"

        return jsonify(user), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Agrega un nuevo producto al inventario.

Recibe nombre, estado, cantidad y categoría.

Returns:
    Response: Mensaje de confirmación o error.
"""
@app.route('/productos/agregar', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    estado = data.get('estado')
    cantidad = data.get('cantidad')
    categoria = data.get('categoria')
    
    if not all([nombre, estado, cantidad, categoria]):
        return jsonify({'error': 'Faltan campos obligatorios.'}), 400

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        sql = "INSERT INTO productos (nombre, estado, cantidad, categoria) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nombre, estado, cantidad, categoria))
        cnx.commit()
        return jsonify({'message': 'Producto agregado correctamente.'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Edita la información de un producto existente.

Args:
    id (int): ID del producto a editar.

Returns:
    Response: Mensaje de éxito o error.
"""
@app.route('/productos/editar/<int:id>', methods=['PUT'])
def editar_producto(id):
    data = request.get_json()
    nombre = data.get('nombre')
    cantidad = data.get('cantidad')
    estado = data.get('estado')

    if not all([nombre, cantidad, estado]):
        return jsonify({'error': 'Faltan campos obligatorios.'}), 400

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
        producto = cursor.fetchone()

        if not producto:
            return jsonify({'error': 'Producto no encontrado.'}), 404

        # Actualizar el producto
        sql = "UPDATE productos SET nombre = %s, cantidad = %s, estado = %s WHERE id = %s"
        cursor.execute(sql, (nombre, cantidad, estado, id))
        cnx.commit()

        return jsonify({'message': 'Producto actualizado correctamente.'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Devuelve un listado completo de productos en el inventario.

Returns:
    Response: Lista de productos en formato JSON.
"""
@app.route('/productos/listar', methods=['GET'])
def listar_productos():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        return jsonify(productos), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Asigna múltiples productos a distintas direcciones.

Actualiza el stock y crea registros en la tabla `salidas_stock`.

Returns:
    Response: Mensaje de éxito o error.
"""
@app.route('/productos/asignar_multiples', methods=['POST'])
def asignar_multiples_productos():
    try:
        data = request.get_json()
        asignaciones = data.get('asignaciones')
        
        if not asignaciones:
            return jsonify({'error': 'No se recibieron asignaciones válidas.'}), 400
        
        cnx = get_db_connection()
        cursor = cnx.cursor()
        
        for asignacion in asignaciones:
            producto_id = asignacion.get('producto_id')
            cantidad = asignacion.get('cantidad')
            destino = asignacion.get('direccion')

            # Validar datos
            if not producto_id or not cantidad or not destino:
                continue

            # Obtener cantidad disponible del producto
            cursor.execute("SELECT cantidad FROM productos WHERE id = %s", (producto_id,))
            producto = cursor.fetchone()

            if not producto:
                return jsonify({'error': f'Producto con ID {producto_id} no encontrado.'}), 404

            cantidad_disponible = producto[0]

            if cantidad > cantidad_disponible:
                return jsonify({'error': f'No hay suficiente stock del producto con ID {producto_id}'}), 400

            # Restar stock y añadir a salida de stock
            cursor.execute("UPDATE productos SET cantidad = cantidad - %s WHERE id = %s", (cantidad, producto_id))
            cursor.execute(
                "INSERT INTO salidas_stock (producto_id, cantidad, destino, estado) "
                "VALUES (%s, %s, %s, 'Nuevo')",
                (producto_id, cantidad, destino)
            )
        
        cnx.commit()
        return jsonify({'message': 'Productos asignados correctamente.'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Elimina un producto del inventario.

Args:
    id (int): ID del producto a eliminar.

Returns:
    Response: Confirmación o mensaje de error.
"""

@app.route('/productos/eliminar/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        cnx.commit()
        return jsonify({'message': 'Producto eliminado correctamente.'}), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Exporta el inventario actual de productos a un archivo Excel.

Returns:
    Response: Archivo Excel generado como descarga.
"""
@app.route('/productos/exportar', methods=['GET'])
def exportar_stock():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        df = pd.DataFrame(productos)
        file_path = "stock_export.xlsx"
        df.to_excel(file_path, index=False)
        return send_file(file_path, as_attachment=True)
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Lista todas las salidas de stock filtradas por categoría.

Returns:
    Response: Lista de salidas con información del producto.
"""
@app.route('/salidas/listar', methods=['GET'])
def listar_salidas():
    try:
        categoria = request.args.get("categoria")
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """
            SELECT 
                s.id, 
                s.producto_id,
                p.nombre AS producto, 
                s.cantidad, 
                s.destino AS direccion,
                s.fecha_salida,
                s.estado
            FROM salidas_stock s
            JOIN productos p ON s.producto_id = p.id
            WHERE p.categoria = %s
        """
        cursor.execute(query, (categoria,))
        salidas = cursor.fetchall()
        return jsonify(salidas), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Devuelve un producto al almacén restando de la salida actual.

Args:
    id (int): ID de la salida registrada.

Returns:
    Response: Cantidad actualizada o mensaje de error.
"""
@app.route('/salidas/devolver/<int:id>', methods=['PUT'])
def devolver_producto(id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Obtener información actual de la salida
        cursor.execute("SELECT producto_id, cantidad FROM salidas_stock WHERE id = %s", (id,))
        salida = cursor.fetchone()

        if not salida:
            return jsonify({'error': 'Salida no encontrada.'}), 404

        producto_id, cantidad_actual = salida
        data = request.get_json()
        cantidad_devolver = data.get('cantidad')

        if not cantidad_devolver or cantidad_devolver <= 0:
            return jsonify({'error': 'Cantidad no válida.'}), 400

        if cantidad_devolver > cantidad_actual:
            return jsonify({'error': 'No puedes devolver más cantidad de la que salió.'}), 400

        # 1. Actualizar stock del producto
        cursor.execute("UPDATE productos SET cantidad = cantidad + %s WHERE id = %s", (cantidad_devolver, producto_id))

        # 2. Actualizar la salida
        nueva_cantidad = cantidad_actual - cantidad_devolver

        if nueva_cantidad == 0:
            cursor.execute("DELETE FROM salidas_stock WHERE id = %s", (id,))
        else:
            cursor.execute("UPDATE salidas_stock SET cantidad = %s WHERE id = %s", (nueva_cantidad, id))

        cnx.commit()
        return jsonify({
            'message': 'Producto devuelto correctamente.',
            'nueva_cantidad': nueva_cantidad
        }), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()


"""
Elimina parcialmente o completamente una salida de stock.

Args:
    id (int): ID del movimiento de salida.

Returns:
    Response: Estado de la eliminación.
"""
@app.route('/salidas/eliminar/<int:id>', methods=['DELETE'])
def eliminar_salida(id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        data = request.get_json()
        cantidad_a_eliminar = data.get('cantidad')

        # Obtener cantidad actual
        cursor.execute("SELECT cantidad FROM salidas_stock WHERE id = %s", (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Salida no encontrada'}), 404

        cantidad_actual = result[0]

        if cantidad_a_eliminar <= 0 or cantidad_a_eliminar > cantidad_actual:
            return jsonify({'error': 'Cantidad inválida'}), 400

        nueva_cantidad = cantidad_actual - cantidad_a_eliminar

        if nueva_cantidad == 0:
            cursor.execute("DELETE FROM salidas_stock WHERE id = %s", (id,))
        else:
            cursor.execute("UPDATE salidas_stock SET cantidad = %s WHERE id = %s", (nueva_cantidad, id))

        cnx.commit()
        return jsonify({
            'message': 'Producto eliminado correctamente',
            'nueva_cantidad': nueva_cantidad
        }), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        cnx.close()
        
# Endpoint para Servir Archivos de Imágenes guardadas
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


"""
Lista todos los movimientos de productos (entrada y salida).

Se puede filtrar por categoría.

Returns:
    Response: Lista de movimientos.
"""
@app.route('/historial/listar', methods=['GET'])
def listar_historial_movimientos():
    try:
        categoria = request.args.get('categoria')
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT 
                h.id,
                h.tipo_movimiento,
                h.cantidad,
                h.fecha_movimiento,
                h.direccion,
                h.detalles,
                p.nombre AS producto,
                u.username AS usuario
            FROM historial_movimientos h
            JOIN productos p ON h.producto_id = p.id
            LEFT JOIN usuarios u ON h.usuario_id = u.id
        """

        params = []
        if categoria:
            query += " WHERE p.categoria = %s"
            params.append(categoria)

        query += " ORDER BY h.fecha_movimiento DESC"

        cursor.execute(query, tuple(params))
        movimientos = cursor.fetchall()
        return jsonify(movimientos), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        cnx.close()


"""
Elimina un movimiento del historial.

Args:
    id (int): ID del movimiento.

Returns:
    Response: Confirmación de eliminación.
"""
@app.route('/historial/eliminar/<int:id>', methods=['DELETE'])
def eliminar_movimiento(id):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()

        # Verificamos si existe
        cursor.execute("SELECT id FROM historial_movimientos WHERE id = %s", (id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Movimiento no encontrado.'}), 404

        cursor.execute("DELETE FROM historial_movimientos WHERE id = %s", (id,))
        cnx.commit()
        return jsonify({'message': 'Movimiento eliminado correctamente.'}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        cnx.close()


"""
Registra un movimiento (entrada o salida) en el historial.

Requiere: producto_id, tipo_movimiento, cantidad.

Returns:
    Response: Mensaje de éxito o error.
"""
@app.route('/historial/registrar', methods=['POST'])
def registrar_movimiento():
    data = request.get_json()
    print("[DEBUG] Datos recibidos para historial:", data)
    producto_id = data.get('producto_id')
    tipo_movimiento = data.get('tipo_movimiento')  # "Entrada" o "Salida"
    cantidad = data.get('cantidad')
    usuario_id = data.get('usuario_id') if 'usuario_id' in data else None
    direccion = data.get('direccion')
    detalles = data.get('detalles', '')

    if not all([producto_id, tipo_movimiento, cantidad]):
        return jsonify({'error': 'Faltan campos obligatorios.'}), 400

    try:
        cnx = get_db_connection()
        cursor = cnx.cursor()
        cursor.execute("""
            INSERT INTO historial_movimientos (
                producto_id, tipo_movimiento, cantidad, usuario_id, direccion, detalles
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (producto_id, tipo_movimiento, cantidad, usuario_id, direccion, detalles))

        cnx.commit()
        return jsonify({'message': 'Movimiento registrado correctamente.'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500

    finally:
        cursor.close()
        cnx.close()


"""
Exporta el historial completo de movimientos a Excel.

Returns:
    Response: Archivo Excel descargable.
"""
@app.route('/historial/exportar', methods=['GET'])
def exportar_historial():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                h.id,
                h.tipo_movimiento,
                h.cantidad,
                h.fecha_movimiento,
                h.direccion,
                h.detalles,
                p.nombre AS producto
            FROM historial_movimientos h
            JOIN productos p ON h.producto_id = p.id
            ORDER BY h.fecha_movimiento DESC
        """)
        historial = cursor.fetchall()

        df = pd.DataFrame(historial)

        file_path = "historial_export.xlsx"
        df.to_excel(file_path, index=False)

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


"""
Asegura que todas las respuestas del servidor sean en formato JSON.

Args:
    response (Response): Respuesta original de Flask.

Returns:
    Response: Respuesta modificada con headers.
"""
@app.after_request
def add_headers(response):
    response.headers["Content-Type"] = "application/json"
    return response