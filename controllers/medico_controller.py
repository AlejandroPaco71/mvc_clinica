from flask import request, redirect, url_for, Blueprint, flash
from models.medico_model import Medico
from view import medico_view
from utils.decorators import login_required, admin_required

medico_bp = Blueprint('medico', __name__, url_prefix="/medicos")

@medico_bp.route("/")
@login_required  # Proteger esta ruta
def index():
    # recupera todos los registros de médicos
    medicos = Medico.get_all()
    return medico_view.list(medicos)

@medico_bp.route("/create", methods=['GET', 'POST'])
@login_required  # Proteger esta ruta
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        
        medico = Medico(nombre, especialidad, telefono, correo)
        medico.save()
        flash('Registro exitoso', 'success')
        return redirect(url_for('medico.index'))
    
    return medico_view.create()

@medico_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required  # Proteger esta ruta
def edit(id):
    medico = Medico.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        correo = request.form['correo']
        
        # actualizar
        medico.update(nombre=nombre, especialidad=especialidad, telefono=telefono, correo=correo)
        flash('Medico actualizado exitosamente', 'success')
        return redirect(url_for("medico.index"))
        
    return medico_view.edit(medico)

@medico_bp.route("/delete/<int:id>")
@login_required  # Proteger esta ruta
def delete(id):
    medico = Medico.get_by_id(id)
    medico.delete()
    flash('Medico eliminado exitosamente', 'success')
    return redirect(url_for("medico.index"))