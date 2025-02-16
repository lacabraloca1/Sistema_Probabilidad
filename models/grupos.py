from utils.extensions import db

class Grupos(db.Model):
    __tablename__ = 'Grupos'

    grupos_id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    turno = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return f'<Grupo {self.nombre} - Turno {self.turno}>'
