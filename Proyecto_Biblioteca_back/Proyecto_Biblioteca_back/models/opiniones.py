from database import get_db, Libro


class Opinion:
    def __init__(self, opinion_id=None, libro_id=None, opinion_texto=None, puntaje=None, fecha_opinion=None):
        self.opinion_id = opinion_id
        self.libro_id = libro_id
        self.opinion_texto = opinion_texto
        self.puntaje = puntaje
        self.fecha_opinion = fecha_opinion

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.opinion_id:
            cursor.execute("""
                UPDATE opiniones SET libro_id = %s, opinion_texto = %s, puntaje = %s, fecha_opinion = %s WHERE opinion_id = %s
            """, (self.libro_id, self.opinion_texto, self.puntaje, self.fecha_opinion, self.opinion_id))
        else:
            cursor.execute("""
                INSERT INTO opiniones (libro_id, opinion_texto, puntaje, fecha_opinion) VALUES (%s, %s, %s, %s)
            """, (self.libro_id, self.opinion_texto, self.puntaje, self.fecha_opinion))
            self.opinion_id = cursor.lastrowid
        db.commit()
        cursor.close()

    @staticmethod
    def get_all():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM opiniones")
        rows = cursor.fetchall()
        cursor.close()
        return [Opinion(*row) for row in rows]

    @staticmethod
    def get_by_id(opinion_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM opiniones WHERE opinion_id = %s", (opinion_id,))
        row = cursor.fetchone()
        cursor.close()
        return Opinion(*row) if row else None

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM opiniones WHERE opinion_id = %s", (self.opinion_id,))
        db.commit()
        cursor.close()

    def serialize(self):
        return {
            'opinion_id': self.opinion_id,
            'libro_id': self.libro_id,
            'opinion_texto': self.opinion_texto,
            'puntaje': self.puntaje,
            'fecha_opinion': self.fecha_opinion,
            'libro': self.get_libro().serialize() if self.get_libro() else None
        }

    def get_libro(self):
        return Libro.get_by_id(self.libro_id)

    def __repr__(self):
        return f'<Opinion {self.opinion_id}>'
