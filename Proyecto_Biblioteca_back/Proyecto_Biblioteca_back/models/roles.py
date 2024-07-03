from database import get_db

class Rol:
    def __init__(self, id=None, nombre=None, descripcion=None):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id:
            cursor.execute("""
                UPDATE roles SET nombre = %s, descripcion = %s WHERE id = %s
            """, (self.nombre, self.descripcion, self.id))
        else:
            cursor.execute("""
                INSERT INTO roles (nombre, descripcion) VALUES (%s, %s)
            """, (self.nombre, self.descripcion))
            self.id = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM roles")
        rows = cursor.fetchall()
        cursor.close()
        return [Rol(*row) for row in rows]

    @staticmethod
    def get_by_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM roles WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        return Rol(*row) if row else None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM roles WHERE id = %s", (self.id,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion
        }

    def __repr__(self):
        return f'<Rol {self.nombre}>'
