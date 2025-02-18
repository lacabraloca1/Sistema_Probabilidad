from flask import Blueprint, request, flash,render_template, redirect, url_for, jsonify
from utils.extensions import db
from models.grupos import Grupos

grupos_bp = Blueprint('grupos_bp', __name__)

@grupos_bp.route('/')
def vista_grupos():
    grupos = Grupos.query.all()
    return render_template('admin_grupos.html', grupos=grupos)

@grupos_bp.route('/crear', methods=['POST'])
def crear_grupo():
    data = request.form
    nuevo_grupo = Grupos(nombre=data.get('nombre'), turno=data.get('turno'))
    db.session.add(nuevo_grupo)
    db.session.commit()
    return redirect(url_for('grupos_bp.vista_grupos'))

@grupos_bp.route('/editar/<int:id>', methods=['POST'])
def editar_grupo(id):
    grupo = Grupos.query.get(id)
    if not grupo:
        return jsonify({"error": "Grupo no encontrado"}), 404
    grupo.nombre = request.form.get('nombre')
    grupo.turno = request.form.get('turno')
    db.session.commit()
    return redirect(url_for('grupos_bp.vista_grupos'))

@grupos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_grupo(id):
    grupo = Grupos.query.get(id)
    if not grupo:
        return jsonify({"error": "Grupo no encontrado"}), 404

    db.session.delete(grupo)
    db.session.commit()

    # Restablecer el AUTO_INCREMENT después de eliminar
    db.session.execute("ALTER TABLE Grupos AUTO_INCREMENT = 1")
    db.session.commit()

    flash("Grupo eliminado correctamente", "success")
    return redirect(url_for('grupos_bp.vista_grupos'))
