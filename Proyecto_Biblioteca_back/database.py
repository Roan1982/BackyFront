import os
import mysql.connector
from flask import g
from dotenv import load_dotenv

# Obtener la ruta del directorio actual
d = os.path.dirname(__file__)
os.chdir(d)

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la base de datos usando variables de entorno
DATABASE_CONFIG = {
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 3306)
}

# Función para obtener la conexión de la base de datos
def get_db():
    if 'db' not in g:
        print("···· Abriendo conexión a la base de datos ····")
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    return g.db

# Función para cerrar la conexión a la base de datos
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print("···· Cerrando conexión a la base de datos ····")
        db.close()

# Función para inicializar la base de datos
def init_db():
    db = get_db()
    cursor = db.cursor()

    # Crear tablas si no existen con todas las claves e índices incluidos
    sql_commands = [
        """CREATE TABLE IF NOT EXISTS roles (
            id INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(50) NOT NULL,
            descripcion VARCHAR(255) DEFAULT NULL,
            PRIMARY KEY (id),
            UNIQUE KEY nombre (nombre)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        """CREATE TABLE IF NOT EXISTS usuarios (
            id_usuario INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            apellido VARCHAR(100) NOT NULL,
            username VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            fecha_nacimiento DATE NOT NULL,
            fecha_registro TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
            genero VARCHAR(20) NOT NULL,
            pais VARCHAR(100) DEFAULT NULL,
            password VARCHAR(255) NOT NULL,
            rol_id INT DEFAULT NULL,
            PRIMARY KEY (id_usuario),
            UNIQUE KEY username (username),
            UNIQUE KEY email (email),
            KEY fk_rol (rol_id),
            CONSTRAINT fk_rol FOREIGN KEY (rol_id) REFERENCES roles (id)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        """CREATE TABLE IF NOT EXISTS generos_literarios (
            genero_id INT NOT NULL AUTO_INCREMENT,
            nombre_genero VARCHAR(100) NOT NULL,
            PRIMARY KEY (genero_id)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        """CREATE TABLE IF NOT EXISTS autores (
            autor_id INT NOT NULL AUTO_INCREMENT,
            nombre VARCHAR(100) NOT NULL,
            apellidos VARCHAR(100) NOT NULL,
            nacionalidad VARCHAR(50) DEFAULT NULL,
            PRIMARY KEY (autor_id)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        """CREATE TABLE IF NOT EXISTS libros (
            libro_id INT NOT NULL AUTO_INCREMENT,
            titulo VARCHAR(255) NOT NULL,
            autor_id INT DEFAULT NULL,
            genero_id INT DEFAULT NULL,
            anio_publicacion INT DEFAULT NULL,
            imagen VARCHAR(255) DEFAULT NULL,
            resenia TEXT,
            pdf VARCHAR(255) DEFAULT NULL,
            PRIMARY KEY (libro_id),
            KEY autor_id (autor_id),
            KEY genero_id (genero_id),
            CONSTRAINT libros_ibfk_1 FOREIGN KEY (autor_id) REFERENCES autores (autor_id),
            CONSTRAINT libros_ibfk_2 FOREIGN KEY (genero_id) REFERENCES generos_literarios (genero_id)
        ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;""",
        
        """CREATE TABLE IF NOT EXISTS opiniones (
            opinion_id INT NOT NULL AUTO_INCREMENT,
            libro_id INT DEFAULT NULL,
            opinion_texto TEXT,
            puntaje INT DEFAULT NULL,
            fecha_opinion DATE DEFAULT NULL,
            PRIMARY KEY (opinion_id),
            KEY libro_id (libro_id),
            CONSTRAINT opiniones_ibfk_1 FOREIGN KEY (libro_id) REFERENCES libros (libro_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"""
    ]

    for command in sql_commands:
        cursor.execute(command)

    db.commit()

    # Inserciones de autores si no existen
    cursor.execute("""
        INSERT INTO autores (nombre, apellidos, nacionalidad) VALUES
        ('Esopo', 'Esopo', 'Grecia'), ('Daniel', 'Defoe', 'Inglaterra'), ('Jonathan', 'Swift', 'Irlanda'),
        ('Robert Louis', 'Stevenson', 'Escocia'), ('Graciela', 'Montes', 'Argentina'), ('Miriam', 'Reyes', 'Mexico'),
        ('Sofia', 'Rhei', 'España'), ('Educ', 'Maestros', 'Argentina'), ('Jacob y Wilhelm', 'Grimm', 'Alemania'),
        ('James Orchard', 'Halliwell Phillipps', 'Inglaterra'), ('Robert', 'Southey', 'Inglaterra'), 
        ('Cultura', 'Argentina', 'Argentina'), ('Jhon', 'E.thomas', 'EE UU'), 
        ('Monica del rocio', 'Chariguaman leon ', 'Ecuador'), ('Guadalupe', 'Rodriguez', 'Chile'), 
        ('Amado', 'Nervo', 'Mexico'), ('orientacion', 'Andujar', 'España'), ('Sergio', 'Palao', 'España'),
        ('peque', 'Ocio', 'España'), ('Sandra', 'Lopez Abos', 'España'), ('Miguel', 'Santos Arevalo', 'Peru'),
        ('Celeste', 'Marin', 'Argentina'), ('Liber', 'Espacio', 'Argentina'), ('Junta de', 'Andalucia ', 'España'),
        ('Small', 'FOOT', 'Alemania'), ('Niños blog', 'Lifeway', 'Mexico'), ('TRES', 'Museos', 'Venezuela'),
        ('Jhon', 'Doe', 'Narnia'), ('Esopo', 'Esopo', 'Grecia'), ('Oscar', 'Wilde', 'Irlanda'),
        ('Hans Christian', 'Andersen', 'Alemania'), ('Charles Lutwidge', 'Dogson', 'Inglaterra'),
        ('Benjamin', 'Tabart', 'Inglaterra'), ('Anoine', 'De Saint Exupery', 'Francia'), 
        ('Charles', 'Perrault', 'Francia'), ('Giovanni Francesco', 'Straparola', 'Rusia'), 
        ('Frank', 'Baum', 'EEUU'), ('Julio', 'Verne', 'Francia'), ('Edgar Alan', 'Poe', 'EEUU'), 
        ('Charles', 'Dickens', 'Inglaterra'), ('Stephen', 'King', 'EEUU'), ('J.R.R', 'Tolkien', 'Inglaterra'), 
        ('Ray', 'Bradbury', 'EEUU'), ('J K', 'Rowling', 'Inglaterra'), ('Alicia', 'Garcia Herrera', 'España'),
        ('Luis', 'Gonzalez Blasco', 'España'), ('Cecilia', 'Ansalone', 'España'), ('Fernan', 'Caballero', 'Ecuador'),
        ('Alejandro', 'Dumas', 'Francia'), ('Per', 'Abbat', 'Narnia'), ('Diego', 'Hurtado de Mendoza', 'España'),
        ('William', 'Langland', 'Inglaterra'), ('Arturo', 'Perez Reverte', 'España'), 
        ('Edgar', 'Rice Burroughs', 'Inglaterra'), ('Carlo', 'Collodi', 'Italia'), 
        ('Fiodor', 'Dostoyecski', 'Rusia'), ('Jose Maria', 'Arguedas', 'Argentina'), 
        ('Charles', 'Dickens', 'Inglaterra'), ('Jose', 'Saramago', 'Portugal'), 
        ('William', 'Shakespeare', 'Inglaterra'), ('Gabriel', 'Garcia Marquez', 'Colombia'), 
        ('Jean', 'De la Fontaine', 'Francia'), ('Jose', 'Hernandez', 'Argentina'), 
        ('Julio', 'Vernes', 'Francia'), ('Jhon Ajvide', 'Lindqvist', 'Suecia'), ('Mark', 'TWAIN', 'Inglaterra'), 
        ('Jane', 'Austen', 'Suecia'), ('Octavia', 'Butler', 'Africa'), ('James Matthew', 'Barrie', 'Suecia'), 
        ('Philip K', 'Dick', 'Inglaterra'), ('Jose', 'Saramago', 'Suecia'), ('Miyuki', 'Miyabe', 'Suecia'),
        ('Miyabe', 'Miyuki', 'Suecia'), ('Laura', 'Gallego', 'Inglaterra'), ('Lewis', 'Carrol', 'Portugal'), 
        ('Milan', 'Kundera', 'Francia');
    """)

    db.commit()

    cursor.close()
    close_db()

# Función para inicializar la aplicación
def init_app(app):
    # Registrar la función close_db para que se llame automáticamente
    # cuando el contexto de la aplicación se destruye
    app.teardown_appcontext(close_db)

# Si este script se ejecuta directamente, inicializar la base de datos
if __name__ == '__main__':
    init_db()
