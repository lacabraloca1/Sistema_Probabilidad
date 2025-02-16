from utils.extensions import db

class Calificaciones(db.Model):
    __tablename__ = 'Calificaciones'

    calificaciones_id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Alumnos.usuario_id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('Materias.materia_id'), nullable=False)
    cuatrimestre_id = db.Column(db.Integer, db.ForeignKey('Cuatrimestre.cuatrimestre_id'), nullable=False)

    primer_parcial = db.Column(db.Numeric(5,2), nullable=True)
    segundo_parcial = db.Column(db.Numeric(5,2), nullable=True)
    tercer_parcial = db.Column(db.Numeric(5,2), nullable=True)
    calificacion_final = db.Column(db.Numeric(5,2), nullable=True)

    def calcular_calificacion_final(self):
        if self.primer_parcial is not None and self.segundo_parcial is not None and self.tercer_parcial is not None:
            self.calificacion_final = (self.primer_parcial + self.segundo_parcial + self.tercer_parcial) / 3

    def __repr__(self):
        return f'<Calificación {self.calificaciones_id} - Alumno {self.usuario_id}>'
