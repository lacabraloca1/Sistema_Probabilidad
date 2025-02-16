CREATE DATABASE sistema_escolar_db;
USE sistema_escolar_db;

-- Tabla de Alumnos
CREATE TABLE Alumnos (
    usuario_id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50),
    fecha_nacimiento DATE NOT NULL,
    email_correo VARCHAR(100) UNIQUE NOT NULL
);

-- Tabla de Grupos
CREATE TABLE Grupos (
    grupos_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    turno ENUM('Matutino', 'Vespertino', 'Nocturno') NOT NULL
);

-- Tabla de Cuatrimestres
CREATE TABLE Cuatrimestre (
    cuatrimestre_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL
);

-- Tabla de Materias
CREATE TABLE Materias (
    materia_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    creditos INT NOT NULL CHECK (creditos > 0)
);

-- Relación Alumnos-Grupo-Cuatrimestre
CREATE TABLE Alumnos_Grupos_Cuatrimestre (
    asignacion_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    grupo_cuatri_id INT,
    FOREIGN KEY (usuario_id) REFERENCES Alumnos(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (grupo_cuatri_id) REFERENCES Grupos(grupos_id) ON DELETE CASCADE
);

-- Relación Materias-Cuatrimestre
CREATE TABLE Materias_Cuatrimestre (
    materia_id INT,
    cuatrimestre_id INT,
    PRIMARY KEY (materia_id, cuatrimestre_id),
    FOREIGN KEY (materia_id) REFERENCES Materias(materia_id) ON DELETE CASCADE,
    FOREIGN KEY (cuatrimestre_id) REFERENCES Cuatrimestre(cuatrimestre_id) ON DELETE CASCADE
);

-- Inscripción de Alumnos en Materias
CREATE TABLE Inscripcion_Alumnos (
    inscripcion_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    materia_id INT,
    cuatrimestre_id INT,
    estatus ENUM('Cursando', 'Aprobado', 'Reprobado') DEFAULT 'Cursando',
    FOREIGN KEY (usuario_id) REFERENCES Alumnos(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES Materias(materia_id) ON DELETE CASCADE,
    FOREIGN KEY (cuatrimestre_id) REFERENCES Cuatrimestre(cuatrimestre_id) ON DELETE CASCADE
);

-- Tabla de Calificaciones
CREATE TABLE Calificaciones (
    calificaciones_id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    materia_id INT,
    cuatrimestre_id INT,
    primer_parcial DECIMAL(4,2) CHECK (primer_parcial >= 0 AND primer_parcial <= 10),
    segundo_parcial DECIMAL(4,2) CHECK (segundo_parcial >= 0 AND segundo_parcial <= 10),
    tercer_parcial DECIMAL(4,2) CHECK (tercer_parcial >= 0 AND tercer_parcial <= 10),
    calificacion_final DECIMAL(4,2) GENERATED ALWAYS AS ((primer_parcial + segundo_parcial + tercer_parcial) / 3) STORED,
    estatus ENUM('Aprobado', 'Reprobado') GENERATED ALWAYS AS (CASE WHEN calificacion_final >= 7 THEN 'Aprobado' ELSE 'Reprobado' END) STORED,
    FOREIGN KEY (usuario_id) REFERENCES Alumnos(usuario_id) ON DELETE CASCADE,
    FOREIGN KEY (materia_id) REFERENCES Materias(materia_id) ON DELETE CASCADE,
    FOREIGN KEY (cuatrimestre_id) REFERENCES Cuatrimestre(cuatrimestre_id) ON DELETE CASCADE
);
