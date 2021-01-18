import pytest
import flask

from main import app as flask_app


@pytest.fixture
def app() -> flask.app.Flask:
    yield flask_app


@pytest.fixture
def client(app: flask.app.Flask) -> flask.app.Flask:
    return app.test_client()
