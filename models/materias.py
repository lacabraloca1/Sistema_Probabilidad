from utils.extensions import db

class Materias(db.Model):
    __tablename__ = 'Materias'

    materia_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    creditos = db.Column(db.Integer, nullable=False)

    # Evita conflicto con la relación de calificaciones
    calificaciones = db.relationship('Calificaciones', back_populates='materia', overlaps="calificaciones")

    # Evita conflicto con MateriasCuatrimestre
    cuatrimestres = db.relationship('MateriasCuatrimestre', back_populates='materia', overlaps="cuatrimestres")

    def __repr__(self):
        return f'<Materia {self.nombre}>'
