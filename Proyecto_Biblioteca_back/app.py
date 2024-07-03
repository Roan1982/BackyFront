import os
from datetime import datetime
from flask import Flask, jsonify, request, g, make_response
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import mysql.connector
from mysql.connector import Error

# Importar funciones y configuración de la base de datos desde database.py
from database import get_db, close_db, init_app

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Agrega una clave secreta para las sesiones
bcrypt = Bcrypt(app)



# Configuración CORS
CORS(app)

# Inicializar la aplicación con el contexto de base de datos
init_app(app)

# Configurar carpeta de carga
app.config['UPLOAD_FOLDER'] = 'static'
app.config['IMAGE_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'img')
app.config['PDF_FOLDER'] = os.path.join(app.config['UPLOAD_FOLDER'], 'Libros')

# Crear carpetas si no existen
os.makedirs(app.config['IMAGE_FOLDER'], exist_ok=True)
os.makedirs(app.config['PDF_FOLDER'], exist_ok=True)

@app.route('/libros', methods=['GET'])
def listar_libros():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT l.libro_id, l.titulo, l.autor_id, l.genero_id, l.anio_publicacion, l.imagen, l.resenia, l.pdf, a.nombre as autor_nombre
            FROM libros l
            LEFT JOIN autores a ON l.autor_id = a.autor_id
        """)
        libros = cursor.fetchall()
        cursor.close()
        return jsonify(libros)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Agregar libro
@app.route('/libros', methods=['POST'])
def agregar_libro():
    db = get_db()
    cursor = db.cursor()

    # Obtener los datos del libro desde la solicitud
    data = request.form
    titulo = data.get('titulo')
    autor_id = data.get('autor_id')
    genero_id = data.get('genero_id')
    anio_publicacion = data.get('anio_publicacion')
    resenia = data.get('resenia')

    # Manejar la carga de imagen y PDF
    imagen_file = request.files.get('imagen')
    pdf_file = request.files.get('pdf')

    if imagen_file and pdf_file:
        # Asegurar nombres de archivo seguros
        imagen_filename = secure_filename(imagen_file.filename)
        pdf_filename = secure_filename(pdf_file.filename)

        # Guardar los archivos en la carpeta estática (o cualquier otra ruta que prefieras)
        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], 'img', imagen_filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'Libros', pdf_filename)
        imagen_file.save(imagen_path)
        pdf_file.save(pdf_path)

        # Guardar las rutas en la base de datos
        sql = """
            INSERT INTO libros (titulo, autor_id, genero_id, anio_publicacion, imagen, resenia, pdf)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        val = (titulo, autor_id, genero_id, anio_publicacion, imagen_filename, resenia, pdf_filename)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()

        return jsonify({'message': 'Libro agregado exitosamente'}), 201

    return jsonify({'error': 'Se requiere una imagen y un archivo PDF'}), 400

# Configurar carpeta de carga
app.config['UPLOAD_FOLDER'] = 'static'

# Editar libro
@app.route('/libros/<int:libro_id>', methods=['PUT'])
def editar_libro(libro_id):
    db = get_db()
    cursor = db.cursor()
    data = request.json
    sql = "UPDATE libros SET titulo=%s, autor_id=%s, genero_id=%s, anio_publicacion=%s, imagen=%s, resenia=%s, pdf=%s WHERE libro_id=%s"
    val = (data['titulo'], data['autor_id'], data['genero_id'], data['anio_publicacion'], data['imagen'], data['resenia'], data['pdf'], libro_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Libro actualizado exitosamente'})

# Eliminar libro
@app.route('/libros/<int:libro_id>', methods=['DELETE'])
def eliminar_libro(libro_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM libros WHERE libro_id=%s", (libro_id,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Libro eliminado exitosamente'})

# Ruta para listar usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        # Establece una conexión y un cursor dentro de un contexto
        with get_db() as db:
            cursor = db.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.id_usuario, u.nombre, u.apellido, u.username, u.email, u.fecha_nacimiento,
                       u.fecha_registro, u.genero, u.pais, r.nombre AS rol
                FROM usuarios u
                LEFT JOIN roles r ON u.rol_id = r.id
            """)
            usuarios = cursor.fetchall()
            cursor.close()

        # Convierte el resultado a JSON y lo devuelve como respuesta
        return jsonify(usuarios)
    
    except mysql.connector.Error as err:
        # Manejo de errores específicos de mysql.connector
        return jsonify({"error": f"Error de base de datos: {err}"}), 500
    
    except Exception as e:
        # Manejo de errores genéricos
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500

# Ruta para agregar un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.json
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    username = data.get('username')
    email = data.get('email')
    fecha_nacimiento = data.get('fecha_nacimiento')
    genero = data.get('genero')
    pais = data.get('pais')
    
    # Encriptar la contraseña con bcrypt
    password = data.get('password')
    hashed_password = generate_password_hash(password).decode('utf-8')

    rol_id = data.get('rol_id')

    try:
        db = get_db()
        cursor = db.cursor()

        # Insertar el nuevo usuario en la base de datos
        cursor.execute("""
            INSERT INTO usuarios (nombre, apellido, username, email, fecha_nacimiento, genero, pais, password, rol_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, username, email, fecha_nacimiento, genero, pais, hashed_password, rol_id))

        db.commit()
        cursor.close()

        return jsonify({'message': 'Usuario agregado exitosamente'}), 200

    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al agregar el usuario'}), 500

@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def editar_usuario(id_usuario):
    try:
        db = get_db()
        cursor = db.cursor()
        data = request.json
        
        # Aquí puedes imprimir los datos recibidos para verificar
        print(data)
        
        # Actualización del usuario en la base de datos
        sql = "UPDATE usuarios SET nombre=%s, apellido=%s, username=%s, email=%s, fecha_nacimiento=%s, genero=%s, pais=%s, rol_id=%s WHERE id_usuario=%s"
        val = (data['nombre'], data['apellido'], data['username'], data['email'], data['fecha_nacimiento'], data['genero'], data['pais'], data['rol_id'], id_usuario)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        
        return jsonify({'message': 'Usuario actualizado exitosamente'})
    
    except Exception as e:
        print(str(e))  # Imprime el error para depuración
        return jsonify({'error': 'Error al actualizar usuario'}), 500

@app.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()
        cursor.close()

        if not usuario:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'id_usuario': usuario[0],
            'nombre': usuario[1],
            'apellido': usuario[2],
            'username': usuario[3],
            'email': usuario[4],
            'fecha_nacimiento': usuario[5],
            'genero': usuario[6],
            'pais': usuario[7]
        }), 200
    
    except Exception as e:
        print(e)
        return jsonify({'error': 'Error al obtener el usuario'}), 500


