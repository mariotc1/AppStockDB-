-- ---------------------------------------------------------
-- SCRIPT DE CREACIÓN DE LA BASE DE DATOS: db_inmuebles
-- Proyecto: AppGestiónStockDB
-- Autor: Mario Tomé Core
-- Ciclo: DAM - Curso 2024/2025
-- Centro: Colegio San Viator Valladolid
-- Fecha de exportación: 2025-03-28
-- ---------------------------------------------------------
-- Script compatible con MySQL 8.0.35

CREATE DATABASE IF NOT EXISTS db_inmuebles;
USE db_inmuebles;

-- Tabla: usuarios
DROP TABLE IF EXISTS usuarios;

CREATE TABLE usuarios (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  recovery_code VARCHAR(6) DEFAULT NULL,
  profile_picture VARCHAR(255) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Tabla: productos
DROP TABLE IF EXISTS productos;

CREATE TABLE productos (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  estado ENUM('Nuevo','Usado','Dañado') NOT NULL,
  cantidad INT NOT NULL,
  categoria ENUM('Habitaciones','Electrodomésticos','Zonas Comunes','Baños') NOT NULL,
  fecha_ingreso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  CONSTRAINT productos_chk_1 CHECK (cantidad >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Tabla: salidas_stock
DROP TABLE IF EXISTS salidas_stock;

CREATE TABLE salidas_stock (
  id INT NOT NULL AUTO_INCREMENT,
  producto_id INT NOT NULL,
  cantidad INT NOT NULL,
  destino VARCHAR(255) NOT NULL,
  estado ENUM('Nuevo','Usado','Dañado') NOT NULL,
  fecha_salida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  devuelto TINYINT(1) DEFAULT 0,
  detalles TEXT,
  PRIMARY KEY (id),
  KEY producto_id (producto_id),
  CONSTRAINT salidas_stock_ibfk_1 FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
  CONSTRAINT salidas_stock_chk_1 CHECK (cantidad > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- Tabla: historial_movimientos
DROP TABLE IF EXISTS historial_movimientos;

CREATE TABLE historial_movimientos (
  id INT NOT NULL AUTO_INCREMENT,
  producto_id INT NOT NULL,
  tipo_movimiento ENUM('Entrada','Salida') NOT NULL,
  cantidad INT NOT NULL,
  usuario_id INT DEFAULT NULL,
  direccion VARCHAR(255) DEFAULT NULL,
  fecha_movimiento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  detalles TEXT,
  PRIMARY KEY (id),
  KEY producto_id (producto_id),
  KEY usuario_id (usuario_id),
  CONSTRAINT historial_movimientos_ibfk_1 FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE,
  CONSTRAINT historial_movimientos_ibfk_2 FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;