from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorador para requerir que el usuario esté logueado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Por favor inicia sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorador para requerir que el usuario sea administrador"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Por favor inicia sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        if session.get('user_rol') != 'admin':
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function