from utils.extensions import db

class Materias(db.Model):
    __tablename__ = 'Materias'

    materia_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    creditos = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Materia {self.nombre}>'
