from utils.extensions import db
from sqlalchemy import Enum

class InscripcionAlumnos(db.Model):
    __tablename__ = 'Inscripcion_Alumnos'

    inscripcion_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Alumnos.usuario_id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('Materias.materia_id'), nullable=False)
    cuatrimestre_id = db.Column(db.Integer, db.ForeignKey('Cuatrimestre.cuatrimestre_id'), nullable=False)
    estatus = db.Column(Enum('cursando', 'aprobado', 'reprobado', 'retirado', name="estatus_materia"), nullable=False, default='cursando')

    def __repr__(self):
        return f'<Inscripción {self.inscripcion_id} - {self.estatus}>'
