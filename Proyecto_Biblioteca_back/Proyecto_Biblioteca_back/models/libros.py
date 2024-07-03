from database import get_db, Autor, GeneroLiterario, Opinion

class Libro:
    def __init__(self, libro_id=None, titulo=None, autor_id=None, genero_id=None, anio_publicacion=None, imagen=None, resenia=None, pdf=None):
        self.libro_id = libro_id
        self.titulo = titulo
        self.autor_id = autor_id
        self.genero_id = genero_id
        self.anio_publicacion = anio_publicacion
        self.imagen = imagen
        self.resenia = resenia
        self.pdf = pdf

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.libro_id:
            cursor.execute("""
                UPDATE libros SET titulo = %s, autor_id = %s, genero_id = %s, anio_publicacion = %s, imagen = %s, resenia = %s, pdf = %s WHERE libro_id = %s
            """, (self.titulo, self.autor_id, self.genero_id, self.anio_publicacion, self.imagen, self.resenia, self.pdf, self.libro_id))
        else:
            cursor.execute("""
                INSERT INTO libros (titulo, autor_id, genero_id, anio_publicacion, imagen, resenia, pdf) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (self.titulo, self.autor_id, self.genero_id, self.anio_publicacion, self.imagen, self.resenia, self.pdf))
            self.libro_id = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM libros")
        rows = cursor.fetchall()
        cursor.close()
        return [Libro(*row) for row in rows]

    @staticmethod
    def get_by_id(libro_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM libros WHERE libro_id = %s", (libro_id,))
        row = cursor.fetchone()
        cursor.close()
        return Libro(*row) if row else None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM libros WHERE libro_id = %s", (self.libro_id,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'libro_id': self.libro_id,
            'titulo': self.titulo,
            'autor_id': self.autor_id,
            'genero_id': self.genero_id,
            'anio_publicacion': self.anio_publicacion,
            'imagen': self.imagen,
            'resenia': self.resenia,
            'pdf': self.pdf,
            'autor': self.get_autor().serialize() if self.get_autor() else None,
            'genero': self.get_genero().serialize() if self.get_genero() else None,
            'opiniones': [opinion.serialize() for opinion in self.get_opiniones()]
        }

    def get_autor(self):
        return Autor.get_by_id(self.autor_id)

    def get_genero(self):
        return GeneroLiterario.get_by_id(self.genero_id)

    def get_opiniones(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM opiniones WHERE libro_id = %s", (self.libro_id,))
        rows = cursor.fetchall()
        cursor.close()
        return [Opinion(*row) for row in rows]

    def __repr__(self):
        return f'<Libro {self.titulo}>'
