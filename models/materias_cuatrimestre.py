from utils.extensions import db

class MateriasCuatrimestre(db.Model):
    __tablename__ = 'Materias_Cuatrimestre'

    materia_id = db.Column(db.Integer, db.ForeignKey('Materias.materia_id'), primary_key=True)
    cuatrimestre_id = db.Column(db.Integer, db.ForeignKey('Cuatrimestre.cuatrimestre_id'), primary_key=True)

    materia = db.relationship('Materias', backref=db.backref('cuatrimestres', lazy=True))
    cuatrimestre = db.relationship('Cuatrimestre', backref=db.backref('materias', lazy=True))

    def __repr__(self):
        return f'<Materia {self.materia_id} en Cuatrimestre {self.cuatrimestre_id}>'