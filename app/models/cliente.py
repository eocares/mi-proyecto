from datetime import datetime

from ..database import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    telefono = db.Column(db.String(30))
    empresa = db.Column(db.String(120))
    notas = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Cliente {self.id} {self.nombre}>"
