CREATE DATABASE IF NOT EXISTS db_inmuebles;

ALTER TABLE usuarios ADD COLUMN profile_picture VARCHAR(255) NULL;
ALTER TABLE usuarios ADD COLUMN recovery_code VARCHAR(6) NULL;
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    estado ENUM('Nuevo', 'Usado', 'Dañado') NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad >= 0),
    categoria ENUM('Habitaciones', 'Electrodomésticos', 'Zonas Comunes', 'Baños') NOT NULL,
    fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS salidas_stock (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    destino VARCHAR(255) NOT NULL,
    estado ENUM('Nuevo', 'Usado', 'Dañado') NOT NULL,
    fecha_salida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS historial_movimientos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT NOT NULL,
    tipo_movimiento ENUM('Entrada', 'Salida') NOT NULL,
    cantidad INT NOT NULL,
    usuario_id INT,
    direccion VARCHAR(255), -- NULL para entradas
    fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);
