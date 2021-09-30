import flask
import pytest

from webhook import handleWebhook

# Create a fake 'app' for generating test request contexts.

request = {
    "queryResult": {
        "queryText": "hi",
        "intent": {
            "name": "projects/galstarter-316823/agent/intents/00c2877d-2440-447f-8dc1-045623a55bd4",
            "displayName": "Default Welcome Intent",
        },
    }
}


@pytest.fixture(scope="module")
def app():
    return flask.Flask(__name__)


def test_handleWebhook(app):
    with app.test_request_context(json=request):
        res = handleWebhook(flask.request)
        assert "Hello from a GCF Webhook" in str(res)
