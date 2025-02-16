from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from utils.extensions import db
from models.cuatrimestre import Cuatrimestre

cuatrimestres_bp = Blueprint('cuatrimestres_bp', __name__)

@cuatrimestres_bp.route('/')
def vista_cuatrimestres():
    cuatrimestres = Cuatrimestre.query.all()
    return render_template('admin_cuatrimestres.html', cuatrimestres=cuatrimestres)

@cuatrimestres_bp.route('/crear', methods=['POST'])
def crear_cuatrimestre():
    data = request.form
    nuevo_cuatrimestre = Cuatrimestre(nombre=data.get('nombre'))
    db.session.add(nuevo_cuatrimestre)
    db.session.commit()
    return redirect(url_for('cuatrimestres_bp.vista_cuatrimestres'))

@cuatrimestres_bp.route('/editar/<int:id>', methods=['POST'])
def editar_cuatrimestre(id):
    cuatrimestre = Cuatrimestre.query.get(id)
    if not cuatrimestre:
        return jsonify({"error": "Cuatrimestre no encontrado"}), 404
    cuatrimestre.nombre = request.form.get('nombre')
    db.session.commit()
    return redirect(url_for('cuatrimestres_bp.vista_cuatrimestres'))

@cuatrimestres_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_cuatrimestre(id):
    cuatrimestre = Cuatrimestre.query.get(id)
    if not cuatrimestre:
        return jsonify({"error": "Cuatrimestre no encontrado"}), 404
    db.session.delete(cuatrimestre)
    db.session.commit()
    return redirect(url_for('cuatrimestres_bp.vista_cuatrimestres'))
