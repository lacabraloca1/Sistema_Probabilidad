from utils.extensions import db

class MateriasCuatrimestre(db.Model):
    __tablename__ = 'Materias_Cuatrimestre'

    materia_id = db.Column(db.Integer, db.ForeignKey('Materias.materia_id'), primary_key=True)
    cuatrimestre_id = db.Column(db.Integer, db.ForeignKey('Cuatrimestre.cuatrimestre_id'), primary_key=True)

    # Evita conflictos de backref con `Materias`
    materia = db.relationship('Materias', back_populates='cuatrimestres', overlaps="cuatrimestres")   
    cuatrimestre = db.relationship('Cuatrimestre', backref='materias', lazy=True)

    def __repr__(self):
        return f'<Materia {self.materia_id} en Cuatrimestre {self.cuatrimestre_id}>'
