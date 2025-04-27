CREATE DATABASE IF NOT EXISTS db_inmuebles;
USE db_inmuebles;

DROP TABLE IF EXISTS `productos`;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `estado` enum('Nuevo','Usado','Dañado') NOT NULL,
  `cantidad` int NOT NULL,
  `categoria` enum('Habitaciones','Electrodomésticos','Zonas Comunes','Baños') NOT NULL,
  `fecha_ingreso` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  CONSTRAINT `productos_chk_1` CHECK ((`cantidad` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `productos` WRITE;
INSERT INTO `productos` VALUES (3,'Sábanas','Nuevo',37,'Habitaciones','2025-03-04 08:20:44'),(4,'Lámpara','Usado',21,'Habitaciones','2025-03-04 08:52:50'),(5,'Cortinas','Nuevo',18,'Habitaciones','2025-03-05 09:04:16'),(7,'Mesita de Noche','Usado',2,'Habitaciones','2025-03-15 21:28:06'),(8,'Colchones','Usado',25,'Habitaciones','2025-03-15 21:30:32'),(9,'Perchero','Nuevo',9,'Habitaciones','2025-03-15 21:31:34'),(13,'Cómodas','Usado',32,'Habitaciones','2025-03-23 11:38:14'),(14,'Escritorio','Nuevo',14,'Habitaciones','2025-03-23 11:38:51'),(15,'Sillas','Nuevo',60,'Habitaciones','2025-03-23 11:39:30'),(16,'Tostadora','Nuevo',10,'Electrodomésticos','2025-03-29 21:39:44'),(17,'Cafetera','Nuevo',20,'Electrodomésticos','2025-03-29 21:45:05'),(18,'Labadora','Nuevo',23,'Electrodomésticos','2025-03-29 21:46:20'),(19,'Microondas','Usado',46,'Electrodomésticos','2025-03-29 21:46:56'),(20,'Batidora','Nuevo',51,'Electrodomésticos','2025-03-29 21:47:39'),(21,'Airfrier','Nuevo',24,'Electrodomésticos','2025-03-29 21:48:00'),(22,'Lámpara','Usado',30,'Zonas Comunes','2025-03-30 07:34:46'),(23,'Mesas','Nuevo',40,'Zonas Comunes','2025-03-30 07:35:25'),(24,'Sillas','Nuevo',26,'Zonas Comunes','2025-03-30 07:36:35'),(25,'Espejo','Nuevo',24,'Baños','2025-03-30 07:37:27'),(26,'Plato de ducha','Nuevo',2,'Baños','2025-03-30 07:38:27'),(27,'Toallas','Nuevo',20,'Baños','2025-03-31 06:45:37'),(28,'Gel de Baño','Nuevo',100,'Baños','2025-03-31 06:46:11'),(29,'Cortinas de Baño','Usado',40,'Baños','2025-03-31 06:46:43'),(30,'Alfombrillas','Nuevo',50,'Baños','2025-03-31 06:47:22'),(31,'Cepillo de Dientes','Nuevo',69,'Baños','2025-03-31 06:48:16'),(32,'Acondicionador','Nuevo',40,'Baños','2025-03-31 06:48:42'),(33,'Esponjas','Nuevo',120,'Baños','2025-03-31 06:49:15'),(34,'Lavavajillas','Usado',12,'Electrodomésticos','2025-03-31 06:51:46'),(35,'Plancha','Usado',31,'Electrodomésticos','2025-03-31 06:53:46'),(36,'Secadora','Nuevo',38,'Electrodomésticos','2025-03-31 06:54:20'),(37,'Alfombras','Usado',42,'Zonas Comunes','2025-03-31 06:59:22'),(38,'Estanterias','Usado',40,'Zonas Comunes','2025-03-31 07:01:13'),(39,'Papelera','Nuevo',30,'Zonas Comunes','2025-03-31 07:01:54'),(40,'TV','Usado',104,'Zonas Comunes','2025-03-31 07:02:31'),(41,'Muebles de Sala','Usado',24,'Zonas Comunes','2025-03-31 07:03:46'),(42,'Sillón','Usado',40,'Zonas Comunes','2025-03-31 07:04:20');
UNLOCK TABLES;


DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `recovery_code` varchar(6) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `usuarios` WRITE;
INSERT INTO `usuarios` VALUES (3,'Juan','juan@gmail.com','$2b$12$w4t3KmDxZqmdojY1J9drRerS85AG839SnTdv7mzEyJqQ940cL2qBC',NULL,NULL),(5,'mariotc1','m@gmail.com','$2b$12$R5zWxUjOayTYfKbVvwPEGOmq492wPAOpKlfDlJY8MIeWpNQN.EV4O',NULL,'user_5.jpg'),(7,'Claudia','clau@gmail.com','$2b$12$2zZhVZlyQ.LI4ogv6vItkeJCSsPumDokYZsvFyCSi5VhJDgySyQJy',NULL,NULL),(9,'gredos','elgredos13@gmail.com','$2b$12$/hyO261ammZ5o9gwa0sPrODYymdjPKlyMKGSsDupNYjso2m4jdrFm',NULL,NULL),(10,'Avantia','avantiacrm@gmail.com','$2b$12$qwy5rac2V.5Baim/Kb/fcuv9ol6dSkXSaOUadF0kSU3W16n5tp9nm',NULL,NULL),(11,'Clau','ruizcabclaudia@gmail.com','$2b$12$AXlJyXklJBvWKfRpNbp7aeB72UDC3xSFJeJ6n2S7vpmlWjMs6lCcG',NULL,NULL),(12,'taller','infotallerapp@gmail.com','$2b$12$B60jHUCqWzv15hi/VE6O.e90.mD.OnVvpQdlIF49oPkflYa379YRW',NULL,NULL),(13,'nico','nico@gmail.com','$2b$12$yoUWgvWsf/Cr5wF.vOs51.5RbSRX9N77Vhh5inxLUJiCAeVtOvoBm',NULL,NULL),(14,'alejandro','afroeros22@gmail.com','$2b$12$.hYZUIKx1jOqePsUNQhVZ.sN5tpJ9SDsdSuFivLSRRTJaB9dtjOJ.',NULL,NULL),(15,'mario','mario.tome@serbatic.es','$2b$12$JavX2AS8/4GCyNO58Smt7.0.IQrSZWmjXi2qccJOUWpqsq8XOwVW.',NULL,'user_15.jpg'),(17,'mariooo:)','mario.tomcor@sanviatorvalladolid.com','$2b$12$5CIBTCRuS9bwsKleep8L5O5AYZOh2ZGadcEITW7sW8eqKCTwKdLPy',NULL,'user_17.jpg'),(18,'Sonia','scavila@hotmail.com','$2b$12$ZC9wHBiUnnOsqX/uTSt2NOe6wPcjQ3t.W/O8JI56eJZ6xrFt1zqpK',NULL,NULL),(20,'Sara','2010saratc@gmail.com','$2b$12$s/90Tss2JRj6Go7d4TSf/OdVtP0Hbnqy30Q0f3.P.lr4DgWU6O8Oe',NULL,NULL),(21,'prueba','p@gmail.com','$2b$12$u4b6gBRanhKDvo9.cDbHoe2C.mZKNZ7WXmKWYTsVKe95bzNEvJI/S',NULL,NULL),(22,'Prueba2','p2@gmail.com','$2b$12$3JZPnsKm6jdO/matGJGkUeQfBCepoS4vHJqIf3S87EWarPCvW1Rlm',NULL,NULL),(23,'Prueba 3','p3@gmail.com','$2b$12$PW0FlTbrEQMGfFC9/JpRkOH4z4eisWW8F.qojC42lMLpgj.ZJqkNO',NULL,NULL),(28,'Mario Tomé Core','mariotomecore@gmail.com','$2b$12$YivkNGC9fkAsKgwvm3f6oObjMYL8MRlAPwV9wNlDkK7R8FSar59pS','375421',NULL),(29,'Prueba Tema Negro','ptn@gmail.com','$2b$12$f5xIOgMcjgbDfcWLcQEEyuByQiYJ.BEe.SRYcNuveas0M9ZuGk7Be',NULL,NULL),(30,'Prueba Tema Claro','ptc@gmail.com','$2b$12$I3tPx3vtNd9Qh0/S4/nZiut996xHLrZcXRyLXNnY.HBiXgldLS6gu',NULL,NULL),(31,'pvbipur','ewnowdv@weoigvnr.com','$2b$12$Qy9gFRMNRDDSOQ.z../7celmKZkJyQ99hlz.IkUlUTIDONrsEjTgC',NULL,NULL),(32,'ewfjvpvmd','mw@gmail.com','$2b$12$Y0Sl76E3l4FHIpMTcFVi2.ejzZ/fWw17vtv5l4Frse/7HxPtaAT02',NULL,NULL),(33,'wd','wdc@gmail.com','$2b$12$bSskz9fIHk1Viw4ykyn.f.BsGcXZ5KkPxCeoP9yLgNk4Mzityc0.2',NULL,NULL),(34,'Pruebas','p23@gmail.com','$2b$12$7UgiORTMHR8FHaRmol2bDe0Qj6L9D6TU4TVnTcd2DScsc/QDmmWUi',NULL,NULL);
UNLOCK TABLES;


DROP TABLE IF EXISTS `historial_movimientos`;
CREATE TABLE `historial_movimientos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `tipo_movimiento` enum('Entrada','Salida') NOT NULL,
  `cantidad` int NOT NULL,
  `usuario_id` int DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `fecha_movimiento` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `detalles` text,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `historial_movimientos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `historial_movimientos_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `historial_movimientos` WRITE;
INSERT INTO `historial_movimientos` VALUES (3,15,'Entrada',1,NULL,'Calle Inventada','2025-03-29 12:39:19','Devolución desde ReturnProductDialog'),(4,14,'Entrada',1,NULL,'Calle Inventada 12, 3F','2025-03-29 12:39:32','Devolución desde ReturnProductDialog'),(5,9,'Salida',4,NULL,'Calle Camaño 12, 3ºD','2025-03-29 12:41:32','Asignación registrada automáticamente'),(6,3,'Salida',10,NULL,'Calle Camaño 12, 3ºD','2025-03-29 12:41:34','Asignación registrada automáticamente'),(10,3,'Entrada',1,NULL,'Calle caballeria. 35-39','2025-03-29 12:52:35','Devolución desde ReturnProductDialog'),(11,3,'Salida',1,NULL,'Calle Ocasina 24, 1ºC','2025-03-29 12:58:13','Asignación registrada automáticamente'),(12,18,'Salida',3,NULL,'Calle Caballeria, 35 2ºF','2025-03-30 07:45:28','Asignación registrada automáticamente'),(13,18,'Entrada',1,NULL,'Calle Caballeria, 35 2ºF','2025-03-30 08:02:06','Devolución desde ReturnProductDialog'),(14,19,'Entrada',2,NULL,'Av. Segovia 16, 2ºC','2025-03-30 08:02:31','Devolución desde ReturnProductDialog'),(15,18,'Entrada',1,NULL,'Calle Caballeria, 35 2ºF','2025-03-30 08:02:45','Devolución desde ReturnProductDialog'),(16,19,'Salida',1,NULL,'Av. Segovia 16, 2ºC','2025-03-30 08:06:14','Eliminación manual de producto desde DeleteSelectedProductDialog'),(17,19,'Salida',14,NULL,'Calle Ejemplo 12, 4ºF','2025-03-30 08:07:20','Asignación registrada automáticamente'),(18,21,'Salida',6,NULL,'Calle Ejemplo 12, 4ºF','2025-03-30 08:07:22','Asignación registrada automáticamente'),(19,19,'Entrada',1,NULL,'Av. Segovia 16, 2ºC','2025-03-30 08:12:47','Devolución desde ReturnProductDialog'),(20,19,'Entrada',2,NULL,'Calle Ejemplo 12, 4ºF','2025-03-30 08:13:04','Devolución desde ReturnProductDialog'),(21,3,'Salida',1,NULL,'Calle ejemplo 13, 4ºA','2025-03-30 19:04:13','Asignación registrada automáticamente'),(22,3,'Salida',1,NULL,'Calle ejemplo 13, 4ºA','2025-03-30 19:06:10','Eliminación manual de producto desde DeleteSelectedProductDialog'),(23,26,'Salida',2,NULL,'Callle Ejemplo 12, 2ºG','2025-03-30 19:26:31','Asignación registrada automáticamente'),(24,25,'Salida',1,NULL,'Callle Ejemplo 12, 2ºG','2025-03-30 19:26:33','Asignación registrada automáticamente'),(25,30,'Salida',12,NULL,'Calle Embajadore 34, 2ºE','2025-03-31 10:14:03','Asignación registrada automáticamente'),(26,25,'Salida',18,NULL,'Calle Embajadore 34, 2ºE','2025-03-31 10:14:05','Asignación registrada automáticamente'),(27,31,'Salida',19,NULL,'Calle Embajadore 34, 2ºE','2025-03-31 10:14:07','Asignación registrada automáticamente'),(28,22,'Salida',12,NULL,'Calle Colón 24, 2ºA','2025-03-31 10:15:44','Asignación registrada automáticamente'),(29,38,'Salida',20,NULL,'Calle Colón 24, 2ºA','2025-03-31 10:15:46','Asignación registrada automáticamente'),(30,23,'Salida',14,NULL,'Calle Colón 24, 2ºA','2025-03-31 10:15:48','Asignación registrada automáticamente'),(31,42,'Salida',4,NULL,'Calle Colón 24, 2ºA','2025-03-31 10:15:51','Asignación registrada automáticamente'),(32,17,'Salida',10,NULL,'Avenida Segovia 19, 3ºB','2025-03-31 10:17:06','Asignación registrada automáticamente'),(33,34,'Salida',12,NULL,'Avenida Segovia 19, 3ºB','2025-03-31 10:17:09','Asignación registrada automáticamente'),(34,36,'Salida',22,NULL,'Avenida Segovia 19, 3ºB','2025-03-31 10:17:11','Asignación registrada automáticamente'),(35,31,'Entrada',4,NULL,'Calle Embajadore 34, 2ºE','2025-04-02 08:58:49','Devolución desde ReturnProductDialog'),(36,23,'Entrada',4,NULL,'Calle Colón 24, 2ºA','2025-04-02 08:59:30','Devolución desde ReturnProductDialog'),(37,38,'Entrada',8,NULL,'Calle Colón 24, 2ºA','2025-04-02 08:59:45','Devolución desde ReturnProductDialog'),(38,3,'Entrada',1,NULL,'Calle Camaño 12, 3ºD','2025-04-04 11:30:38','Devolución desde ReturnProductDialog'),(39,32,'Salida',6,NULL,'Plaza del Carmen 29, 3ºA','2025-04-04 11:32:31','Asignación registrada automáticamente'),(40,38,'Salida',12,NULL,'Acera Recoletas 24, 5ºG','2025-04-04 11:33:48','Asignación registrada automáticamente'),(41,42,'Salida',17,NULL,'Acera Recoletas 24, 5ºG','2025-04-04 11:33:50','Asignación registrada automáticamente'),(42,3,'Salida',1,NULL,'Calle Comprobar Dialofg','2025-04-05 14:48:29','Asignación registrada automáticamente');
UNLOCK TABLES;


DROP TABLE IF EXISTS `salidas_stock`;
CREATE TABLE `salidas_stock` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `destino` varchar(255) NOT NULL,
  `estado` enum('Nuevo','Usado','Dañado') NOT NULL,
  `fecha_salida` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `devuelto` tinyint(1) DEFAULT '0',
  `detalles` text,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `salidas_stock_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `salidas_stock_chk_1` CHECK ((`cantidad` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOCK TABLES `salidas_stock` WRITE;
INSERT INTO `salidas_stock` VALUES (4,3,1,'C// Caballeria 35-39 1B','Nuevo','2025-03-20 08:19:39',0,NULL),(5,4,1,'Calle Embajadores, 2C','Nuevo','2025-03-20 08:38:51',1,NULL),(7,8,1,'Acera Recoletas 14, 4F','Nuevo','2025-03-20 08:46:01',0,NULL),(19,9,2,'Calle Camaño 12, 3ºD','Nuevo','2025-03-29 12:41:30',0,NULL),(20,3,6,'Calle Camaño 12, 3ºD','Nuevo','2025-03-29 12:41:30',0,NULL),(21,3,1,'Calle Ocasina 24, 1ºC','Nuevo','2025-03-29 12:58:10',0,NULL),(22,19,1,'Av. Segovia 16, 2ºC','Nuevo','2025-03-30 07:43:04',0,NULL),(24,19,7,'Calle Ejemplo 12, 4ºF','Nuevo','2025-03-30 08:07:18',0,NULL),(25,21,4,'Calle Ejemplo 12, 4ºF','Nuevo','2025-03-30 08:07:18',0,NULL),(27,26,2,'Callle Ejemplo 12, 2ºG','Nuevo','2025-03-30 19:26:29',0,NULL),(28,25,1,'Callle Ejemplo 12, 2ºG','Nuevo','2025-03-30 19:26:29',0,NULL),(29,30,12,'Calle Embajadore 34, 2ºE','Nuevo','2025-03-31 10:14:01',0,NULL),(30,25,18,'Calle Embajadore 34, 2ºE','Nuevo','2025-03-31 10:14:01',0,NULL),(31,31,15,'Calle Embajadore 34, 2ºE','Nuevo','2025-03-31 10:14:01',0,NULL),(32,22,12,'Calle Colón 24, 2ºA','Nuevo','2025-03-31 10:15:42',0,NULL),(33,38,12,'Calle Colón 24, 2ºA','Nuevo','2025-03-31 10:15:42',0,NULL),(34,23,10,'Calle Colón 24, 2ºA','Nuevo','2025-03-31 10:15:42',0,NULL),(35,42,4,'Calle Colón 24, 2ºA','Nuevo','2025-03-31 10:15:42',0,NULL),(36,17,10,'Avenida Segovia 19, 3ºB','Nuevo','2025-03-31 10:17:04',0,NULL),(37,34,12,'Avenida Segovia 19, 3ºB','Nuevo','2025-03-31 10:17:04',0,NULL),(38,36,22,'Avenida Segovia 19, 3ºB','Nuevo','2025-03-31 10:17:04',0,NULL),(39,32,6,'Plaza del Carmen 29, 3ºA','Nuevo','2025-04-04 11:32:29',0,NULL),(40,38,12,'Acera Recoletas 24, 5ºG','Nuevo','2025-04-04 11:33:46',0,NULL),(41,42,17,'Acera Recoletas 24, 5ºG','Nuevo','2025-04-04 11:33:46',0,NULL),(42,3,1,'Calle Comprobar Dialofg','Nuevo','2025-04-05 14:48:27',0,NULL);
UNLOCK TABLES;