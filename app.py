from flask import Flask, render_template
from utils.extensions import db
from routes.alumnos import alumnos_bp
from routes.grupos import grupos_bp
from routes.cuatrimestres import cuatrimestres_bp
from routes.materias import materias_bp
from routes.calificaciones import calificaciones_bp
from routes.inscripcion import inscripcion_bp
from routes.materias_cuatrimestre import materias_cuatri_bp
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234567890@localhost/sistema_escolar_db'#root:contraseña
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Registrar los Blueprints
app.register_blueprint(alumnos_bp, url_prefix='/alumnos')
app.register_blueprint(grupos_bp, url_prefix='/grupos')
app.register_blueprint(cuatrimestres_bp, url_prefix='/cuatrimestres')
app.register_blueprint(materias_bp, url_prefix='/materias')
app.register_blueprint(calificaciones_bp, url_prefix='/calificaciones')
app.register_blueprint(inscripcion_bp, url_prefix='/inscripcion')
app.register_blueprint(materias_cuatri_bp, url_prefix='/materias-cuatrimestre')

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
