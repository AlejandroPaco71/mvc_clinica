from flask import Flask, request, session, redirect, url_for
from controllers import medico_controller, paciente_controller, consulta_controller, auth_controller
from database import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clinica.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mi_clave_secreta_super_segura_123"

db.init_app(app)


app.register_blueprint(medico_controller.medico_bp)
app.register_blueprint(paciente_controller.paciente_bp)
app.register_blueprint(consulta_controller.consulta_bp)
app.register_blueprint(auth_controller.auth_bp)

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if request.path == path else ''
    return(dict(is_active = is_active))


@app.route("/")
def home():
    if session.get('logged_in'):
        return "<h1>Bienvenido a la Clinica Médica</h1><a href='/medicos/'>Ir a Administrar Clinica </a>"
    else:
        return redirect(url_for('auth.login'))

if __name__ ==  "__main__"  :
    with app.app_context():
        db.create_all()
        # Crear usuario administrador por defecto (opcional)
        # from models.usuario_model import Usuario
        # if not Usuario.get_by_username('admin'):
        #     admin = Usuario('Administrador', 'admin', 'admin123', 'admin')
        #     admin.save()
        #     print("Usuario administrador creado: admin / admin123")
    app.run(debug=True)
 




















