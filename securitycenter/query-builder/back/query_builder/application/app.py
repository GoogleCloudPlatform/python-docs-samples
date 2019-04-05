# coding: utf-8
import os
from os import path
from logging import Formatter
from flask import Flask
from query_builder.application.default_settings import LOGGER_FORMAT
from ..domain_model.db import database
from ..domain_model.models import Step, Query

from .blueprints.query import query_blueprint


def create_database():
    if os.getenv('db_type', 'Sqlite') == 'Sqlite':
        database.drop_tables([Step, Query], safe=True)
        database.create_tables([Step, Query], safe=True)
        database.close()


def create_app(mode):
    instance_path = path.join(path.abspath(
        path.dirname(__file__)), "%s_instance" % mode)

    app = Flask("query_builder",
                instance_path=instance_path,
                instance_relative_config=True)

    app.config.from_object('query_builder.application.default_settings')
    app.config.from_pyfile('config.cfg')
    app.register_blueprint(query_blueprint)
    # Changing pre configured log handler format to configured on query builder
    for handler in app.logger.handlers:
        handler.setFormatter(Formatter(LOGGER_FORMAT))

    return app
