import hmac
import secrets

from dotenv import load_dotenv
from flask import Flask, abort, redirect, request, session, url_for

load_dotenv()

from .config import get_config  # noqa: E402
from .database import db, init_db  # noqa: E402


def create_app(config_name=None):
    """Factory de la aplicación."""
    app = Flask(__name__)
    app.config.from_object(get_config(config_name))

    init_db(app)

    from .routes import clientes_bp
    app.register_blueprint(clientes_bp)

    @app.route("/")
    def inicio():
        return redirect(url_for("clientes.index"))

    # --- Protección CSRF sencilla para formularios POST ---
    @app.before_request
    def verificar_csrf():
        if request.method == "POST":
            esperado = session.get("csrf", "")
            recibido = request.form.get("csrf_token", "")
            if not esperado or not hmac.compare_digest(esperado, recibido):
                abort(400, "Token CSRF inválido. Recarga la página e inténtalo de nuevo.")

    @app.context_processor
    def inyectar_csrf():
        if "csrf" not in session:
            session["csrf"] = secrets.token_hex(16)
        return {"csrf_token": session["csrf"]}

    return app
