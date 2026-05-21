from flask import request, redirect, url_for, Blueprint, session, flash, render_template
from models.usuario_model import Usuario
from view import auth_view

auth_bp = Blueprint('auth', __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Buscar usuario por username
        usuario = Usuario.get_by_username(username)
        
        if usuario and usuario.verify_password(password):
            # Guardar datos en sesión
            session['user_id'] = usuario.id
            session['user_name'] = usuario.nombre
            session['user_rol'] = usuario.rol
            session['logged_in'] = True
            
            flash(f'Bienvenido {usuario.nombre}!', 'success')
            #Si logramos logearnos corectamente la vista se va directo a lista de medicos
            return redirect(url_for('medico.index'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
            return redirect(url_for('auth.login'))
    
    return auth_view.login()

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validamos que las contraseñas coincidan
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('auth.register'))
        
        # Validamos que el username no exista
        existing_user = Usuario.get_by_username(username)
        if existing_user:
            flash('El nombre de usuario ya existe', 'danger')
            return redirect(url_for('auth.register'))
        
        # Creamos el  nuevo usuario, por defecto con rol 'usuario'
        usuario = Usuario(nombre, username, password, 'usuario')
        usuario.save()
        
        flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('auth.login'))
    
    return auth_view.register()

@auth_bp.route("/logout")
def logout():
    # Limpiar la sesión
    session.clear()
    flash('Sesion cerrada Chau!!', 'info')
    return redirect(url_for('auth.login'))