# Eliminar usuario
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Usuario eliminado exitosamente'})

# Listar autores
@app.route('/autores', methods=['GET'])
def listar_autores():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM autores")
    autores = cursor.fetchall()
    cursor.close()
    return jsonify(autores)

# Agregar autor
@app.route('/autores', methods=['POST'])
def agregar_autor():
    db = get_db()
    cursor = db.cursor()
    data = request.json
    sql = "INSERT INTO autores (nombre, apellidos, nacionalidad) VALUES (%s, %s, %s)"
    val = (data['nombre'], data['apellidos'], data['nacionalidad'])
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Autor agregado exitosamente'}), 201

# Editar autor
@app.route('/autores/<int:autor_id>', methods=['PUT'])
def editar_autor(autor_id):
    db = get_db()
    cursor = db.cursor()
    data = request.json
    sql = "UPDATE autores SET nombre=%s, apellidos=%s WHERE autor_id=%s"
    val = (data['nombre'], data['apellidos'], autor_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Autor actualizado exitosamente'})

# Eliminar autor
@app.route('/autores/<int:autor_id>', methods=['DELETE'])
def eliminar_autor(autor_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM autores WHERE autor_id=%s", (autor_id,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Autor eliminado exitosamente'})

# Listar géneros
@app.route('/generos', methods=['GET'])
def listar_generos():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM generos_literarios")
    generos = cursor.fetchall()
    cursor.close()
    return jsonify(generos)

# Agregar género
@app.route('/generos', methods=['POST'])
def agregar_genero():
    db = get_db()
    cursor = db.cursor()
    data = request.json
    sql = "INSERT INTO generos_literarios (nombre) VALUES (%s)"
    val = (data['nombre'],)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Género agregado exitosamente'}), 201

# Editar género
@app.route('/generos/<int:genero_id>', methods=['PUT'])
def editar_genero(genero_id):
    db = get_db()
    cursor = db.cursor()
    data = request.json
    sql = "UPDATE generos_literarios SET nombre=%s WHERE genero_id=%s"
    val = (data['nombre'], genero_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Género actualizado exitosamente'})

# Eliminar género
@app.route('/generos/<int:genero_id>', methods=['DELETE'])
def eliminar_genero(genero_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM generos_literarios WHERE genero_id=%s", (genero_id,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Género eliminado exitosamente'})

# Listar opiniones
@app.route('/opiniones', methods=['GET'])
def listar_opiniones():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM opiniones")
    opiniones = cursor.fetchall()
    cursor.close()
    return jsonify(opiniones)

# Agregar opinión
@app.route('/opiniones', methods=['POST'])
def agregar_opinion():
    db = get_db()
    cursor = db.cursor()
    data = request.json
    sql = "INSERT INTO opiniones (libro_id, opinion_texto, puntaje, fecha_opinion) VALUES (%s, %s, %s, %s)"
    val = (data['libro_id'], data['opinion_texto'], data['puntaje'], datetime.now())
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Opinión agregada exitosamente'}), 201

# Editar opinión
@app.route('/opiniones/<int:opinion_id>', methods=['PUT'])
def editar_opinion(opinion_id):
    db = get_db()
    cursor = db.cursor()
    data = request.json
    sql = "UPDATE opiniones SET libro_id=%s, opinion_texto=%s, puntaje=%s, fecha_opinion=%s WHERE opinion_id=%s"
    val = (data['libro_id'], data['opinion_texto'], data['puntaje'], data['fecha_opinion'], opinion_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()
    return jsonify({'message': 'Opinión actualizada exitosamente'})

# Eliminar opinión
@app.route('/opiniones/<int:opinion_id>', methods=['DELETE'])
def eliminar_opinion(opinion_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM opiniones WHERE opinion_id=%s", (opinion_id,))
    db.commit()
    cursor.close()
    return jsonify({'message': 'Opinión eliminada exitosamente'})

# Manejo de errores
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

# Ruta para listar todos los roles
@app.route('/roles', methods=['GET'])
def listar_roles():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM roles")
        roles = cursor.fetchall()
        cursor.close()

        roles_list = []
        for rol in roles:
            rol_data = {
                'id': rol[0],
                'nombre': rol[1],
                'descripcion': rol[2]
            }
            roles_list.append(rol_data)

        return jsonify(roles_list)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para agregar un nuevo rol
@app.route('/roles', methods=['POST'])
def agregar_rol():
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')

        if not nombre or not descripcion:
            return jsonify({'error': 'Se requiere nombre y descripción para agregar un rol'}), 400

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO roles (nombre, descripcion) VALUES (%s, %s)", (nombre, descripcion))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Rol agregado correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar un rol existente por su ID
@app.route('/roles/<int:id>', methods=['PUT'])
def actualizar_rol(id):
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')

        if not nombre or not descripcion:
            return jsonify({'error': 'Se requiere nombre y descripción para actualizar un rol'}), 400

        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE roles SET nombre = %s, descripcion = %s WHERE id = %s", (nombre, descripcion, id))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Rol actualizado correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para eliminar un rol existente por su ID
@app.route('/roles/<int:id>', methods=['DELETE'])
def eliminar_rol(id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM roles WHERE id = %s", (id,))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Rol eliminado correctamente'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

app.run(host='0.0.0.0', port=5000)