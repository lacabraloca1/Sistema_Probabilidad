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
    calificacion_final = db.Column(db.Numeric(5,2), nullable=True)  # AHORA ES UNA COLUMNA NORMAL

    # Relación con Alumnos
    alumno = db.relationship('Alumnos', backref='calificaciones')

    # Relación con Materias
    materia = db.relationship('Materias', back_populates='calificaciones', overlaps="calificaciones")

    # Relación con Cuatrimestre
    cuatrimestre = db.relationship('Cuatrimestre', backref='calificaciones')

    def calcular_calificacion_final(self):
        """ Calcula la calificación final solo si los tres parciales tienen valor """
        if self.primer_parcial is not None and self.segundo_parcial is not None and self.tercer_parcial is not None:
            try:
                self.calificacion_final = round(
                    (float(self.primer_parcial) + float(self.segundo_parcial) + float(self.tercer_parcial)) / 3, 2
                )
            except (ValueError, TypeError):
                self.calificacion_final = None

    def __repr__(self):
        return f'<Calificación {self.calificaciones_id} - Alumno {self.usuario_id}>'
