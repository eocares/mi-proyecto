"""Lógica de negocio de contactos: validación y acceso a datos."""
import re

from sqlalchemy import or_

from ..database import db
from ..models import Cliente

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CAMPOS = ("nombre", "email", "telefono", "empresa", "notas")


def _limpiar(form):
    return {c: (form.get(c) or "").strip() for c in CAMPOS}


def validar(datos, cliente_id=None):
    errores = {}
    if not datos["nombre"]:
        errores["nombre"] = "El nombre es obligatorio."
    elif len(datos["nombre"]) > 100:
        errores["nombre"] = "El nombre no puede pasar de 100 caracteres."

    if not datos["email"]:
        errores["email"] = "El correo es obligatorio."
    elif not EMAIL_RE.match(datos["email"]):
        errores["email"] = "Escribe un correo válido."
    else:
        existente = Cliente.query.filter(db.func.lower(Cliente.email) == datos["email"].lower()).first()
        if existente and existente.id != cliente_id:
            errores["email"] = "Ya existe un contacto con ese correo."

    if datos["telefono"] and not re.match(r"^[0-9+()\-\s]{6,30}$", datos["telefono"]):
        errores["telefono"] = "Usa solo números, espacios, + ( ) o guiones."
    return errores


def listar(busqueda=""):
    consulta = Cliente.query
    if busqueda:
        patron = f"%{busqueda}%"
        consulta = consulta.filter(or_(
            Cliente.nombre.like(patron),
            Cliente.email.like(patron),
            Cliente.empresa.like(patron),
            Cliente.telefono.like(patron),
        ))
    return consulta.order_by(Cliente.nombre).all()


def obtener(cliente_id):
    return db.get_or_404(Cliente, cliente_id)


def crear(form):
    """Devuelve (cliente, errores, datos)."""
    datos = _limpiar(form)
    errores = validar(datos)
    if errores:
        return None, errores, datos
    cliente = Cliente(**datos)
    db.session.add(cliente)
    db.session.commit()
    return cliente, {}, datos


def actualizar(cliente, form):
    datos = _limpiar(form)
    errores = validar(datos, cliente_id=cliente.id)
    if errores:
        return False, errores, datos
    for campo, valor in datos.items():
        setattr(cliente, campo, valor)
    db.session.commit()
    return True, {}, datos


def eliminar(cliente):
    db.session.delete(cliente)
    db.session.commit()
