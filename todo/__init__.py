from flask import Flask
from flask_mongoengine import MongoEngine

from todo.config import app_config


def create_app(config_name="dev"):
    app = Flask("toDoList")
    app.config.from_object(app_config[config_name])
    app.db = MongoEngine(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from todo.api import bp as api_bp

    app.register_blueprint(api_bp)


__all__ = (create_app, register_blueprints)

