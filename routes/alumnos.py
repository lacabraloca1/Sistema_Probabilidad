from flask import Blueprint,flash, request, render_template, redirect, url_for, jsonify
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

    # Verificación y asignación de valores predeterminados si son None
    matricula = data.get('matricula', '').strip()
    nombre = data.get('nombre', '').strip()
    apellido_paterno = data.get('apellido_paterno', '').strip()
    apellido_materno = data.get('apellido_materno', '').strip()
    fecha_nacimiento = data.get('fecha_nacimiento', None)
    email_correo = data.get('email_correo', '').strip()

    # Validar que los campos obligatorios no estén vacíos
    if not matricula or not nombre or not apellido_paterno or not email_correo:
        flash("Todos los campos obligatorios deben estar llenos.", "error")
        return redirect(url_for('alumnos_bp.vista_alumnos'))

    # Crear nuevo alumno asegurando que los valores sean válidos
    nuevo_alumno = Alumnos(
        matricula=matricula,
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno or "N/A",  # Si es vacío, asigna "N/A"
        fecha_nacimiento=fecha_nacimiento or None,  # Mantiene None si no se proporciona
        email_correo=email_correo
    )

    try:
        db.session.add(nuevo_alumno)
        db.session.commit()
        flash("Alumno agregado correctamente", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al agregar el alumno: {str(e)}", "error")

    return redirect(url_for('alumnos_bp.vista_alumnos'))

@alumnos_bp.route('/editar/<int:id>', methods=['POST'])
def editar_alumno(id):
    alumno = Alumnos.query.get(id)
    if not alumno:
        return jsonify({"error": "Alumno no encontrado"}), 404

    alumno.matricula = request.form.get('matricula')
    alumno.nombre = request.form.get('nombre')
    alumno.apellido_paterno = request.form.get('apellido_paterno')
    alumno.apellido_materno = request.form.get('apellido_materno')
    alumno.email_correo = request.form.get('email_correo')

    db.session.commit()
    flash("Alumno editado correctamente", "success")
    return redirect(url_for('alumnos_bp.vista_alumnos'))

@alumnos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_alumno(id):
    alumno = Alumnos.query.get(id)
    if not alumno:
        flash("Alumno no encontrado", "error")
        return redirect(url_for('alumnos_bp.vista_alumnos'))

    db.session.delete(alumno)
    db.session.commit()

    # Restablecer el AUTO_INCREMENT solo si no hay más registros
    ultimo = db.session.query(Alumnos).order_by(Alumnos.usuario_id.desc()).first()
    if not ultimo:
        db.session.execute("ALTER TABLE Alumnos AUTO_INCREMENT = 1")
        db.session.commit()

    flash("Alumno eliminado correctamente", "success")
    return redirect(url_for('alumnos_bp.vista_alumnos'))
