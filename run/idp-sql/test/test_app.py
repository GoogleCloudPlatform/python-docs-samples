from flask import render_template


def test_get_index(app, client):
    assert client.get('/').status_code == 200

def test_post_no_jwt(app, client):
    assert client.post('/').status_code == 401

def test_post_invalid_jwt(app, client):
    assert client.post('/', headers={"Authorization": "Bearer iam-a-token"}).status_code == 403
