from database import db

class Consulta(db.Model):
    __tablename__ = "consultas"
    
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    diagnostico = db.Column(db.String(250), nullable=False)
    tratamiento = db.Column(db.String(250), nullable=False)
    
    # Claves foráneas
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    # Relaciones
    medico = db.relationship('Medico', back_populates='consultas')
    paciente = db.relationship('Paciente', back_populates='consultas')
    
    def __init__(self, fecha, diagnostico, tratamiento, medico_id, paciente_id):
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.medico_id = medico_id
        self.paciente_id = paciente_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def get_all():
        return Consulta.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Consulta.query.get(id)
    
    def update(self, fecha=None, diagnostico=None, tratamiento=None, medico_id=None, paciente_id=None):
        if fecha:
            self.fecha = fecha
        if diagnostico:
            self.diagnostico = diagnostico
        if tratamiento:
            self.tratamiento = tratamiento
        if medico_id:
            self.medico_id = medico_id
        if paciente_id:
            self.paciente_id = paciente_id
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()