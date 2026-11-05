from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Conecta SQLAlchemy con la app y crea las tablas si no existen."""
    db.init_app(app)
    from . import models  # noqa: F401  (registra los modelos)
    with app.app_context():
        db.create_all()
