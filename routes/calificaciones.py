from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from utils.extensions import db
from models.calificaciones import Calificaciones

calificaciones_bp = Blueprint('calificaciones_bp', __name__)

@calificaciones_bp.route('/')
def vista_calificaciones():
    calificaciones = Calificaciones.query.all()
    return render_template('admin_calificaciones.html', calificaciones=calificaciones)

@calificaciones_bp.route('/crear', methods=['POST'])
def asignar_calificacion():
    data = request.form
    nueva_calificacion = Calificaciones(
        usuario_id=data.get('usuario_id'),
        materia_id=data.get('materia_id'),
        cuatrimestre_id=data.get('cuatrimestre_id'),
        primer_parcial=data.get('primer_parcial'),
        segundo_parcial=data.get('segundo_parcial'),
        tercer_parcial=data.get('tercer_parcial')
    )
    nueva_calificacion.calcular_calificacion_final()
    db.session.add(nueva_calificacion)
    db.session.commit()
    return redirect(url_for('calificaciones_bp.vista_calificaciones'))

@calificaciones_bp.route('/editar/<int:id>', methods=['POST'])
def editar_calificacion(id):
    calificacion = Calificaciones.query.get(id)
    if not calificacion:
        return jsonify({"error": "Calificación no encontrada"}), 404
    calificacion.primer_parcial = request.form.get('primer_parcial')
    calificacion.segundo_parcial = request.form.get('segundo_parcial')
    calificacion.tercer_parcial = request.form.get('tercer_parcial')
    calificacion.calcular_calificacion_final()
    db.session.commit()
    return redirect(url_for('calificaciones_bp.vista_calificaciones'))

@calificaciones_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_calificacion(id):
    calificacion = Calificaciones.query.get(id)
    if not calificacion:
        return jsonify({"error": "Calificación no encontrada"}), 404
    db.session.delete(calificacion)
    db.session.commit()
    return redirect(url_for('calificaciones_bp.vista_calificaciones'))
