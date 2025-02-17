from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from utils.extensions import db
from scipy.stats import binom
from models.calificaciones import Calificaciones
from models.alumnos import Alumnos
from models.cuatrimestre import Cuatrimestre
from models.materias import Materias

calificaciones_bp = Blueprint('calificaciones_bp', __name__)

def calcular_probabilidad(primer_parcial, segundo_parcial, tercer_parcial):
    n = 3  # Número de parciales
    promedio = (primer_parcial + segundo_parcial + tercer_parcial) / 3
    
    # Ajuste de p basado en el promedio
    if promedio >= 9:
        p = 0.9
    elif promedio >= 8:
        p = 0.75
    elif promedio >= 7:
        p = 0.6
    elif promedio >= 6:
        p = 0.4
    else:
        p = 0.2
    
    # Número de parciales aprobados (>=7)
    parciales_aprobados = sum(1 for calificacion in [primer_parcial, segundo_parcial, tercer_parcial] if calificacion >= 7)

    # Probabilidad de aprobar al menos 2 parciales
    probabilidad_aprobar = 1 - binom.cdf(1, n, p)

    return round(probabilidad_aprobar * 100, 2)

@calificaciones_bp.route('/')
def vista_calificaciones():
    alumnos = Alumnos.query.all()
    materias = Materias.query.all()
    cuatrimestres = Cuatrimestre.query.all()

    calificaciones = Calificaciones.query.all()

    for calificacion in calificaciones:
        # Calcular la probabilidad de aprobar el cuatrimestre basado en las calificaciones de los tres parciales
        probabilidad = calcular_probabilidad(
            calificacion.primer_parcial,
            calificacion.segundo_parcial,
            calificacion.tercer_parcial
        )
        calificacion.probabilidad = probabilidad
        
    return render_template('admin_calificaciones.html', calificaciones=calificaciones, alumnos=alumnos, materias=materias, cuatrimestres=cuatrimestres)

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
