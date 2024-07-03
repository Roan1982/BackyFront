from database import get_db

class GeneroLiterario:
    def __init__(self, genero_id=None, nombre_genero=None):
        self.genero_id = genero_id
        self.nombre_genero = nombre_genero

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.genero_id:
            cursor.execute("""
                UPDATE generos_literarios SET nombre_genero = %s WHERE genero_id = %s
            """, (self.nombre_genero, self.genero_id))
        else:
            cursor.execute("""
                INSERT INTO generos_literarios (nombre_genero) VALUES (%s)
            """, (self.nombre_genero,))
            self.genero_id = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM generos_literarios")
        rows = cursor.fetchall()
        cursor.close()
        return [GeneroLiterario(*row) for row in rows]

    @staticmethod
    def get_by_id(genero_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM generos_literarios WHERE genero_id = %s", (genero_id,))
        row = cursor.fetchone()
        cursor.close()
        return GeneroLiterario(*row) if row else None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM generos_literarios WHERE genero_id = %s", (self.genero_id,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'genero_id': self.genero_id,
            'nombre_genero': self.nombre_genero
        }

    def __repr__(self):
        return f'<GeneroLiterario {self.nombre_genero}>'
