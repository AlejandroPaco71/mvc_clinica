from flask import request, redirect, url_for, Blueprint
from models.paciente_model import Paciente
from view import paciente_view

paciente_bp = Blueprint('paciente', __name__, url_prefix="/pacientes")

@paciente_bp.route("/")
def index():
    # recupera todos los registros de pacientes
    pacientes = Paciente.get_all()
    return paciente_view.list(pacientes)

@paciente_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        paciente = Paciente(nombre, edad, direccion, telefono)
        paciente.save()
        return redirect(url_for('paciente.index'))
    
    return paciente_view.create()

@paciente_bp.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    paciente = Paciente.get_by_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        # actualizar
        paciente.update(nombre=nombre, edad=edad, direccion=direccion, telefono=telefono)
        return redirect(url_for("paciente.index"))
        
    return paciente_view.edit(paciente)

@paciente_bp.route("/delete/<int:id>")
def delete(id):
    paciente = Paciente.get_by_id(id)
    paciente.delete()
    return redirect(url_for("paciente.index"))