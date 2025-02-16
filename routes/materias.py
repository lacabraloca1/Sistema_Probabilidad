from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from utils.extensions import db
from models.materias import Materias

materias_bp = Blueprint('materias_bp', __name__)

@materias_bp.route('/')
def vista_materias():
    materias = Materias.query.all()
    return render_template('admin_materias.html', materias=materias)

@materias_bp.route('/crear', methods=['POST'])
def crear_materia():
    data = request.form
    nueva_materia = Materias(nombre=data.get('nombre'), creditos=data.get('creditos'))
    db.session.add(nueva_materia)
    db.session.commit()
    return redirect(url_for('materias_bp.vista_materias'))

@materias_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_materia(id):
    materia = Materias.query.get(id)
    if not materia:
        return jsonify({"error": "Materia no encontrada"}), 404
    db.session.delete(materia)
    db.session.commit()
    return redirect(url_for('materias_bp.vista_materias'))
