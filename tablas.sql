USE click_construir;
GO

--  TABLA ROLES
CREATE TABLE roles (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(50) NOT NULL
);

--  TABLA USUARIOS
CREATE TABLE usuarios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    correo NVARCHAR(100) UNIQUE NOT NULL,
    contrasena NVARCHAR(100) NOT NULL,
    telefono NVARCHAR(20),
    id_rol INT,
    FOREIGN KEY (id_rol) REFERENCES roles(id)
);

--  TABLA CATEGORIAS
CREATE TABLE categorias (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(200)
);

--  TABLA PROYECTOS
CREATE TABLE proyectos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo NVARCHAR(100) NOT NULL,
    descripcion NVARCHAR(MAX),
    presupuesto DECIMAL(10,2),
    ubicacion NVARCHAR(100),
    fecha_publicacion DATETIME DEFAULT GETDATE(),
    estado NVARCHAR(50) DEFAULT 'abierto',
    id_usuario INT,
    id_categoria INT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_categoria) REFERENCES categorias(id)
);

--  TABLA COTIZACIONES
CREATE TABLE cotizaciones (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_proyecto INT,
    id_trabajador INT,
    valor DECIMAL(10,2),
    descripcion NVARCHAR(MAX),
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id),
    FOREIGN KEY (id_trabajador) REFERENCES usuarios(id)
);

--  TABLA CALIFICACIONES
CREATE TABLE calificaciones (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT,          -- quien recibe la calificación
    id_calificador INT,      -- quien califica
    puntuacion INT CHECK (puntuacion BETWEEN 1 AND 5),
    comentario NVARCHAR(300),
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_calificador) REFERENCES usuarios(id)
);

--  TABLA COMENTARIOS 
CREATE TABLE comentarios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    id_proyecto INT,
    id_usuario INT,
    contenido NVARCHAR(300),
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_proyecto) REFERENCES proyectos(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);