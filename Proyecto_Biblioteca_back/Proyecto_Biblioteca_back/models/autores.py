from database import get_db

class Autor:
    def __init__(self, autor_id=None, nombre=None, apellidos=None, nacionalidad=None):
        self.autor_id = autor_id
        self.nombre = nombre
        self.apellidos = apellidos
        self.nacionalidad = nacionalidad

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.autor_id:
            cursor.execute("""
                UPDATE autores SET nombre = %s, apellidos = %s, nacionalidad = %s WHERE autor_id = %s
            """, (self.nombre, self.apellidos, self.nacionalidad, self.autor_id))
        else:
            cursor.execute("""
                INSERT INTO autores (nombre, apellidos, nacionalidad) VALUES (%s, %s, %s)
            """, (self.nombre, self.apellidos, self.nacionalidad))
            self.autor_id = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM autores")
        rows = cursor.fetchall()
        cursor.close()
        return [Autor(*row) for row in rows]

    @staticmethod
    def get_by_id(autor_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM autores WHERE autor_id = %s", (autor_id,))
        row = cursor.fetchone()
        cursor.close()
        return Autor(*row) if row else None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM autores WHERE autor_id = %s", (self.autor_id,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'autor_id': self.autor_id,
            'nombre': self.nombre,
            'apellidos': self.apellidos,
            'nacionalidad': self.nacionalidad
        }

    def __repr__(self):
        return f'<Autor {self.nombre} {self.apellidos}>'
