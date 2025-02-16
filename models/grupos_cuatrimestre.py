from utils.extensions import db

class GruposCuatrimestre(db.Model):
    __tablename__ = 'Grupos_Cuatrimestre'

    grupo_cuatri_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    grupos_id = db.Column(db.Integer, db.ForeignKey('Grupos.grupos_id'))
    cuatrimestre_id = db.Column(db.Integer, db.ForeignKey('Cuatrimestre.cuatrimestre_id'))

    grupo = db.relationship('Grupos', backref='cuatrimestres')
    cuatrimestre = db.relationship('Cuatrimestre', backref='grupos')

    def __repr__(self):
        return f'<Grupo {self.nombre} - Cuatrimestre {self.cuatrimestre_id}>'
