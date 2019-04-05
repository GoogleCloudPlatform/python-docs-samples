from creator import creator_app


def test_index():
    creator_app.app.testing = True
    client = creator_app.app.test_client()

    r = client.get('/')
    assert 204 == r.status_code
    assert '' == r.data.decode('utf-8')


def test_cron():
    creator_app.app.testing = True
    client = creator_app.app.test_client()

    r = client.get('/events/processor',
                   headers={'X-AppEngine-Cron': 'mocke_header'})
    assert 204 == r.status_code
    assert '' == r.data.decode('utf-8')


def test_pubsub_with_invalid_token():
    creator_app.app.testing = True
    client = creator_app.app.test_client()

    r = client.post('/_ah/push-handlers/receive_message?token=46577')
    assert 400 == r.status_code
    assert 'Invalid request: token required' == r.data.decode('utf-8')


def test_pubsub_with_valid_token():
    creator_app.app.testing = True
    client = creator_app.app.test_client()

    r = client.post('/_ah/push-handlers/receive_message?token=g8g232hhdh2h3dh2dh22ddoi2d282j')
    assert 204 == r.status_code
    assert '' == r.data.decode('utf-8')


def test_pubsub_without_token():
    creator_app.app.testing = True
    client = creator_app.app.test_client()

    r = client.post('/_ah/push-handlers/receive_message')
    assert 400 == r.status_code
    assert 'Invalid request: token required' == r.data.decode('utf-8')
