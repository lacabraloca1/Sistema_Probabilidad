from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from sqlalchemy import text
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
    creditos = int(data.get('creditos', 100))
    creditos = min(max(creditos, 1), 100) 
    nueva_materia = Materias(nombre=data.get('nombre'), creditos=creditos)
    db.session.add(nueva_materia)
    db.session.commit()
    return redirect(url_for('materias_bp.vista_materias'))

@materias_bp.route('/materias/editar/<int:materia_id>', methods=['POST'])
def editar_materia(materia_id):
    materia = Materias.query.get(materia_id)
    if not materia:
        return jsonify({"error": "Materia no encontrada"}), 404

    materia.nombre = request.form.get('nombre')
    materia.creditos = request.form.get('creditos')

    db.session.commit()
    return redirect(url_for('materias_bp.vista_materias'))


@materias_bp.route('/materias/eliminar/<int:materia_id>', methods=['POST'])
def eliminar_materia(materia_id):
    materia = Materias.query.get(materia_id)
    if not materia:
        return jsonify({"error": "Materia no encontrada"}), 404

    db.session.delete(materia)
    db.session.commit()

    # 🔹 Reset AUTO_INCREMENT para mantener el ID ordenado
    db.session.execute(text("ALTER TABLE Materias AUTO_INCREMENT = 1"))
    db.session.commit()

    return jsonify({"mensaje": "Materia eliminada exitosamente"}), 200
