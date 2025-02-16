from utils.extensions import db

class Alumnos(db.Model):
    __tablename__ = 'Alumnos'

    usuario_id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido_paterno = db.Column(db.String(100), nullable=False)
    apellido_materno = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email_correo = db.Column(db.String(150), unique=True, nullable=False)

    def __repr__(self):
        return f'<Alumno {self.matricula} - {self.nombre}>'


from models.inscripcion_alumnos import InscripcionAlumnos
Alumnos.inscripciones = db.relationship('InscripcionAlumnos', backref='alumno', lazy=True)
