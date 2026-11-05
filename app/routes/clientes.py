from flask import Blueprint, flash, redirect, render_template, request, url_for

from ..services import cliente_service as servicio

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")


@clientes_bp.get("/")
def index():
    q = request.args.get("q", "").strip()
    return render_template("clientes/index.html", clientes=servicio.listar(q), q=q)


@clientes_bp.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        cliente, errores, datos = servicio.crear(request.form)
        if not errores:
            flash(f"Contacto «{cliente.nombre}» creado.", "ok")
            return redirect(url_for("clientes.index"))
        return render_template("clientes/form.html", datos=datos, errores=errores, editando=False), 422
    return render_template("clientes/form.html", datos={}, errores={}, editando=False)


@clientes_bp.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    cliente = servicio.obtener(cliente_id)
    if request.method == "POST":
        ok, errores, datos = servicio.actualizar(cliente, request.form)
        if ok:
            flash("Cambios guardados.", "ok")
            return redirect(url_for("clientes.index"))
        return render_template("clientes/form.html", datos=datos, errores=errores,
                               editando=True, cliente=cliente), 422
    return render_template("clientes/form.html", datos=cliente, errores={},
                           editando=True, cliente=cliente)


@clientes_bp.post("/<int:cliente_id>/eliminar")
def eliminar(cliente_id):
    cliente = servicio.obtener(cliente_id)
    nombre = cliente.nombre
    servicio.eliminar(cliente)
    flash(f"Contacto «{nombre}» eliminado.", "ok")
    return redirect(url_for("clientes.index"))
