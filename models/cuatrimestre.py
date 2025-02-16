from utils.extensions import db

class Cuatrimestre(db.Model):
    __tablename__ = 'Cuatrimestre'

    cuatrimestre_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Cuatrimestre {self.nombre}>'
