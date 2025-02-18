from flask import Blueprint, flash, redirect, request, jsonify, url_for
from utils.extensions import db
from models.materias_cuatrimestre import MateriasCuatrimestre

materias_cuatri_bp = Blueprint('materias_cuatri_bp', __name__)

# ✅ Asignar una materia a un cuatrimestre
@materias_cuatri_bp.route('/materias-cuatrimestre', methods=['POST'])
def asignar_materia():
    data = request.json
    nueva_asignacion = MateriasCuatrimestre(materia_id=data.get('materia_id'), cuatrimestre_id=data.get('cuatrimestre_id'))
    db.session.add(nueva_asignacion)
    db.session.commit()
    return jsonify({"mensaje": "Materia asignada a cuatrimestre exitosamente"}), 201

@materias_cuatri_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_materia_cuatrimestre(id):
    materia_cuatrimestre = MateriasCuatrimestre.query.get(id)
    if not materia_cuatrimestre:
        return jsonify({"error": "Relación Materia-Cuatrimestre no encontrada"}), 404

    db.session.delete(materia_cuatrimestre)
    db.session.commit()

    # Restablecer el AUTO_INCREMENT después de eliminar
    db.session.execute("ALTER TABLE Materias_Cuatrimestre AUTO_INCREMENT = 1")
    db.session.commit()

    flash("Relación Materia-Cuatrimestre eliminada correctamente", "success")
    return redirect(url_for('materias_cuatrimestre_bp.vista_materias_cuatrimestre'))
