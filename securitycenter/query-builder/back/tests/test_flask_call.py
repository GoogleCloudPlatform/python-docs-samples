import pytest
from query_builder.application import app as _app
from flask import url_for
from query_builder.application.blueprints.query import (
    AUTHENTICATED_USER_EMAIL_HEADER,
    AUTHENTICATED_USER_ID_HEADER,
    IAP_JWT_ASSERTION_HEADER
)


@pytest.fixture
def app():
    return _app.create_app('development')


def setup_function():
    _app.create_database()


class ResponseMock:
    def __init__(self, status_code, data):
        self.status_code = status_code
        self.data = data


def post_test_side_effect(*args, **kwargs):
    """Example how create mock return based on parameters"""
    return ResponseMock(200, kwargs['data'].upper())


def test_client_post_success(client, mocker):
    """Test example posting on flask application with status code 200 and dynamic response"""
    data = 'value'
    expected = data.upper()
    with mocker.patch('flask.testing.FlaskClient.post', side_effect=post_test_side_effect):
        res = client.post(url_for('query.list_queries'), data=data)
        assert res.status_code == 200, 'Status code should be 200'
        assert res.data == expected, 'Return should be changed to upper case'


def test_missing_security_headers_in_production():
    test_client = _app.create_app('production').test_client()
    """Test the the application raises 403 response with missing header in production mode"""
    res = test_client.get('/queries')
    assert res.status_code == 403, 'Status code should be 403'


def test_security_headers_in_production():
    test_client = _app.create_app('production').test_client()
    """Test the the application should not raises 403 response with security header in production mode"""
    res = test_client.get(
        '/queries',
        headers={
            AUTHENTICATED_USER_EMAIL_HEADER: 'test:example@example.org',
            AUTHENTICATED_USER_ID_HEADER: '3475023457204720447240',
            IAP_JWT_ASSERTION_HEADER: '34nhto043y90t2975tr04g09083u539yt94590h648u065'
        })
    assert res.status_code == 200, 'Status code should be 403'


def test_missing_security_headers_in_development():
    test_client = _app.create_app('development').test_client()
    """Test the the application should not raises 403 response with missing header in development mode"""
    res = test_client.get('/queries')
    assert res.status_code == 200, 'Status code should be 200'
