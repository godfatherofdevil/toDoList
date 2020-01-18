from flask import Blueprint

bp = Blueprint("api", __name__)

from todo.api import routes

__all__ = (bp,)
