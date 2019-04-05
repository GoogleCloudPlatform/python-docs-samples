from flask import Flask

from .blueprints.creator import creator_blueprint


def create_app(mode):
    app = Flask("creator")
    app.register_blueprint(creator_blueprint)
    return app

