from datetime import datetime
from database import get_db, Rol


class Usuario:
    def __init__(self, id_usuario=None, nombre=None, apellido=None, username=None, email=None, fecha_nacimiento=None,
                 fecha_registro=None, genero=None, pais=None, password=None, rol_id=None):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.username = username
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_registro = fecha_registro or datetime.utcnow()
        self.genero = genero
        self.pais = pais
        self.password = password
        self.rol_id = rol_id

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_usuario:
            cursor.execute("""
                UPDATE usuarios SET nombre = %s, apellido = %s, username = %s, email = %s, fecha_nacimiento = %s, 
                fecha_registro = %s, genero = %s, pais = %s, password = %s, rol_id = %s WHERE id_usuario = %s
            """, (self.nombre, self.apellido, self.username, self.email, self.fecha_nacimiento, self.fecha_registro,
                  self.genero, self.pais, self.password, self.rol_id, self.id_usuario))
        else:
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellido, username, email, fecha_nacimiento, fecha_registro, genero, pais, password, rol_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (self.nombre, self.apellido, self.username, self.email, self.fecha_nacimiento, self.fecha_registro,
                  self.genero, self.pais, self.password, self.rol_id))
            self.id_usuario = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios")
        rows = cursor.fetchall()
        cursor.close()
        return [Usuario(*row) for row in rows]

    @staticmethod
    def get_by_id(id_usuario):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        row = cursor.fetchone()
        cursor.close()
        return Usuario(*row) if row else None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (self.id_usuario,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'username': self.username,
            'email': self.email,
            'fecha_nacimiento': self.fecha_nacimiento,
            'fecha_registro': self.fecha_registro,
            'genero': self.genero,
            'pais': self.pais,
            'rol_id': self.rol_id,
            'rol': self.get_rol().serialize() if self.get_rol() else None
        }

    def get_rol(self):
        return Rol.get_by_id(self.rol_id)

    def __repr__(self):
        return f'<Usuario {self.username}>'
