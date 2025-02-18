from flask import Blueprint, flash, request, render_template, redirect, url_for, jsonify
from utils.extensions import db
from scipy.stats import norm
from models.calificaciones import Calificaciones
from models.alumnos import Alumnos
from models.cuatrimestre import Cuatrimestre
from models.materias import Materias
from sqlalchemy.sql import text


calificaciones_bp = Blueprint('calificaciones_bp', __name__)

def calcular_probabilidad(primer_parcial, segundo_parcial, tercer_parcial):
    """
    Calcula la probabilidad de aprobar el cuatrimestre basado en las calificaciones de los tres parciales.
    La probabilidad depende de:
      - El promedio general.
      - La cantidad de parciales aprobados.
      - Un modelo de distribución normal para dar mayor realismo a la probabilidad.
    """

    # Parámetros básicos
    promedio = (primer_parcial + segundo_parcial + tercer_parcial) / 3
    parciales_aprobados = sum(1 for calificacion in [primer_parcial, segundo_parcial, tercer_parcial] if calificacion >= 70)

    # Casos extremos
    if parciales_aprobados == 0:
        return 0  # No hay posibilidad de pasar si no se aprobó ningún parcial
    elif parciales_aprobados == 3 and promedio >= 90:
        return 99  # Si aprobó todo con excelente promedio, alta probabilidad

    # Ajuste probabilístico basado en la normal
    # Media de aprobación = 75, Desviación estándar = 10 para mayor realismo
    probabilidad_base = norm.cdf(promedio, loc=75, scale=10) * 100

    # Ajuste según cantidad de parciales aprobados
    ajuste_parciales = {1: 0.5, 2: 0.75, 3: 1.0}
    probabilidad_final = probabilidad_base * ajuste_parciales.get(parciales_aprobados, 0)

    return round(probabilidad_final, 2)

def calcular_probabilidad_cuatrimestre(calificaciones):
    total_materias = len(calificaciones)
    if total_materias == 0:
        return 0.0  # Evitar división entre 0

    materias_aprobadas = sum(1 for c in calificaciones if c.calificacion_final >= 70)

    # Reglas para determinar la probabilidad
    if materias_aprobadas < (total_materias / 2):
        return 0.0  # No alcanzó el mínimo de 50% de materias aprobadas
    elif materias_aprobadas == total_materias:
        return 100.0  # Aprobó todas las materias

    # Ajuste probabilístico basado en la normal
    probabilidad_base = norm.cdf((materias_aprobadas / total_materias) * 100, loc=75, scale=10) * 100
    return round(probabilidad_base, 2)

@calificaciones_bp.route('/')
def vista_calificaciones():
    alumnos = Alumnos.query.all()
    materias = Materias.query.all()
    cuatrimestres = Cuatrimestre.query.all()

    alumnos_con_calificaciones = {}

    for alumno in alumnos:
        calificaciones = Calificaciones.query.filter_by(usuario_id=alumno.usuario_id).all()

        # Verifica si el alumno tiene calificaciones antes de asignarlas
        if not calificaciones:
            continue

        for calificacion in calificaciones:
            calificacion.probabilidad = calcular_probabilidad(
                calificacion.primer_parcial,
                calificacion.segundo_parcial,
                calificacion.tercer_parcial
            )

        probabilidad_cuatrimestre = calcular_probabilidad_cuatrimestre(calificaciones)

        alumnos_con_calificaciones[alumno.usuario_id] = {
            "alumno": alumno,
            "calificaciones": calificaciones,
            "probabilidad_cuatrimestre": probabilidad_cuatrimestre
        }

    return render_template('admin_calificaciones.html', alumnos_con_calificaciones=alumnos_con_calificaciones, alumnos=alumnos, materias=materias, cuatrimestres=cuatrimestres)

@calificaciones_bp.route('/crear', methods=['POST'])
def asignar_calificacion():
    data = request.form
    usuario_id = data.get('usuario_id')
    materia_id = data.get('materia_id')
    cuatrimestre_id = data.get('cuatrimestre_id')

    primer_parcial = float(data.get('primer_parcial', 0))
    segundo_parcial = float(data.get('segundo_parcial', 0))
    tercer_parcial = float(data.get('tercer_parcial', 0))

    calificacion_final = round((primer_parcial + segundo_parcial + tercer_parcial) / 3, 2)

    nueva_calificacion = Calificaciones(
        usuario_id=usuario_id,
        materia_id=materia_id,
        cuatrimestre_id=cuatrimestre_id,
        primer_parcial=primer_parcial,
        segundo_parcial=segundo_parcial,
        tercer_parcial=tercer_parcial,
        calificacion_final=calificacion_final
    )

    db.session.add(nueva_calificacion)
    db.session.commit()

    flash('Calificación asignada correctamente', 'success')
    return redirect(url_for('calificaciones_bp.vista_calificaciones'))

@calificaciones_bp.route('/editar/<int:id>', methods=['POST'])
def editar_calificacion(id):
    calificacion = Calificaciones.query.get(id)
    if not calificacion:
        return jsonify({"error": "Calificación no encontrada"}), 404
    
    calificacion.primer_parcial = float(request.form.get('primer_parcial', 0))
    calificacion.segundo_parcial = float(request.form.get('segundo_parcial', 0))
    calificacion.tercer_parcial = float(request.form.get('tercer_parcial', 0))
    calificacion.calcular_calificacion_final()

    db.session.commit()
    flash("Calificación actualizada correctamente", "success")
    return redirect(url_for('calificaciones_bp.vista_calificaciones'))

@calificaciones_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_calificacion(id):
    calificacion = Calificaciones.query.get(id)
    if not calificacion:
        return jsonify({"error": "Calificación no encontrada"}), 404

    db.session.delete(calificacion)
    db.session.commit()

    db.session.execute(text("ALTER TABLE Calificaciones AUTO_INCREMENT = 1"))
    db.session.commit()

    flash("Calificación eliminada correctamente", "warning")
    return redirect(url_for('calificaciones_bp.vista_calificaciones'))
