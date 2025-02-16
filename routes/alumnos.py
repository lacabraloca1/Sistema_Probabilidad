from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from utils.extensions import db
from models.alumnos import Alumnos

alumnos_bp = Blueprint('alumnos_bp', __name__)

@alumnos_bp.route('/')
def vista_alumnos():
    alumnos = Alumnos.query.all()
    return render_template('admin_alumnos.html', alumnos=alumnos)

@alumnos_bp.route('/crear', methods=['POST'])
def crear_alumno():
    data = request.form
    nuevo_alumno = Alumnos(
        matricula=data.get('matricula'),
        nombre=data.get('nombre'),
        apellido_paterno=data.get('apellido_paterno'),
        apellido_materno=data.get('apellido_materno'),
        fecha_nacimiento=data.get('fecha_nacimiento'),
        email_correo=data.get('email_correo')
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return redirect(url_for('alumnos_bp.vista_alumnos'))

@alumnos_bp.route('/editar/<int:id>', methods=['POST'])
def editar_alumno(id):
    alumno = Alumnos.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    alumno.nombre = request.form.get('nombre')
    alumno.email_correo = request.form.get('email_correo')
    db.session.commit()
    return redirect(url_for('alumnos_bp.vista_alumnos'))

@alumnos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_alumno(id):
    alumno = Alumnos.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404
    db.session.delete(alumno)
    db.session.commit()
    return redirect(url_for('alumnos_bp.vista_alumnos'))
