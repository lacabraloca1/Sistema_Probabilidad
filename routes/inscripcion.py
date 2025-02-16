from flask import Blueprint, request, jsonify
from utils.extensions import db
from models.inscripcion_alumnos import InscripcionAlumnos

inscripcion_bp = Blueprint('inscripcion_bp', __name__)

# ✅ Inscribir un alumno a una materia
@inscripcion_bp.route('/inscripcion', methods=['POST'])
def inscribir_alumno():
    data = request.json
    nueva_inscripcion = InscripcionAlumnos(
        usuario_id=data.get('usuario_id'),
        materia_id=data.get('materia_id'),
        cuatrimestre_id=data.get('cuatrimestre_id'),
        estatus='cursando'  # Por defecto el alumno inicia como "cursando"
    )
    db.session.add(nueva_inscripcion)
    db.session.commit()
    return jsonify({"mensaje": "Alumno inscrito exitosamente"}), 201

# ✅ Obtener todas las inscripciones
@inscripcion_bp.route('/inscripcion', methods=['GET'])
def obtener_inscripciones():
    inscripciones = InscripcionAlumnos.query.all()
    inscripciones_json = [
        {
            "inscripcion_id": insc.inscripcion_id,
            "usuario_id": insc.usuario_id,
            "materia_id": insc.materia_id,
            "cuatrimestre_id": insc.cuatrimestre_id,
            "estatus": insc.estatus
        } for insc in inscripciones
    ]
    return jsonify(inscripciones_json)

# ✅ Cambiar estatus de una inscripción
@inscripcion_bp.route('/inscripcion/<int:inscripcion_id>', methods=['PUT'])
def actualizar_estatus(inscripcion_id):
    inscripcion = InscripcionAlumnos.query.get(inscripcion_id)
    if not inscripcion:
        return jsonify({"error": "Inscripción no encontrada"}), 404

    data = request.json
    nuevo_estatus = data.get('estatus')

    if nuevo_estatus not in ['cursando', 'aprobado', 'reprobado', 'retirado']:
        return jsonify({"error": "Estatus no válido"}), 400

    inscripcion.estatus = nuevo_estatus
    db.session.commit()
    return jsonify({"mensaje": "Estatus actualizado con éxito"})

# ✅ Eliminar una inscripción
@inscripcion_bp.route('/inscripcion/<int:inscripcion_id>', methods=['DELETE'])
def eliminar_inscripcion(inscripcion_id):
    inscripcion = InscripcionAlumnos.query.get(inscripcion_id)
    if not inscripcion:
        return jsonify({"error": "Inscripción no encontrada"}), 404

    db.session.delete(inscripcion)
    db.session.commit()
    return jsonify({"mensaje": "Inscripción eliminada exitosamente"})
