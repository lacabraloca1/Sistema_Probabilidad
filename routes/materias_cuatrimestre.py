from flask import Blueprint, request, jsonify
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
