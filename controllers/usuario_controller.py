from flask import request, redirect, url_for, Blueprint, flash
from models.usuario_model import Usuario
from view import usuario_view
from utils.decorators import login_required, admin_required

usuario_bp = Blueprint('usuario', __name__, url_prefix="/usuarios")

@usuario_bp.route("/")
@login_required  # Proteger esta ruta
def index():
    # recupera todos los registros de usuarios
    usuarios = Usuario.get_all()
    return usuario_view.list(usuarios)


@usuario_bp.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        rol = request.form['rol']
        
        # Validamos que las contraseñas coincidan
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('usuario.create'))
        
        # Validamos que el username no exista
        existing_user = Usuario.get_by_username(username)
        if existing_user:
            flash('El nombre de usuario ya existe', 'danger')
            return redirect(url_for('usuario.create'))
        
        # Creamos el  nuevo usuario
        usuario = Usuario(nombre, username, password, rol)
        usuario.save()
        
        flash('Registro exitoso', 'success')
        #return redirect(url_for('usuario.login'))
        return redirect(url_for('usuario.index'))
    
    return usuario_view.create()

@usuario_bp.route("/edit/<int:id>", methods=['GET','POST'])
@login_required
def edit(id):
    usuario = Usuario.get_by_id(id)
    if not usuario:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('usuario.index'))
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form.get('password')  # Puede estar vacío
        confirm_password = request.form['confirm_password']
        rol = request.form['rol']
        
        # Verificamos si el username ya existe, excepto el mismo usuario
        existing_user = Usuario.query.filter_by(username=username).first()
        if existing_user and existing_user.id != id:
            flash('El nombre de usuario ya existe', 'danger')
            return redirect(url_for('usuario.edit', id=id))
        
        # Validamos que las contraseñas coincidan
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('usuario.edit'), id=id)
        
        # Si cambia el password o no 
        if password:
            usuario.update(nombre=nombre, username=username, password=password, rol=rol)
        else:
            usuario.update(nombre=nombre, username=username, rol=rol)
        
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('usuario.index'))
    
    return usuario_view.edit(usuario)

@usuario_bp.route("/delete/<int:id>")
@login_required  # Proteger esta ruta
def delete(id):
    usuario = Usuario.get_by_id(id)
    usuario.delete()
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for("usuario.index"))