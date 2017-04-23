import pytest
import responses


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('SPARKPOST_API_KEY', 'sparkpost-api-key')

    import main

    # Propagate exceptions to the test env
    main.app.testing = True
    return main.app.test_client()


def test_index(app):
    resp = app.get('/')
    assert resp.status_code == 200

@responses.activate
def test_send(app):
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        json={
          'results': {
            'total_rejected_recipients': 0,
            'total_accepted_recipients': 1,
            'id': '11668787484950529'
          }
        },
        status=200)
    resp = app.post('/send', data={'email':'roberta@example.com'})
    assert resp.status_code == 302

@responses.activate
def test_send_fail(app):
    responses.add(
        responses.POST,
        'https://api.sparkpost.com/api/v1/transmissions',
        json={
          'errors': [
            {
              'description': 'Unconfigured or unverified sending domain.',
              'code': '7001',
              'message': 'Invalid domain'
            }
          ]
        },
        status=400)
    resp = app.post('/send', data={'email': 'roberto@example.com'})
    assert resp.status_code == 200
    page = resp.data.decode('utf8')
    assert 'Something unfortunate happened' in page

