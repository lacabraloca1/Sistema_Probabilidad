CREATE DATABASE IF NOT EXISTS sistema_escolar;
USE sistema_escolar;

-- Tabla de Alumnos
CREATE TABLE IF NOT EXISTS Alumnos (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) DEFAULT 'N/A',
    fecha_nacimiento DATE DEFAULT NULL,
    email_correo VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de Materias
CREATE TABLE IF NOT EXISTS Materias (
    materia_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    creditos INT DEFAULT 100 CHECK (creditos BETWEEN 0 AND 100) -- ✅ Limite de 0 a 100 créditos
);

-- Tabla de Cuatrimestres
CREATE TABLE IF NOT EXISTS Cuatrimestre (
    cuatrimestre_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla de Inscripciones de Alumnos
CREATE TABLE IF NOT EXISTS Inscripcion_Alumnos (
    inscripcion_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    materia_id INT NOT NULL,
    cuatrimestre_id INT NOT NULL,
    estatus ENUM('cursando', 'aprobado', 'reprobado', 'retirado') DEFAULT 'cursando',
    FOREIGN KEY (usuario_id) REFERENCES Alumnos(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES Materias(materia_id) ON DELETE CASCADE,
    FOREIGN KEY (cuatrimestre_id) REFERENCES Cuatrimestre(cuatrimestre_id) ON DELETE CASCADE
);

-- Tabla de Calificaciones
CREATE TABLE IF NOT EXISTS Calificaciones (
    calificaciones_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    materia_id INT NOT NULL,
    cuatrimestre_id INT NOT NULL,
    primer_parcial FLOAT CHECK (primer_parcial BETWEEN 0 AND 100),  -- ✅ Límite de 0 a 100
    segundo_parcial FLOAT CHECK (segundo_parcial BETWEEN 0 AND 100), -- ✅ Límite de 0 a 100
    tercer_parcial FLOAT CHECK (tercer_parcial BETWEEN 0 AND 100),  -- ✅ Límite de 0 a 100
    calificacion_final FLOAT CHECK (calificacion_final BETWEEN 0 AND 100), -- ✅ Límite de 0 a 100
    FOREIGN KEY (usuario_id) REFERENCES Alumnos(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES Materias(materia_id) ON DELETE CASCADE,
    FOREIGN KEY (cuatrimestre_id) REFERENCES Cuatrimestre(cuatrimestre_id) ON DELETE CASCADE
);

-- Restablecer AUTO_INCREMENT después de eliminación
ALTER TABLE Alumnos AUTO_INCREMENT = 1;
ALTER TABLE Materias AUTO_INCREMENT = 1;
ALTER TABLE Cuatrimestre AUTO_INCREMENT = 1;
ALTER TABLE Inscripcion_Alumnos AUTO_INCREMENT = 1;
ALTER TABLE Calificaciones AUTO_INCREMENT = 1;
